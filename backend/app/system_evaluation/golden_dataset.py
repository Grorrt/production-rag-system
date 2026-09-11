"""
Golden evaluation dataset for testing RAG performance.
Contains curated question-answer pairs with expected sources.
"""

from typing import List, Dict


class EvaluationSample:
    def __init__(
        self,
        question: str,
        ground_truth: str,
        expected_sources: List[str],
        category: str,
    ):
        self.question = question
        self.ground_truth = ground_truth
        self.expected_sources = expected_sources
        self.category = category


def load_golden_dataset() -> List[EvaluationSample]:
    """
    Loads the golden evaluation dataset.
    In production, this would load from a file or database.
    """
    return [
        EvaluationSample(
            question="How do I implement dynamic routing in Next.js?",
            ground_truth="In Next.js, dynamic routing is implemented using the app directory with "
            "folder names in square brackets like [slug]. Files named page.tsx inside these "
            "folders become dynamic routes.",
            expected_sources=["nextjs-docs"],
            category="routing",
        ),
        EvaluationSample(
            question="What is the useEffect cleanup function?",
            ground_truth="The useEffect cleanup function is returned from the effect function and "
            "runs when the component unmounts or before the effect re-runs. It is used to "
            "clean up subscriptions, timers, or event listeners.",
            expected_sources=["react-docs"],
            category="hooks",
        ),
        EvaluationSample(
            question="How does LangChain memory work?",
            ground_truth="LangChain memory stores conversation history for context-aware responses. "
            "Common types include ConversationBufferMemory, ConversationSummaryMemory, "
            "and VectorStoreRetrieverMemory.",
            expected_sources=["langchain-docs"],
            category="memory",
        ),
        EvaluationSample(
            question="What is FastAPI dependency injection?",
            ground_truth="FastAPI dependency injection uses the Depends() function to declare "
            "dependencies in path operation parameters. FastAPI automatically resolves "
            "and injects these dependencies when handling requests.",
            expected_sources=["fastapi-docs"],
            category="api",
        ),
    ]
