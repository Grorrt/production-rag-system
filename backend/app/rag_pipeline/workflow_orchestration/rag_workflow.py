"""
LangGraph workflow that orchestrates the entire RAG pipeline.
State machine with nodes for query transform, hybrid search,
re-ranking, hallucination checking, generation, and citation formatting.
"""

from typing import List, Optional, TypedDict, Annotated

from langgraph.graph import StateGraph, END

from backend.app.configuration.app_config import config
from backend.app.rag_pipeline.document_processing.embedding_generator import EmbeddingGenerator
from backend.app.rag_pipeline.information_retrieval.vector_database import VectorDatabase
from backend.app.rag_pipeline.information_retrieval.hybrid_search import HybridSearch
from backend.app.rag_pipeline.information_retrieval.result_ranker import ResultRanker
from backend.app.rag_pipeline.answer_generation.rag_chain import RAGGenerationChain


class WorkflowState(TypedDict):
    query: str
    query_variants: List[str]
    retrieved_chunks: List[dict]
    final_chunks: List[dict]
    generation: Optional[dict]
    error: Optional[str]
    sources: List[dict]


class RAGWorkflow:
    """
    LangGraph-based workflow for the complete RAG pipeline.
    Nodes: query_transform -> hybrid_search -> rerank -> hallucination_check -> generate
    """

    def __init__(self, embedder=None, vector_db=None, hybrid_search=None, reranker=None, generator=None):
        self.embedder = embedder or EmbeddingGenerator()
        self.vector_db = vector_db or VectorDatabase()
        self.hybrid_search = hybrid_search or HybridSearch(self.vector_db, self.embedder)
        self.reranker = reranker or ResultRanker()
        self.generator = generator or RAGGenerationChain()

        self._build_graph()

    def _query_transform_node(self, state: WorkflowState) -> dict:
        """
        Transforms the user query into search variants.
        For now, uses the original query and a simplified version.
        In production, this could use the LLM to generate alternatives.
        """
        query = state["query"]
        variants = [query, query.lower().strip()]
        return {"query_variants": variants}

    def _hybrid_search_node(self, state: WorkflowState) -> dict:
        """
        Executes hybrid search using the best query variant.
        """
        query = state["query"]
        results = self.hybrid_search.search(
            query=query,
            top_k=config.retrieval_top_k,
        )
        return {"retrieved_chunks": results}

    def _rerank_node(self, state: WorkflowState) -> dict:
        chunks = state["retrieved_chunks"]
        if not chunks:
            return {"final_chunks": [], "error": "No relevant information found in the knowledge base."}
        reranked = self.reranker.rerank(state["query"], chunks, top_k=config.reranker_top_k)
        return {"final_chunks": reranked[: config.final_top_k]}

    def _generate_node(self, state: WorkflowState) -> dict:
        """
        Generates the final answer using the LLM with retrieved context.
        Falls back to general knowledge if no relevant chunks found
        or if the LLM determines context is irrelevant.
        """
        query = state["query"]
        chunks = state["final_chunks"]

        if not chunks:
            result = self.generator.generate_general(query=query)
            return {"generation": result, "sources": []}

        result = self.generator.generate(query=query, chunks=chunks)
        answer = result.get("answer", "").lower()

        # If LLM says it can't find the answer in documents, fall back to general knowledge
        cannot_find_phrases = [
            "cannot find",
            "cannot find this information",
            "not found in the provided documents",
            "do not have information",
            "no information",
            "i cannot find",
        ]
        if any(phrase in answer for phrase in cannot_find_phrases):
            general_result = self.generator.generate_general(query=query)
            return {"generation": general_result, "sources": []}

        return {"generation": result, "sources": result.get("sources", [])}

    def _build_graph(self):
        """
        Builds the LangGraph state machine.
        """
        workflow = StateGraph(WorkflowState)

        workflow.add_node("query_transform", self._query_transform_node)
        workflow.add_node("hybrid_search", self._hybrid_search_node)
        workflow.add_node("rerank", self._rerank_node)
        workflow.add_node("generate", self._generate_node)

        workflow.set_entry_point("query_transform")

        workflow.add_edge("query_transform", "hybrid_search")
        workflow.add_edge("hybrid_search", "rerank")
        workflow.add_edge("rerank", "generate")
        workflow.add_edge("generate", END)

        self.app = workflow.compile()

    def run(self, query: str) -> dict:
        """
        Runs the complete RAG workflow for a given query.
        Returns the generated answer with sources.
        """
        initial_state: WorkflowState = {
            "query": query,
            "query_variants": [query],
            "retrieved_chunks": [],
            "final_chunks": [],
            "generation": None,
            "error": None,
            "sources": [],
        }

        result = self.app.invoke(initial_state)

        return {
            "query": query,
            "answer": result.get("generation", {}).get("answer", ""),
            "sources": result.get("generation", {}).get("sources", []),
            "source_count": result.get("generation", {}).get("source_count", 0),
            "error": result.get("error"),
        }
