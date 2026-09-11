"""
Splits documents into smaller chunks for embedding and retrieval.
Uses recursive character splitting with semantic boundary awareness.
"""

from typing import List

from backend.app.rag_pipeline.document_processing.document_loader import Document


class RecursiveCharacterTextSplitter:
    """
    Custom recursive character text splitter.
    Splits text at sensible boundaries: paragraphs, sentences, then words.
    Avoids dependency on langchain text splitters which can cause import issues.
    """

    def __init__(
        self,
        chunk_size: int = 512,
        chunk_overlap: int = 50,
        separators=None,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n\n", "\n\n", "\n", ". ", " ", ""]

    def split_text(self, text: str) -> List[str]:
        if not text:
            return []

        chunks = []
        current_chunk = ""
        paragraphs = self._split_with_separators(text, self.separators)

        for para in paragraphs:
            if len(current_chunk) + len(para) <= self.chunk_size:
                current_chunk += para
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())

                overlap_start = max(0, len(current_chunk) - self.chunk_overlap)
                current_chunk = current_chunk[overlap_start:] + para

                if len(current_chunk) > self.chunk_size * 1.5:
                    for line in current_chunk.split("\n"):
                        for part in self._split_if_needed(line, self.chunk_size):
                            chunks.append(part.strip())
                    current_chunk = ""

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks or [text.strip()]

    def _split_with_separators(self, text: str, separators: List[str]) -> List[str]:
        result = [text]

        for sep in separators:
            if sep == "":
                break

            new_result = []
            for segment in result:
                split_parts = segment.split(sep)
                for i, part in enumerate(split_parts):
                    if part:
                        new_result.append(part)
                    if i < len(split_parts) - 1 and sep:
                        new_result.append(sep)
            result = new_result

            if len(result) > 1:
                break

        return result

    def _split_if_needed(self, text: str, max_length: int) -> List[str]:
        if len(text) <= max_length:
            return [text]

        parts = []
        for i in range(0, len(text), max_length):
            parts.append(text[i : i + max_length])
        return parts


class TextSplitter:
    """
    Splits extracted documents into overlapping chunks optimized for retrieval.
    Two-stage strategy:
      1. Recursive split on sensible boundaries (paragraphs, sentences)
      2. Each chunk is enriched with its position and source metadata.
    """

    def __init__(
        self,
        chunk_size: int = 512,
        chunk_overlap: int = 50,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n\n", "\n\n", "\n", ". ", " ", ""],
        )

    def split_documents(self, documents: List[Document]) -> List[dict]:
        """
        Splits a list of documents into chunks.
        Each chunk is a dictionary with text, metadata, and a unique chunk ID.
        """
        all_chunks = []

        for doc in documents:
            chunks = self.splitter.split_text(doc.text)

            for chunk_index, chunk_text in enumerate(chunks):
                chunk_id = f"{doc.document_id}_{chunk_index}"

                chunk_data = {
                    "chunk_id": chunk_id,
                    "text": chunk_text.strip(),
                    "metadata": {
                        **doc.metadata,
                        "chunk_index": chunk_index,
                        "total_chunks": len(chunks),
                        "document_id": doc.document_id,
                    },
                }

                all_chunks.append(chunk_data)

        return all_chunks

    def split_text(self, text: str, source: str = None) -> List[dict]:
        """
        Convenience method to split raw text directly.
        """
        chunks = self.splitter.split_text(text)
        result = []

        for i, chunk_text in enumerate(chunks):
            result.append({
                "chunk_id": f"{source or 'text'}_{i}",
                "text": chunk_text.strip(),
                "metadata": {
                    "source": source or "raw_text",
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                },
            })

        return result
