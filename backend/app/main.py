"""
FastAPI application entry point for the Production RAG System.
Configures middleware, registers routes, and starts the server.
"""

import traceback as tb
import sys
import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.app.configuration.app_config import config
from backend.app.api.middleware.request_logging import RequestLoggingMiddleware
from backend.app.api.routes import (
    user_authentication,
    ingest_documents,
    answer_questions,
    evaluate_system,
)

logger = structlog.get_logger()

app = FastAPI(
    title=config.app_name,
    version=config.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catches all unhandled exceptions and returns JSON with traceback."""
    trace = "".join(tb.format_exception(type(exc), exc, exc.__traceback__))
    logger = structlog.get_logger()
    logger.error("unhandled_exception", error=str(exc), traceback=trace)
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "traceback": trace.split("\n")[-10:]},
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestLoggingMiddleware)

app.include_router(user_authentication.router)
app.include_router(ingest_documents.router)
app.include_router(answer_questions.router)
app.include_router(evaluate_system.router)


@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": config.app_name,
        "version": config.app_version,
    }


@app.get("/api/stats")
def system_stats():
    """Returns system usage statistics."""
    return {
        "total_documents": 0,
        "total_chunks": 0,
        "queries_today": 0,
        "average_latency_ms": 0,
        "uptime_hours": 0,
    }


@app.on_event("startup")
async def startup_event():
    logger.info("Starting Production RAG System", version=config.app_version)
    # Warm up pipeline components to catch errors early
    try:
        from backend.app.rag_pipeline.document_processing.embedding_generator import EmbeddingGenerator
        gen = EmbeddingGenerator()
        logger.info("embedding_generator_ok", cache_dir=config.cache_dir)
    except Exception as e:
        logger.error("embedding_generator_failed", error=str(e))
    try:
        from backend.app.rag_pipeline.information_retrieval.vector_database import VectorDatabase
        db = VectorDatabase()
        logger.info("vector_database_ok", host=config.qdrant_host, collection=config.qdrant_collection)
    except Exception as e:
        logger.error("vector_database_failed", error=str(e))


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Production RAG System")
