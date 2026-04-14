from typing import Dict, Any, List

from .vector_store import VectorStore
from .config import settings


def answer_question(question: str, project: str = None, top_k: int = 5) -> Dict[str, Any]:
    project_name = project or settings.default_project
    store = VectorStore(project_name)

    retrieved = store.query(question, top_k=top_k)

    if not retrieved:
        return {
            "answer": "No relevant document content was found for this question.",
            "sources": [],
            "retrieval_count": 0,
        }

    # ✅ SIMPLE CONTEXT-BASED ANSWER (NO OPENAI)
    answer_parts = []
    for doc in retrieved:
        content = doc.get("content", "")
        if content:
            answer_parts.append(content)

    answer = "\n\n".join(answer_parts)

    sources = [
        {
            "source": doc["metadata"].get("source"),
            "chunk_index": doc["metadata"].get("chunk_index"),
            "distance": doc.get("distance"),
        }
        for doc in retrieved
    ]

    return {
        "answer": answer,
        "sources": sources,
        "retrieval_count": len(retrieved),
    }