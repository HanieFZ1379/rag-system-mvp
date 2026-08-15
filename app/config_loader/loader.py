# config_loader/loader.py
import os
import yaml
from typing import Dict, Any

class ConfigLoader:
    """Container that provides hierarchical attribute access,
       dotted‑key dict access, and a flat view."""
    def __init__(self, data: Dict[str, Any]):
        object.__setattr__(self, "_data", data)
        object.__setattr__(self, "_flat", self._build_flat(data))

    @staticmethod
    def flatten(mapping: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
        flat: Dict[str, Any] = {}
        for k, v in mapping.items():
            new_key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                flat.update(ConfigLoader.flatten(v, new_key))
            else:
                flat[new_key] = v
        return flat

    @staticmethod
    def _build_flat(mapping: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
        return ConfigLoader.flatten(mapping, prefix)

    @property
    def flat(self) -> Dict[str, Any]:
        return dict(self._flat)

    def __getattr__(self, name: str) -> Any:
        data = object.__getattribute__(self, "_data")

        # 1) Look up in the YAML-backed config
        if name in data:
            value = data[name]
            if isinstance(value, dict):
                return ConfigLoader(value)
            return value

        # 2) Fallback to environment variables (for secrets such as API keys)
        env_val = os.getenv(name)
        if env_val is not None:
            return env_val

        # 3) Nothing found
        raise AttributeError(f"{self.__class__.__name__} has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        data = object.__getattribute__(self, "_data")
        data[name] = value
        flat = object.__getattribute__(self, "_flat")
        if isinstance(value, dict):
            for k in list(flat):
                if k == name or k.startswith(f"{name}."):
                    del flat[k]
            flat.update(self._build_flat(value, name))
        else:
            flat[name] = value

    def __getitem__(self, key: str) -> Any:
        data = object.__getattribute__(self, "_data")
        if key in data:
            return data[key]
        parts = key.split(".")
        current = data
        for part in parts:
            if not isinstance(current, dict) or part not in current:
                raise KeyError(key)
            current = current[part]
        return current

    def __setitem__(self, key: str, value: Any) -> None:
        data = object.__getattribute__(self, "_data")
        parts = key.split(".")
        current = data
        for part in parts[:-1]:
            if part not in current or not isinstance(current[part], dict):
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value
        flat = object.__getattribute__(self, "_flat")
        flat[key] = value
        if isinstance(value, dict):
            for k in list(flat):
                if k.startswith(f"{key}."):
                    del flat[k]
            flat.update(self._build_flat(value, key))

    def as_dict(self) -> Dict[str, Any]:
        return dict(self._data)

# load a yaml file (returns a dict, empty dict if file missing)
def _load_yaml(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

# Deep‑merge implementation 
def _deep_merge(base: dict, overlay: dict) -> dict:
    for k, v in overlay.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            base[k] = _deep_merge(base.get(k, {}), v)
        else:
            base[k] = v
    return base


# we build the singleton configuration object

_BASE_CFG = _load_yaml(os.path.join(os.path.dirname(__file__), "..", "config", "default.yaml"))

# Determine which workflow is active (environment variable must be set BEFORE
# any import of this module)
_WORKFLOW = os.getenv("APP_WORKFLOW", "w1")   # fallback to "w1" for local testing
_WORKFLOW_CFG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", f"{_WORKFLOW}.yaml")
_WORKFLOW_CFG = _load_yaml(_WORKFLOW_CFG_PATH)
_MERGED_DICT = _deep_merge(_BASE_CFG.copy(), _WORKFLOW_CFG)
# wrap the merged dict in ConfigLoader
_CONFIG = ConfigLoader(_MERGED_DICT)
# accessor – this is the singleton you will use everywhere

def get_config() -> ConfigLoader:
    """Return the already built, read‑only configuration."""
    return _CONFIG