"""
Document loaders for PDF, HTML, Markdown, and plain text files.
Each loader extracts text content and metadata from its source format.
"""

import hashlib
from pathlib import Path
from typing import List, Optional

import fitz
from bs4 import BeautifulSoup


class Document:
    """
    Represents a single extracted document with its text content and metadata.
    """

    def __init__(
        self,
        text: str,
        metadata: dict,
        document_id: str = None,
    ):
        self.text = text
        self.metadata = metadata
        self.document_id = document_id or hashlib.md5(text.encode()).hexdigest()[:12]

    def __repr__(self):
        return f"Document(id={self.document_id}, source={self.metadata.get('source', 'unknown')})"


class PdfLoader:
    """Loads text content from PDF files using PyMuPDF."""

    def load(self, file_path: str) -> List[Document]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        documents = []
        doc = fitz.open(file_path)

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text().strip()

            if not text:
                continue

            metadata = {
                "source": str(path),
                "file_name": path.name,
                "file_type": "pdf",
                "page_number": page_num + 1,
                "total_pages": len(doc),
            }

            documents.append(Document(text=text, metadata=metadata))

        doc.close()
        return documents


class HtmlLoader:
    """Loads text content from HTML files using BeautifulSoup."""

    def load(self, file_path: str) -> List[Document]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"HTML file not found: {file_path}")

        with open(file_path, encoding="utf-8") as file:
            soup = BeautifulSoup(file.read(), "html.parser")

        title = soup.title.string if soup.title else path.stem
        body = soup.body

        text_parts = []
        for element in body.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "pre", "code"]):
            tag = element.name
            text = element.get_text(strip=True)
            if text:
                if tag.startswith("h"):
                    prefix = "#" * int(tag[1])
                    text_parts.append(f"{prefix} {text}")
                elif tag == "li":
                    text_parts.append(f"- {text}")
                elif tag in ("pre", "code"):
                    text_parts.append(f"```\n{text}\n```")
                else:
                    text_parts.append(text)

        metadata = {
            "source": str(path),
            "file_name": path.name,
            "file_type": "html",
            "title": title,
        }

        return [Document(text="\n\n".join(text_parts), metadata=metadata)]


class MarkdownLoader:
    """Loads text content from Markdown files."""

    def load(self, file_path: str) -> List[Document]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Markdown file not found: {file_path}")

        with open(file_path, encoding="utf-8") as file:
            text = file.read()

        metadata = {
            "source": str(path),
            "file_name": path.name,
            "file_type": "markdown",
        }

        return [Document(text=text, metadata=metadata)]


class TextLoader:
    """Loads text content from plain text files."""

    def load(self, file_path: str) -> List[Document]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Text file not found: {file_path}")

        with open(file_path, encoding="utf-8") as file:
            text = file.read()

        metadata = {
            "source": str(path),
            "file_name": path.name,
            "file_type": "text",
        }

        return [Document(text=text, metadata=metadata)]


class DocumentLoaderFactory:
    """
    Factory that selects the appropriate loader based on file extension.
    """

    _loaders = {
        ".pdf": PdfLoader(),
        ".html": HtmlLoader(),
        ".htm": HtmlLoader(),
        ".md": MarkdownLoader(),
        ".mdx": MarkdownLoader(),
        ".txt": TextLoader(),
    }

    @classmethod
    def get_loader(cls, file_path: str):
        extension = Path(file_path).suffix.lower()
        loader = cls._loaders.get(extension)

        if loader is None:
            supported = ", ".join(cls._loaders.keys())
            raise ValueError(
                f"Unsupported file type: {extension}. Supported types: {supported}"
            )

        return loader

    @classmethod
    def load_document(cls, file_path: str) -> List[Document]:
        loader = cls.get_loader(file_path)
        return loader.load(file_path)
