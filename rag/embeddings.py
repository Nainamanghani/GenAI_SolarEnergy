from typing import List
from sentence_transformers import SentenceTransformer

# ✅ Load FREE local embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_texts(texts: List[str]) -> List[List[float]]:
    if not texts:
        return []
    
    embeddings = model.encode(texts)
    return embeddings.tolist()


def embed_query(query: str) -> List[float]:
    embedding = model.encode(query)
    return embedding.tolist()
