from dotenv import load_dotenv
import os
# Force pure‑offline mode for every HF library
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
load_dotenv()  # Load .env variables

# Load your merged configuration (see previous answer)
from app.config_loader.loader import get_config
CFG = get_config()