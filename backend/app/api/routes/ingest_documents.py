"""
Ingestion routes for uploading and processing documents.
Handles file validation, text extraction, chunking, embedding, and storage.
"""

from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from backend.app.api.dependency_injection import (
    get_current_user,
    get_document_loader,
    get_text_splitter,
    get_embedding_generator,
    get_vector_database,
    get_rag_workflow,
)
from backend.app.rag_pipeline.document_processing.document_loader import DocumentLoaderFactory
from backend.app.rag_pipeline.document_processing.text_splitter import TextSplitter
from backend.app.rag_pipeline.document_processing.embedding_generator import EmbeddingGenerator
from backend.app.rag_pipeline.information_retrieval.vector_database import VectorDatabase

router = APIRouter(prefix="/api/ingest", tags=["Ingestion"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".html", ".htm", ".md", ".mdx", ".txt"}


@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    user: dict = Depends(get_current_user),
    loader: DocumentLoaderFactory = Depends(get_document_loader),
    splitter: TextSplitter = Depends(get_text_splitter),
    embedder: EmbeddingGenerator = Depends(get_embedding_generator),
    vector_db: VectorDatabase = Depends(get_vector_database),
):
    """
    Uploads a document, processes it, and stores chunks in Qdrant.
    """
    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {extension}. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    file_path = UPLOAD_DIR / file.filename
    content = file.file.read()
    file_path.write_bytes(content)

    try:
        documents = loader.load_document(str(file_path))
        chunks = splitter.split_documents(documents)

        texts = [chunk["text"] for chunk in chunks]
        embeddings = embedder.encode(texts)

        points_count = vector_db.upsert_chunks(chunks, embeddings)

        workflow = get_rag_workflow()
        workflow.hybrid_search.build_bm25_index(chunks)

        return {
            "message": "Document ingested successfully",
            "file_name": file.filename,
            "chunks_created": len(chunks),
            "points_stored": points_count,
            "documents_loaded": len(documents),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process document: {str(exc)}",
        )
