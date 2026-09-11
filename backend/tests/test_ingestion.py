"""
Tests for the document ingestion pipeline.
"""

import pytest
from backend.app.rag_pipeline.document_processing.document_loader import (
    DocumentLoaderFactory,
    PdfLoader,
    TextLoader,
    MarkdownLoader,
)


class TestDocumentLoader:
    def test_pdf_loader_creates_documents(self, sample_pdf_path):
        docs = PdfLoader().load(sample_pdf_path)
        assert len(docs) > 0
        assert all(doc.text for doc in docs)
        assert all(doc.metadata.get("file_type") == "pdf" for doc in docs)

    def test_text_loader_creates_documents(self, sample_text_path):
        docs = TextLoader().load(sample_text_path)
        assert len(docs) == 1
        assert "useEffect" in docs[0].text

    def test_factory_selects_correct_loader(self):
        loader = DocumentLoaderFactory.get_loader("test.pdf")
        assert isinstance(loader, PdfLoader)

        loader = DocumentLoaderFactory.get_loader("test.txt")
        assert isinstance(loader, TextLoader)

        loader = DocumentLoaderFactory.get_loader("test.md")
        assert isinstance(loader, MarkdownLoader)

    def test_factory_rejects_unsupported_format(self):
        with pytest.raises(ValueError, match="Unsupported file type"):
            DocumentLoaderFactory.get_loader("test.doc")

    def test_factory_loads_document(self, sample_pdf_path):
        docs = DocumentLoaderFactory.load_document(sample_pdf_path)
        assert len(docs) > 0
        assert "routing" in docs[0].text.lower()


class TestTextSplitter:
    def test_splitter_creates_chunks(self):
        from backend.app.rag_pipeline.document_processing.text_splitter import TextSplitter
        splitter = TextSplitter(chunk_size=100, chunk_overlap=10)

        text = "A. " * 200
        chunks = splitter.split_text(text, source="test")

        assert len(chunks) > 1
        assert all("chunk_id" in c for c in chunks)
        assert all("text" in c for c in chunks)
        assert all("metadata" in c for c in chunks)

    def test_splitter_preserves_metadata(self):
        from backend.app.rag_pipeline.document_processing.text_splitter import TextSplitter
        from backend.app.rag_pipeline.document_processing.document_loader import Document

        splitter = TextSplitter()
        doc = Document(
            text="Hello world. " * 100,
            metadata={"source": "test.md", "file_name": "test.md"},
        )

        chunks = splitter.split_documents([doc])
        assert all(c["metadata"]["source"] == "test.md" for c in chunks)
