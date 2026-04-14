from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# ✅ Load .env
load_dotenv()


class Settings(BaseSettings):
    # ❌ OpenAI removed (now optional)
    openai_api_key: str | None = None

    # Vector DB
    vector_db_provider: str = "chroma"
    chroma_persist_directory: Path = Path("./storage/chroma")

    # ❌ Not used anymore (kept optional for safety)
    embedding_model: str | None = None
    llm_model: str | None = None

    # Chunking
    chunk_size: int = 1200
    chunk_overlap: int = 200

    # Project
    default_project: str = "energy-intelligence"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()