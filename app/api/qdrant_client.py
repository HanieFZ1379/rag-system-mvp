from app.config import cfg
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings 
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams




class Qdrant_base:
    def __init__(self,collection_name=cfg.qdrant.collection_name , embed_model=cfg.models.emb_model ,qdrant_url = cfg.qdrant.url):
        self.client = QdrantClient(qdrant_url)  #  ":memory:" for in-memory testing 
        self.embedding_model = HuggingFaceEmbeddings(model_name= embed_model , 
        # model_kwargs={"local_files_only":True, "device": "cuda",               # Or "cpu" if needed
        # "trust_remote_code": True,      # Required for Qwen models
    # },
    encode_kwargs={
        "batch_size": 4,                # For documents/indexing; adjust down if OOM
        "normalize_embeddings": True    # Recommended for cosine similarity
        # NO prompt_name here—documents don't need it
    },
    query_encode_kwargs={
        "prompt_name": "query",         # For queries during search/retrieval
        "batch_size": 4,                # Can match or differ from encode_kwargs
        "normalize_embeddings": True
    })
        
    def __call__(self, *args, **kwds):
        raise NotImplementedError(" must implement the __call__ method ")

    def create_collection(self,collection_name : str , size = 768 ) :
        self.client.create_collection(collection_name= collection_name,
        vectors_config=VectorParams(size=size, distance=Distance.COSINE))
        print(f"Created collection: {collection_name}")

    def delete_collection(self,collection_name : str):
        collections = [c.name for c in self.client.get_collections().collections]
        if collection_name in collections:
            self.client.delete_collection(collection_name=collection_name)
            print(f"Deleted existing collection: {collection_name}")

    # ── indexing / write ──
    def add_documents(self, documents: List[Document]) -> None:
        """Embed + store documents"""
        # Use chunk_id as point ID
        ids = [doc.metadata["chunk_id"] for doc in documents]
        qdrant_store = QdrantVectorStore.from_documents(
            documents=documents,
            embedding=self.embedding_model,
            url=self.qdrant_url,
            prefer_grpc=False,
            collection_name=self.collection_name,
            batch_size=128,
            ids=ids
            # content_payload_key="chunk_text",
    )
    print("Qdrant index created with metadata (payload).")
    return qdrant_store

if __name__=="__main__":
    q = Qdrant_base()
    q.create_collection("test1")
    # q.delete_collection("test1")
