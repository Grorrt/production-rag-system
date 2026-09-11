from typing import List, Optional, Tuple

from backend.app.configuration.app_config import config


class ResultRanker:
    """
    Re-ranks retrieved chunks using a cross-encoder model via transformers.
    Falls back gracefully if the model cannot be loaded (e.g., OOM on free tier).
    """

    def __init__(self):
        self.model_name = config.reranker_model
        self._tokenizer = None
        self._model = None
        self._available = True

    def _load_model(self) -> bool:
        try:
            from transformers import AutoModelForSequenceClassification, AutoTokenizer
            self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self._model = AutoModelForSequenceClassification.from_pretrained(
                self.model_name,
                torch_dtype="auto",
            )
            return True
        except Exception:
            self._available = False
            return False

    def rerank(
        self,
        query: str,
        chunks: List[dict],
        top_k: int = None,
    ) -> List[dict]:
        if not chunks:
            return []

        if not self._available:
            return chunks[:top_k] if top_k else chunks

        if self._model is None:
            if not self._load_model():
                return chunks[:top_k] if top_k else chunks

        try:
            if top_k is None:
                top_k = config.reranker_top_k

            tokenizer, model = self._tokenizer, self._model
            pairs = [[query, chunk["text"]] for chunk in chunks]
            inputs = tokenizer(
                pairs,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors="pt",
            )
            outputs = model(**inputs)
            scores = outputs.logits.squeeze(-1).detach().numpy()

            scored_chunks = []
            for chunk, score in zip(chunks, scores):
                scored_chunks.append({**chunk, "reranker_score": float(score)})

            scored_chunks.sort(key=lambda x: x["reranker_score"], reverse=True)
            return scored_chunks[:top_k]
        except Exception:
            return chunks[:top_k] if top_k else chunks
