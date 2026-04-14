# Energy Document Intelligence RAG System

A complete Retrieval-Augmented Generation (RAG) architecture tailored for energy domain document intelligence. This system ingests professional documents such as PDF reports and manuals, converts them into searchable vector embeddings, and enables accurate, evidence-grounded question answering.

## System Overview

- Document ingestion: upload PDF and text-based energy documentation.
- Text processing: extract, clean, chunk, and annotate document passages.
- Embedding pipeline: convert passage chunks to semantic vectors.
- Vector database: store embeddings in a high-performance retrieval store.
- Retrieval: find the most relevant domain content for each user question.
- Response generation: use an LLM API to answer with strictly grounded information.

## Architecture

The architecture is intentionally modular and composed of four main layers:

1. **Ingestion Layer**
   - Accepts uploaded documents.
   - Supports PDF extraction and text normalization.
   - Splits text into overlapping semantic chunks.

2. **Embedding Layer**
   - Leverages OpenAI embeddings or any provider-compatible embedding model.
   - Converts chunks into vector embeddings.

3. **Vector Storage Layer**
   - Uses a vector database abstraction.
   - Default implementation uses Chroma for local high-performance retrieval.
   - Can be extended to Pinecone, Milvus, Weaviate, or other providers.

4. **Retrieval + Generation Layer**
   - Performs semantic search for relevant chunks.
   - Constructs a grounded prompt with domain-specific context.
   - Returns evidence-aware answers via an LLM API.

## Key Files

- `app.py` - FastAPI service for upload and query endpoints.
- `rag/document_processor.py` - PDF text extraction and document cleaning.
- `rag/chunker.py` - Document chunking logic with overlap.
- `rag/embeddings.py` - Embedding provider wrapper.
- `rag/vector_store.py` - Vector database abstraction via Chroma.
- `rag/qa.py` - Retrieval and prompt orchestration for QA.
- `.env.example` - Environment configuration template.

## Quick Start

1. Create a Python environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and configure keys.
4. Start the API:
   ```bash
   uvicorn app:app --reload
   ```
5. Upload documents to `/upload` and ask questions via `/query`.

## Extension Points

- Replace Chroma with a cloud vector store by implementing `rag/vector_store.py`.
- Add support for DOCX, HTML, or ZIP ingestion.
- Add a UI layer for file upload, conversational UX, and source view.
- Extend prompt engineering with energy-specific grounding templates.

## Security and Compliance

- Store only metadata and embeddings from the documents.
- Keep API keys in environment variables, not source control.
- Return source citations and document references in responses.
