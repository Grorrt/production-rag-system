"""
Tests for the retrieval pipeline including hybrid search and re-ranking.
"""

import pytest


class TestHybridSearch:
    def test_bm25_index_building(self):
        from backend.app.rag_pipeline.information_retrieval.hybrid_search import HybridSearch

        search = HybridSearch.__new__(HybridSearch)
        chunks = [
            {"chunk_id": "1", "text": "React useEffect cleanup function"},
            {"chunk_id": "2", "text": "Next.js dynamic routing with file system"},
            {"chunk_id": "3", "text": "FastAPI dependency injection system"},
        ]

        search.build_bm25_index(chunks)
        assert search._bm25_ready is True
        assert search._bm25_index is not None


class TestVectorDatabase:
    @pytest.mark.skip(reason="Requires Qdrant to be running")
    def test_collection_creation(self):
        from backend.app.rag_pipeline.information_retrieval.vector_database import VectorDatabase

        db = VectorDatabase()
        collections = db.client.get_collections().collections
        names = [c.name for c in collections]

        assert db.collection_name in names

    @pytest.mark.skip(reason="Requires Qdrant to be running")
    def test_health_check(self):
        from backend.app.rag_pipeline.information_retrieval.vector_database import VectorDatabase

        db = VectorDatabase()
        assert db.health_check() is True


class TestResultRanker:
    def test_reranker_returns_top_k(self):
        from backend.app.rag_pipeline.information_retrieval.result_ranker import ResultRanker

        ranker = ResultRanker()
        chunks = [
            {"chunk_id": "1", "text": "React hooks and useEffect"},
            {"chunk_id": "2", "text": "Python programming language"},
            {"chunk_id": "3", "text": "useEffect cleanup in React"},
        ]

        results = ranker.rerank("useEffect cleanup", chunks, top_k=2)
        assert len(results) <= 2
        assert all("reranker_score" in r for r in results)
