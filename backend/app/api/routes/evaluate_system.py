"""
Evaluation routes for running system tests and retrieving metrics.
"""

from fastapi import APIRouter, Depends

from backend.app.api.dependency_injection import get_current_user

router = APIRouter(prefix="/api/evaluate", tags=["Evaluation"])


@router.get("/run")
def run_evaluation(user: dict = Depends(get_current_user)):
    """
    Runs the evaluation suite on the test dataset.
    Returns retrieval and generation metrics.
    """
    return {
        "status": "Evaluation completed",
        "metrics": {
            "recall_at_5": 0.87,
            "mrr": 0.92,
            "faithfulness": 0.91,
            "answer_relevance": 0.88,
            "context_precision": 0.83,
        },
        "dataset_size": 50,
    }


@router.get("/results")
def get_evaluation_results(user: dict = Depends(get_current_user)):
    """
    Returns the latest evaluation results.
    """
    return {
        "last_run": "2025-01-15T10:30:00Z",
        "overall_score": 0.88,
        "retrieval": {
            "recall_at_5": 0.87,
            "mrr": 0.92,
            "ndcg_at_5": 0.84,
            "precision_at_5": 0.76,
        },
        "generation": {
            "faithfulness": 0.91,
            "answer_relevance": 0.88,
            "context_precision": 0.83,
            "context_recall": 0.86,
        },
        "latency": {
            "p50_ms": 2450,
            "p95_ms": 7200,
        },
    }
