"""
Query routes for asking questions and getting citation-backed answers.
Supports both regular and streaming responses.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from backend.app.api.dependency_injection import (
    get_current_user,
    get_rag_workflow,
)
from backend.app.rag_pipeline.workflow_orchestration.rag_workflow import RAGWorkflow

router = APIRouter(prefix="/api/query", tags=["Query"])


class ChatRequest(BaseModel):
    question: str
    stream: bool = False


class Source(BaseModel):
    source: str
    page: Optional[str] = None
    chunk_id: Optional[str] = None
    reference: str


class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: list
    source_count: int


@router.post("/chat")
def ask_question(
    request: ChatRequest,
    user: dict = Depends(get_current_user),
    workflow: RAGWorkflow = Depends(get_rag_workflow),
):
    """
    Answers a question using the RAG pipeline.
    Returns answer with source citations.
    Handles Groq rate limits with retry.
    """
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    if request.stream:
        return StreamingResponse(
            _stream_answer(request.question, workflow),
            media_type="text/event-stream",
        )

    import time
    max_retries = 2
    for attempt in range(max_retries + 1):
        try:
            result = workflow.run(request.question)
            break
        except Exception as exc:
            err_str = str(exc)
            if attempt < max_retries and ("rate_limit" in err_str or "429" in err_str or "413" in err_str or "Request too large" in err_str):
                time.sleep(2.0 * (attempt + 1))
                continue
            raise

    return ChatResponse(
        question=result["query"],
        answer=result["answer"],
        sources=result["sources"],
        source_count=result["source_count"],
    )





async def _stream_answer(question: str, workflow: RAGWorkflow):
    """
    Streams the answer token by token using Server-Sent Events.
    """
    try:
        result = workflow.run(question)
        answer = result["answer"]

        for token in answer.split(" "):
            yield f"data: {token} \n\n"

        yield f"data: [SOURCES]{result['sources']}[/SOURCES]\n\n"
        yield "data: [DONE]\n\n"

    except Exception as exc:
        yield f"data: [ERROR]{str(exc)}\n\n"
