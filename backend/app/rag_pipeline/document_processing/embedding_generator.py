import hashlib
from pathlib import Path
from typing import List

import diskcache

from backend.app.configuration.app_config import config


class EmbeddingGenerator:
    """
    Converts text chunks into dense vector embeddings using fastembed (ONNX).
    Uses BAAI/bge-base-en-v1.5 and caches results on disk.
    """

    def __init__(self):
        self.model_name = config.embedding_model
        self.dimension = config.embedding_dimension
        self._model = None

        cache_path = Path(config.cache_dir) / "embeddings"
        cache_path.mkdir(parents=True, exist_ok=True)
        self.cache = diskcache.Cache(str(cache_path))

    @property
    def model(self):
        if self._model is None:
            from fastembed import TextEmbedding
            self._model = TextEmbedding(model_name=self.model_name)
        return self._model

    def _text_hash(self, text: str) -> str:
        return hashlib.sha256(text.encode()).hexdigest()

    def encode(self, texts: List[str]) -> List[List[float]]:
        uncached_texts = []
        uncached_indices = []

        for i, text in enumerate(texts):
            text_hash = self._text_hash(text)
            cached = self.cache.get(text_hash)
            if cached is not None:
                texts[i] = cached
            else:
                uncached_texts.append(text)
                uncached_indices.append(i)

        if uncached_texts:
            new_embeddings = list(self.model.embed(uncached_texts))

            for idx, emb in zip(uncached_indices, new_embeddings):
                text_hash = self._text_hash(uncached_texts[uncached_indices.index(idx)])
                self.cache.set(text_hash, emb.tolist())
                texts[idx] = emb.tolist()

        return texts

    def encode_query(self, query: str) -> List[float]:
        embedding = list(self.model.query_embed(query))
        return embedding[0].tolist()

    @property
    def embedding_dimension(self) -> int:
        return self.dimension
