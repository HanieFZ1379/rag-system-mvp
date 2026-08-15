from dataclasses import dataclass
import yaml
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()  # Load .env for secrets and optional ENV

@dataclass
class Config:
    Qdrant_CollectionName: str
    QdrantURL: str

    def __init__(self, custom_cfg_path = None):

        # determine which YAML to load (based on ENV from .env, default to 'config.yaml')
        env = os.getenv("ENV", "default")  # e.g., 'dev', 'prod', or 'default'
        config_file = f"config.{env}.yaml" if env != "default" else "config.yaml"

        base_dir = Path(__file__).resolve().parent  # .../rag-system-mvp/app
        config_path = base_dir / config_file    # .../rag-system-mvp/app/config.yaml

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file '{config_path}' not found. Check your ENV or create the file.")
        
        with open(config_path, 'r') as f:
            data = yaml.safe_load(f)

        
        
        self.Qdrant_CollectionName = data['qdrant'].get('collection_name', "default_collection")
        self.QdrantURL = data['qdrant'].get('url', "http://localhost:6333/")

        self.EMB_TYPE = data['models'].get('emb_type', "huggingface")
        self.EMB_MODEL = data['models'].get('emb_model', "intfloat/multilingual-e5-large-instruct")
        self.CHAT_MODEL = data['models'].get('chat_model', "Qwen3-235B-A22B-Instruct-2507")
        

cfg = Config()