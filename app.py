import logging
from pathlib import Path
from typing import List

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from rag.config import settings
print("API KEY:", settings.openai_api_key)
from rag.document_processor import load_document_bytes, document_to_chunks
from rag.qa import answer_question
from rag.vector_store import VectorStore

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Energy Document Intelligence RAG")


# =========================
# RESPONSE MODELS
# =========================
class UploadResponse(BaseModel):
    project: str
    file_names: List[str]
    chunk_count: int
    message: str


class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]
    retrieval_count: int


# =========================
# STARTUP EVENT
# =========================
@app.on_event("startup")
def startup_event() -> None:
    Path(settings.chroma_persist_directory).mkdir(parents=True, exist_ok=True)
    logger.info("✅ Chroma directory ready")


# =========================
# UPLOAD API
# =========================
@app.post("/upload", response_model=UploadResponse)
async def upload_documents(
    file: UploadFile = File(...),
    project: str = Form(None),
) -> UploadResponse:

    project_name = project or settings.default_project
    logger.info(f"📂 Upload started for project: {project_name}")

    try:
        # Step 1: Read file
        data = await file.read()
        if not data:
            raise HTTPException(status_code=400, detail="Empty file uploaded")

        logger.info("✅ File received")

        # Step 2: Extract text from PDF
        source_name, text = load_document_bytes(file.filename, data)

        if not text or len(text.strip()) == 0:
            raise HTTPException(status_code=400, detail="No text found in PDF")

        logger.info("✅ PDF processed successfully")

        # Step 3: Convert into chunks
        chunks = document_to_chunks(source_name, text)

        if not chunks:
            raise HTTPException(status_code=400, detail="No chunks created from document")

        logger.info(f"✅ Created {len(chunks)} chunks")

        # Step 4: Store in vector DB
        store = VectorStore(project_name)
        store.add_documents(chunks)

        logger.info("✅ Stored in vector database")

        return UploadResponse(
            project=project_name,
            file_names=[file.filename],
            chunk_count=len(chunks),
            message=f"Indexed {len(chunks)} chunks for project '{project_name}'.",
        )

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"❌ Upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


# =========================
# QUERY API
# =========================
@app.post("/query", response_model=QueryResponse)
async def query_documents(
    question: str = Form(...),
    project: str = Form(None),
    top_k: int = Form(5),
) -> QueryResponse:

    project_name = project or settings.default_project
    logger.info(f"🔍 Query received: {question}")

    try:
        answer_payload = answer_question(
            question,
            project=project_name,
            top_k=top_k
        )

        return QueryResponse(**answer_payload)

    except Exception as e:
        logger.error(f"❌ Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health_check() -> dict:
    return {
        "status": "ok",
        "project": settings.default_project
    }