"""
FastAPI dependency injection for shared services and authentication.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from backend.app.configuration.user_security import decode_token
from backend.app.rag_pipeline.workflow_orchestration.rag_workflow import RAGWorkflow
from backend.app.rag_pipeline.document_processing.embedding_generator import EmbeddingGenerator
from backend.app.rag_pipeline.information_retrieval.vector_database import VectorDatabase
from backend.app.rag_pipeline.document_processing.document_loader import DocumentLoaderFactory
from backend.app.rag_pipeline.document_processing.text_splitter import TextSplitter

security = HTTPBearer()

_rag_workflow = None
_embedding_generator = None
_vector_database = None


def get_rag_workflow() -> RAGWorkflow:
    global _rag_workflow
    if _rag_workflow is None:
        embedder = get_embedding_generator()
        vector_db = get_vector_database()
        _rag_workflow = RAGWorkflow(embedder=embedder, vector_db=vector_db)
    return _rag_workflow


def get_embedding_generator() -> EmbeddingGenerator:
    global _embedding_generator
    if _embedding_generator is None:
        _embedding_generator = EmbeddingGenerator()
    return _embedding_generator


def get_vector_database() -> VectorDatabase:
    global _vector_database
    if _vector_database is None:
        _vector_database = VectorDatabase()
    return _vector_database


def get_document_loader():
    return DocumentLoaderFactory()


def get_text_splitter():
    return TextSplitter()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """
    Validates the JWT token and returns the current user.
    """
    try:
        payload = decode_token(credentials.credentials)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
            )
        return {"username": username, "user_id": payload.get("user_id", "")}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
