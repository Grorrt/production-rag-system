"""
Hybrid search combining BM25 (keyword) and dense vector search.
Uses Reciprocal Rank Fusion (RRF) to merge results from both approaches.
"""

import math
from typing import List, Optional

from rank_bm25 import BM25Okapi

from backend.app.configuration.app_config import config


class HybridSearch:
    """
    Performs hybrid search using both BM25 keyword matching and dense vector search.
    Results are merged using Reciprocal Rank Fusion (RRF).
    """

    def __init__(self, vector_database, embedding_generator):
        self.vector_db = vector_database
        self.embedder = embedding_generator
        self._bm25_index = None
        self._bm25_chunks = []
        self._bm25_ready = False

    def build_bm25_index(self, chunks: List[dict]):
        """
        Builds a BM25 index from a list of chunks.
        Should be called after ingestion to enable hybrid search.
        Appends to existing index if one exists.
        """
        existing_ids = {c["chunk_id"] for c in self._bm25_chunks} if self._bm25_ready else set()
        new_chunks = [c for c in chunks if c["chunk_id"] not in existing_ids]

        if not new_chunks and self._bm25_ready:
            return

        all_chunks = list(self._bm25_chunks) + new_chunks if self._bm25_ready else list(new_chunks)

        tokenized_chunks = []
        for chunk in all_chunks:
            tokens = self._tokenize(chunk["text"])
            tokenized_chunks.append(tokens)

        self._bm25_index = BM25Okapi(tokenized_chunks)
        self._bm25_chunks = all_chunks
        self._bm25_ready = True
        self._bm25_initialized = True

    def _tokenize(self, text: str) -> List[str]:
        """Simple whitespace and punctuation tokenization."""
        import re
        tokens = re.findall(r"\w+", text.lower())
        return tokens

    def _bm25_search(
        self,
        query: str,
        top_k: int = 20,
    ) -> List[dict]:
        """
        Performs BM25 keyword search.
        """
        if not self._bm25_ready:
            return []

        tokenized_query = self._tokenize(query)
        scores = self._bm25_index.get_scores(tokenized_query)

        scored_chunks = []
        for idx, score in enumerate(scores):
            scored_chunks.append({
                **self._bm25_chunks[idx],
                "bm25_score": float(score),
                "_index": idx,
            })

        scored_chunks.sort(key=lambda x: x["bm25_score"], reverse=True)
        return scored_chunks[:top_k]

    def _dense_search(
        self,
        query: str,
        top_k: int = 20,
        filter_dict: Optional[dict] = None,
    ) -> List[dict]:
        """
        Performs dense vector search via Qdrant.
        """
        query_vector = self.embedder.encode_query(query)
        results = self.vector_db.search(
            query_vector=query_vector,
            top_k=top_k,
            filter_dict=filter_dict,
        )
        return results

    def search(
        self,
        query: str,
        top_k: int = None,
        filter_dict: Optional[dict] = None,
        rrf_k: int = 60,
    ) -> List[dict]:
        """
        Performs hybrid search combining BM25 and dense vectors using RRF fusion.
        """
        if top_k is None:
            top_k = config.retrieval_top_k

        dense_results = self._dense_search(query, top_k=top_k, filter_dict=filter_dict)
        bm25_results = self._bm25_search(query, top_k=top_k)

        rrf_scores = {}

        for rank, result in enumerate(dense_results):
            chunk_id = result["chunk_id"]
            if chunk_id not in rrf_scores:
                rrf_scores[chunk_id] = {
                    "chunk_id": chunk_id,
                    "text": result["text"],
                    "metadata": result.get("metadata", {}),
                    "dense_score": result["score"],
                    "bm25_score": 0.0,
                }
            rrf_scores[chunk_id]["rrf_score"] = 1.0 / (rrf_k + rank + 1)

        for rank, result in enumerate(bm25_results):
            chunk_id = result["chunk_id"]
            if chunk_id in rrf_scores:
                rrf_scores[chunk_id]["bm25_score"] = result["bm25_score"]
                rrf_scores[chunk_id]["rrf_score"] += 1.0 / (rrf_k + rank + 1)
            else:
                rrf_scores[chunk_id] = {
                    "chunk_id": chunk_id,
                    "text": result["text"],
                    "metadata": result.get("metadata", {}),
                    "dense_score": 0.0,
                    "bm25_score": result["bm25_score"],
                    "rrf_score": 1.0 / (rrf_k + rank + 1),
                }

        merged_results = sorted(
            rrf_scores.values(),
            key=lambda x: x["rrf_score"],
            reverse=True,
        )

        return merged_results[:top_k]
