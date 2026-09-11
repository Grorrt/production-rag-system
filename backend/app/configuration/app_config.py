from pydantic_settings import BaseSettings
from pathlib import Path


_ENV_FILE = Path(__file__).parent.parent.parent / ".env"


class AppConfig(BaseSettings):
    app_name: str = "Production RAG System"
    app_version: str = "1.0.0"
    debug: bool = False

    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection: str = "documents"
    qdrant_api_key: str = ""

    embedding_model: str = "BAAI/bge-base-en-v1.5"
    embedding_dimension: int = 768
    embedding_device: str = "cpu"

    llm_provider: str = "groq"
    llm_model: str = "llama-3.1-8b-instant"
    llm_base_url: str = "http://localhost:11434"
    llm_temperature: float = 0.3
    llm_max_tokens: int = 2048

    groq_api_key: str = ""
    groq_fallback_api_key: str = ""
    groq_model: str = "llama-3.1-8b-instant"

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    reranker_model: str = "BAAI/bge-reranker-v2-m3"

    chunk_size: int = 500
    chunk_overlap: int = 75

    retrieval_top_k: int = 30
    reranker_top_k: int = 8
    final_top_k: int = 10

    secret_key: str = "change-this-to-a-secure-random-key-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    langfuse_host: str = "http://localhost:3001"
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""

    cache_dir: str = str(Path.home() / ".cache" / "rag_system")

    model_config = {"env_file": str(_ENV_FILE), "env_file_encoding": "utf-8"}


config = AppConfig()
