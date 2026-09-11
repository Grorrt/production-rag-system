"""
Qdrant vector database integration for storing and searching document embeddings.
Handles collection creation, upserting vectors, and similarity search.
"""

from typing import List, Optional

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    HnswConfigDiff,
    ScalarQuantization,
    ScalarQuantizationConfig,
    SearchParams,
    QuantizationSearchParams,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)

from backend.app.configuration.app_config import config


class VectorDatabase:
    """
    Manages the Qdrant vector store for document chunks.
    Supports both remote Qdrant server and in-memory mode for local dev.
    Handles collection lifecycle and vector search operations.
    """

    def __init__(self):
        self.is_in_memory = config.qdrant_host.lower() == ":memory:"

        if self.is_in_memory:
            self.client = QdrantClient(location=":memory:")
        elif config.qdrant_api_key:
            self.client = QdrantClient(
                url=config.qdrant_host,
                api_key=config.qdrant_api_key,
            )
        else:
            self.client = QdrantClient(
                host=config.qdrant_host,
                port=config.qdrant_port,
            )
        self.collection_name = config.qdrant_collection
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        """Creates the collection with proper configuration if it does not exist."""
        collections = self.client.get_collections().collections
        existing = [c.name for c in collections]

        if self.collection_name not in existing:
            vector_params = VectorParams(
                size=config.embedding_dimension,
                distance=Distance.COSINE,
            )
            if not self.is_in_memory:
                vector_params.on_disk = True

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=vector_params,
                hnsw_config=HnswConfigDiff(
                    m=16,
                    ef_construct=200,
                    full_scan_threshold=10000,
                ),
                quantization_config=ScalarQuantization(
                    scalar=ScalarQuantizationConfig(
                        type="int8",
                        quantile=0.99,
                        always_ram=False,
                    )
                ),
            )

    def upsert_chunks(self, chunks: List[dict], embeddings: List[List[float]]):
        """
        Inserts or updates chunks with their embeddings in Qdrant.
        """
        points = []
        for chunk, embedding in zip(chunks, embeddings):
            point = PointStruct(
                id=hash(chunk["chunk_id"]) % (2**63),
                vector=embedding,
                payload={
                    "chunk_id": chunk["chunk_id"],
                    "text": chunk["text"],
                    **chunk["metadata"],
                },
            )
            points.append(point)

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
            wait=True,
        )

        return len(points)

    def search(
        self,
        query_vector: List[float],
        top_k: int = 20,
        filter_dict: Optional[dict] = None,
    ) -> List[dict]:
        """
        Searches for the most similar chunks to the query vector.
        Returns list of chunks with scores and metadata.
        """
        search_filter = None
        if filter_dict:
            conditions = []
            for key, value in filter_dict.items():
                conditions.append(
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=value),
                    )
                )
            if conditions:
                search_filter = Filter(must=conditions)

        response = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=top_k,
            query_filter=search_filter,
            search_params=SearchParams(
                quantization=QuantizationSearchParams(
                    ignore=False,
                    rescore=True,
                ),
            ),
            with_payload=True,
        )

        formatted_results = []
        for point in response.points:
            formatted_results.append({
                "chunk_id": point.payload.get("chunk_id"),
                "text": point.payload.get("text", ""),
                "score": point.score,
                "metadata": {
                    k: v for k, v in point.payload.items()
                    if k not in ("chunk_id", "text")
                },
            })

        return formatted_results

    def delete_document(self, document_id: str):
        """Deletes all chunks associated with a document."""
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(value=document_id),
                    )
                ]
            ),
        )

    def count_points(self) -> int:
        """Returns the total number of chunks stored."""
        result = self.client.count(
            collection_name=self.collection_name,
            exact=True,
        )
        return result.count

    def health_check(self) -> bool:
        """Checks if the Qdrant server is reachable."""
        try:
            self.client.get_collections()
            return True
        except Exception:
            return False
