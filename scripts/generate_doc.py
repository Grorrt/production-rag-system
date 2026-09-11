#!/usr/bin/env python3
"""
Production-Grade RAG System — Professional PDF Documentation Generator
"""

from fpdf import FPDF
import os
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "docs")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "Production_RAG_System_Documentation.pdf")

FONT_DIR = "C:/Windows/Fonts"

COLOR_PRIMARY = (25, 55, 109)      # Dark navy blue
COLOR_SECONDARY = (0, 105, 180)    # Medium blue
COLOR_ACCENT = (220, 235, 250)     # Light blue background
COLOR_TEXT = (33, 33, 33)          # Dark gray
COLOR_TEXT_LIGHT = (100, 100, 100) # Gray
COLOR_WHITE = (255, 255, 255)
COLOR_DIVIDER = (200, 200, 200)


class RAGDocumentPDF(FPDF):
    """Custom PDF class for RAG System Documentation"""

    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=25)
        self.section_number = 0
        self.sub_section_number = 0
        self.in_toc = False
        self.toc_entries = []

        # Register fonts
        self.add_font("Arial", "", os.path.join(FONT_DIR, "arial.ttf"))
        self.add_font("Arial", "B", os.path.join(FONT_DIR, "arialbd.ttf"))
        self.add_font("Arial", "I", os.path.join(FONT_DIR, "ariali.ttf"))
        self.add_font("Arial", "BI", os.path.join(FONT_DIR, "arialbi.ttf"))
        self.add_font("Courier", "", os.path.join(FONT_DIR, "cour.ttf"))
        self.add_font("Courier", "B", os.path.join(FONT_DIR, "courbd.ttf"))

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Arial", "I", 8)
        self.set_text_color(*COLOR_TEXT_LIGHT)
        self.cell(0, 6, "Production-Grade RAG System — Technical Documentation", align="L")
        self.cell(0, 6, f"Page {self.page_no()}", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*COLOR_DIVIDER)
        self.line(10, 14, 200, 14)
        self.ln(4)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-15)
        self.set_font("Arial", "I", 7)
        self.set_text_color(*COLOR_TEXT_LIGHT)
        self.cell(0, 10, f"Confidential — {datetime.now().strftime('%Y')}", align="C")

    def cover_page(self):
        self.add_page()
        self.ln(50)
        # Top accent line
        self.set_fill_color(*COLOR_SECONDARY)
        self.rect(10, 40, 190, 3, "F")
        self.ln(15)

        # Title
        self.set_font("Arial", "B", 28)
        self.set_text_color(*COLOR_PRIMARY)
        self.multi_cell(0, 14, "Production-Grade\nRetrieval-Augmented Generation\n(RAG) System", align="C")
        self.ln(6)

        # Subtitle
        self.set_font("Arial", "", 16)
        self.set_text_color(*COLOR_SECONDARY)
        self.multi_cell(0, 10, "Technical Documentation & Architecture Guide", align="C")
        self.ln(12)

        # Accent line
        self.set_fill_color(*COLOR_SECONDARY)
        self.rect(60, self.get_y(), 90, 1.5, "F")
        self.ln(15)

        # Tagline
        self.set_font("Arial", "I", 12)
        self.set_text_color(*COLOR_TEXT_LIGHT)
        self.multi_cell(0, 8, "Building Trustworthy AI Systems with Evidence-Based Answers", align="C")
        self.ln(30)

        # Key info box
        self.set_fill_color(*COLOR_ACCENT)
        self.set_draw_color(*COLOR_SECONDARY)
        x = 35
        y = self.get_y()
        w = 140
        h = 55
        self.rect(x, y, w, h, "DF")

        info_items = [
            ("Document Version", "1.0.0"),
            ("Date", datetime.now().strftime("%B %d, %Y")),
            ("Author", "AI Engineering Team"),
            ("Classification", "Technical Reference"),
        ]
        self.set_text_color(*COLOR_TEXT)
        y_start = y + 6
        for i, (label, value) in enumerate(info_items):
            self.set_xy(x + 8, y_start + i * 11)
            self.set_font("Arial", "B", 10)
            self.cell(50, 7, label)
            self.set_font("Arial", "", 10)
            self.cell(70, 7, value)

        self.ln(80)

        # Bottom note
        self.set_font("Arial", "I", 9)
        self.set_text_color(*COLOR_TEXT_LIGHT)
        self.multi_cell(0, 6, "This document provides a comprehensive overview of the Production-Grade RAG System,\nincluding architecture, components, data flow, and implementation strategy.", align="C")

    def section_title(self, title):
        self.section_number += 1
        self.sub_section_number = 0
        self.ln(4)
        # Section accent bar
        self.set_fill_color(*COLOR_SECONDARY)
        self.rect(10, self.get_y(), 4, 10, "F")
        self.set_x(18)
        self.set_font("Arial", "B", 16)
        self.set_text_color(*COLOR_PRIMARY)
        self.cell(0, 10, f"{self.section_number}. {title}", new_x="LMARGIN", new_y="NEXT")
        self.ln(3)
        # Divider
        self.set_draw_color(*COLOR_DIVIDER)
        self.line(18, self.get_y(), 200, self.get_y())
        self.ln(4)

        # TOC tracking
        if hasattr(self, "_toc_active") and self._toc_active:
            self.toc_entries.append((1, self.section_number, title, self.page_no()))

    def sub_section_title(self, title):
        self.sub_section_number += 1
        self.ln(2)
        self.set_font("Arial", "B", 13)
        self.set_text_color(*COLOR_SECONDARY)
        self.cell(0, 8, f"{self.section_number}.{self.sub_section_number}  {title}", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

        if hasattr(self, "_toc_active") and self._toc_active:
            self.toc_entries.append((2, f"{self.section_number}.{self.sub_section_number}", title, self.page_no()))

    def sub_sub_section(self, title):
        self.ln(1)
        self.set_font("Arial", "B", 11)
        self.set_text_color(*COLOR_PRIMARY)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text):
        self.set_font("Arial", "", 10.5)
        self.set_text_color(*COLOR_TEXT)
        self.multi_cell(0, 5.8, text, align="J")
        self.ln(2)

    def bullet_point(self, text, indent=10):
        x0 = self.get_x()
        self.set_x(x0 + indent)
        self.set_font("Arial", "", 10.5)
        self.set_text_color(*COLOR_TEXT)
        bullet_char = "\u2022"
        self.cell(5, 5.8, bullet_char)
        self.multi_cell(0, 5.8, text, align="J")
        self.ln(1)

    def bold_bullet(self, bold_part, normal_part, indent=10):
        x0 = self.get_x()
        self.set_x(x0 + indent)
        self.set_font("Arial", "", 10.5)
        self.set_text_color(*COLOR_TEXT)
        self.cell(5, 5.8, "\u2022")
        self.set_font("Arial", "B", 10.5)
        self.write(5.8, bold_part)
        self.set_font("Arial", "", 10.5)
        self.write(5.8, " " + normal_part)
        self.ln(5.8)
        self.ln(1)

    def info_box(self, title, content):
        self.ln(2)
        self.set_fill_color(*COLOR_ACCENT)
        self.set_draw_color(*COLOR_SECONDARY)
        y_start = self.get_y()
        self.set_x(15)
        self.rect(15, y_start, 180, 20, "DF")
        self.set_xy(18, y_start + 3)
        self.set_font("Arial", "B", 10)
        self.set_text_color(*COLOR_PRIMARY)
        self.multi_cell(174, 6, f"{title}: {content}")
        self.set_y(y_start + 24)
        self.ln(2)

    def tech_spec(self, label, value):
        self.set_x(20)
        self.set_font("Arial", "B", 10)
        self.set_text_color(*COLOR_PRIMARY)
        self.cell(50, 6, label)
        self.set_font("Arial", "", 10)
        self.set_text_color(*COLOR_TEXT)
        self.cell(0, 6, value, new_x="LMARGIN", new_y="NEXT")
        self.ln(0.5)

    def table_of_contents(self):
        self.add_page()
        self._toc_active = True
        self.set_font("Arial", "B", 20)
        self.set_text_color(*COLOR_PRIMARY)
        self.cell(0, 12, "Table of Contents", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*COLOR_SECONDARY)
        self.line(10, self.get_y() + 2, 200, self.get_y() + 2)
        self.ln(8)

    def render_toc(self):
        self._toc_active = False
        # We need a second pass — store pages
        # For now, just add pages at end (we'll finalize in post-processing)

    def add_toc_entries(self):
        """Add TOC entries (called after all content)"""
        pass

    def number_line(self, num, text):
        self.set_font("Arial", "", 10.5)
        self.set_text_color(*COLOR_TEXT)
        self.cell(8, 5.8, f"{num}.")
        self.multi_cell(0, 5.8, text, align="J")
        self.ln(1)

    def table_row(self, cells, widths, bold=False, fill=False):
        style = "B" if bold else ""
        self.set_font("Arial", style, 9)
        max_h = 6
        if fill:
            self.set_fill_color(*COLOR_ACCENT)
        else:
            self.set_fill_color(*COLOR_WHITE)
        self.set_text_color(*COLOR_TEXT)
        for i, cell_text in enumerate(cells):
            self.cell(widths[i], max_h, cell_text, border=1, fill=True)
        self.ln(max_h)

    def draw_table(self, headers, data, col_widths):
        # Header row
        self.set_font("Arial", "B", 9)
        self.set_fill_color(*COLOR_PRIMARY)
        self.set_text_color(*COLOR_WHITE)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, h, border=1, fill=True, align="C")
        self.ln()

        # Data rows
        for row in data:
            self.set_font("Arial", "", 9)
            self.set_text_color(*COLOR_TEXT)
            max_lines = 1
            # Calculate max height needed
            for i, cell_text in enumerate(row):
                lines = self.multi_cell(col_widths[i], 5, cell_text, dry_run=True, output="LINES")
                max_lines = max(max_lines, len(lines))

            row_h = max(6, max_lines * 5)
            y_before = self.get_y()

            # Check page break
            if y_before + row_h > 270:
                self.add_page()
                # Repeat header
                self.set_font("Arial", "B", 9)
                self.set_fill_color(*COLOR_PRIMARY)
                self.set_text_color(*COLOR_WHITE)
                for i, h in enumerate(headers):
                    self.cell(col_widths[i], 7, h, border=1, fill=True, align="C")
                self.ln()
                y_before = self.get_y()

            x_start = self.get_x()
            for i, cell_text in enumerate(row):
                x = x_start + sum(col_widths[:i])
                self.set_xy(x, y_before)
                self.set_font("Arial", "", 9)
                # Draw cell background
                self.rect(x, y_before, col_widths[i], row_h, "D")
                self.set_xy(x + 0.5, y_before + 0.5)
                self.multi_cell(col_widths[i] - 1, 5, cell_text)
            self.set_y(y_before + row_h)


def build_document():
    pdf = RAGDocumentPDF()

    # ========================================================================
    # COVER PAGE
    # ========================================================================
    pdf.cover_page()

    # ========================================================================
    # TABLE OF CONTENTS
    # ========================================================================
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(*COLOR_PRIMARY)
    pdf.cell(0, 12, "Table of Contents", new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(*COLOR_SECONDARY)
    pdf.line(10, pdf.get_y() + 2, 200, pdf.get_y() + 2)
    pdf.ln(8)

    toc_items = [
        (1, "Executive Summary", 3),
        (2, "Project Overview", 4),
        (3, "System Architecture", 5),
        (4, "Core Components", 7),
        (5, "Data Flow", 12),
        (6, "API Layer", 14),
        (7, "Frontend Application", 15),
        (8, "Evaluation Framework", 16),
        (9, "Production Deployment", 18),
        (10, "Use Cases", 20),
        (11, "Implementation Roadmap", 22),
        (12, "Success Metrics", 23),
        (13, "Conclusion", 25),
    ]

    for num, title, page in toc_items:
        pdf.set_font("Arial", "", 11)
        pdf.set_text_color(*COLOR_TEXT)
        pdf.cell(8, 8, f"{num}.")
        pdf.set_font("Arial", "B" if num < 10 else "", 11)
        pdf.cell(140, 8, title)
        pdf.set_font("Arial", "", 11)
        pdf.cell(20, 8, str(page), align="R", new_x="LMARGIN", new_y="NEXT")

    # ========================================================================
    # 1. EXECUTIVE SUMMARY
    # ========================================================================
    pdf.section_title("Executive Summary")

    pdf.body_text(
        "The Production-Grade Retrieval-Augmented Generation (RAG) System is a comprehensive enterprise-grade "
        "solution designed to deliver accurate, evidence-based answers from an organization's private knowledge base. "
        "Unlike traditional chatbots that rely solely on a language model's parametric knowledge, this system "
        "retrieves relevant information from ingested documents and generates responses grounded in verifiable sources."
    )

    pdf.body_text(
        "The system addresses a critical challenge in enterprise AI adoption: hallucination. By combining dense "
        "vector retrieval with sparse keyword search (BM25), re-ranking with cross-encoders, and a sophisticated "
        "LangGraph workflow, the system ensures that every answer is traceable to specific source documents. "
        "Each response includes inline citations, allowing users to verify the accuracy of the information."
    )

    pdf.info_box(
        "Core Philosophy",
        "Every answer must be backed by evidence. No hallucination. No guessing. Every claim traceable "
        "to a source document with a verifiable citation."
    )

    pdf.sub_section_title("Key Capabilities")
    pdf.bold_bullet("Document Ingestion Pipeline — ", "Process PDFs, HTML pages, Markdown files, and web content with automated chunking and metadata extraction.")
    pdf.bold_bullet("Hybrid Search (BM25 + Dense Vectors) — ", "Combines lexical keyword matching with semantic similarity using Reciprocal Rank Fusion (RRF) for optimal retrieval.")
    pdf.bold_bullet("Cross-Encoder Re-Ranking — ", "A second-stage re-ranker (BAAI/bge-reranker-v2-m3) scores retrieved chunks for maximum precision.")
    pdf.bold_bullet("LangGraph Workflow — ", "State machine orchestrates query transformation, retrieval, re-ranking, generation, hallucination checking, and citation formatting.")
    pdf.bold_bullet("Citation System — ", "Every answer segment is linked to its source document with page numbers and direct references.")
    pdf.bold_bullet("Evaluation Suite — ", "Automated metrics (Recall@k, MRR, Faithfulness, Answer Relevance) with RAGAS framework integration.")
    pdf.bold_bullet("Production Infrastructure — ", "Docker Compose orchestration, JWT authentication, Langfuse monitoring, structured logging, and CI/CD pipelines.")

    # ========================================================================
    # 2. PROJECT OVERVIEW
    # ========================================================================
    pdf.section_title("Project Overview")

    pdf.sub_section_title("What is Retrieval-Augmented Generation?")
    pdf.body_text(
        "Retrieval-Augmented Generation (RAG) is an AI architecture that enhances large language models with "
        "external knowledge retrieval. Instead of generating answers from the model's training data alone, RAG "
        "first searches a knowledge base for relevant information, then provides this context to the LLM for "
        "answer generation. This approach significantly reduces hallucination, enables answers from private "
        "or proprietary data, and allows for real-time knowledge updates without model retraining."
    )

    pdf.sub_section_title("System Design Philosophy")
    pdf.body_text(
        "This system is built on five core design principles:"
    )
    pdf.number_line(1, "Accuracy First — Every component is optimized for retrieval precision and answer faithfulness.")
    pdf.number_line(2, "Traceability — All answers must include verifiable citations to source documents.")
    pdf.number_line(3, "Scalability — Containerized microservices architecture that scales horizontally.")
    pdf.number_line(4, "Observability — Full monitoring, tracing, and logging with Langfuse integration.")
    pdf.number_line(5, "Cost Efficiency — Local embedding model (BGE-base-en-v1.5) and local LLM (Qwen3 8B) eliminate API costs.")

    pdf.sub_section_title("Target Audience")
    pdf.bold_bullet("Organizations — ", "Companies needing to make their internal documentation searchable and answerable.")
    pdf.bold_bullet("Developers — ", "Teams building knowledge-base assistants, customer support bots, or document Q&A systems.")
    pdf.bold_bullet("Researchers — ", "Academics and analysts needing to query large collections of research papers.")
    pdf.bold_bullet("Enterprises — ", "Legal, healthcare, and finance sectors requiring citation-backed answers.")

    # ========================================================================
    # 3. SYSTEM ARCHITECTURE
    # ========================================================================
    pdf.section_title("System Architecture")

    pdf.body_text(
        "The system follows a layered microservices architecture with clear separation of concerns. "
        "Each component is containerized and independently scalable. The architecture is designed for "
        "production deployments with authentication, monitoring, and CI/CD integration."
    )

    pdf.sub_section_title("High-Level Architecture")

    # Text-based architecture diagram using table
    headers = ["Layer", "Component", "Technology", "Responsibility"]
    col_widths = [30, 45, 50, 65]
    data = [
        ["Presentation", "React Frontend", "React + TypeScript + TailwindCSS", "Chat UI, document upload, citation display"],
        ["API Gateway", "FastAPI Server", "FastAPI + OAuth2 + Structlog", "Authentication, routing, request validation"],
        ["Orchestration", "LangGraph Workflow", "LangChain + LangGraph", "Query processing, retrieval, generation flow"],
        ["Retrieval", "Hybrid Search", "Qdrant + BM25 (rank-bm25)", "Dense vector + sparse keyword search"],
        ["Retrieval", "Re-ranker", "BAAI/bge-reranker-v2-m3", "Cross-encoder precision scoring"],
        ["Embeddings", "Embedding Service", "BGE-base-en-v1.5 + sentence-transformers", "Document and query vectorization"],
        ["Generation", "LLM Engine", "Qwen3 8B via Ollama", "Context-grounded answer generation"],
        ["Monitoring", "Observability", "Langfuse + Prometheus + Grafana", "Tracing, metrics, cost tracking"],
        ["Infrastructure", "Container Orchestration", "Docker Compose", "Service management, networking, volumes"],
    ]
    pdf.draw_table(headers, data, col_widths)

    pdf.ln(4)
    pdf.sub_section_title("Technology Stack Summary")

    tech_data = [
        ["Backend Language", "Python 3.12+"],
        ["Web Framework", "FastAPI (async)"],
        ["RAG Framework", "LangChain + LangGraph"],
        ["Vector Database", "Qdrant (self-hosted)"],
        ["Embedding Model", "BAAI/bge-base-en-v1.5 (768 dimensions)"],
        ["Large Language Model", "Qwen3 8B (via Ollama)"],
        ["Re-ranker Model", "BAAI/bge-reranker-v2-m3"],
        ["Hybrid Search", "BM25 + Dense Vector (RRF fusion)"],
        ["Frontend", "React 18 + TypeScript + TailwindCSS"],
        ["Monitoring", "Langfuse (LLM observability)"],
        ["Evaluation", "RAGAS (automated metrics)"],
        ["Authentication", "JWT-based OAuth2"],
        ["Testing", "pytest + pytest-cov"],
        ["CI/CD", "GitHub Actions"],
        ["Containerization", "Docker + Docker Compose"],
        ["Logging", "Structlog (structured logging)"],
    ]
    cols = [50, 90]
    pdf.set_font("Arial", "B", 9)
    pdf.set_fill_color(*COLOR_PRIMARY)
    pdf.set_text_color(*COLOR_WHITE)
    pdf.cell(cols[0], 7, "Component", border=1, fill=True)
    pdf.cell(cols[1], 7, "Technology Choice", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*COLOR_TEXT)
    for label, value in tech_data:
        pdf.set_font("Arial", "B", 9)
        pdf.cell(cols[0], 6, label, border=1)
        pdf.set_font("Arial", "", 9)
        pdf.cell(cols[1], 6, value, border=1, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(4)
    pdf.sub_section_title("Architecture Diagram")
    pdf.body_text(
        "The following diagram illustrates the request flow from user query to generated response:"
    )

    # ASCII-style flow diagram
    flow_lines = [
        "  +--------+     +--------+     +------------+     +------------+",
        "  | React  | --> | FastAPI | --> | LangGraph  | --> | Query      |",
        "  | UI     |     | Gateway |     | Workflow   |     | Transform  |",
        "  +--------+     +--------+     +------------+     +------------+",
        "                                                     |",
        "                                                     v",
        "  +--------+     +--------+     +------------+     +------------+",
        "  | Qwen3  | <-- | Re-     | <-- | Hybrid     | <-- | Vector     |",
        "  | LLM    |     | ranker  |     | Search     |     | + BM25     |",
        "  +--------+     +--------+     +------------+     +------------+",
        "                                                     |",
        "                                                     v",
        "  +--------+     +--------+     +------------+",
        "  | Citation| --> | Langfuse| --> | Response   |",
        "  | System |     | Monitor |     | to User    |",
        "  +--------+     +--------+     +------------+",
    ]
    pdf.set_font("Courier", "", 7)
    for line in flow_lines:
        pdf.cell(0, 3.5, line, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # ========================================================================
    # 4. CORE COMPONENTS
    # ========================================================================
    pdf.section_title("Core Components")

    # --- 4.1 ---
    pdf.sub_section_title("Document Ingestion Pipeline")
    pdf.body_text(
        "The ingestion pipeline is responsible for loading documents from various sources, extracting text content, "
        "splitting them into semantically meaningful chunks, generating embeddings, and storing them in Qdrant. "
        "The pipeline supports multiple document formats and provides metadata extraction for enhanced retrieval."
    )
    pdf.sub_sub_section("Supported Document Formats")
    pdf.bold_bullet("PDF — ", "Using PyMuPDF (fitz) for text extraction with layout preservation.")
    pdf.bold_bullet("HTML — ", "BeautifulSoup-based parser for web pages with tag-aware extraction.")
    pdf.bold_bullet("Markdown — ", "Native markdown support with frontmatter metadata parsing.")
    pdf.bold_bullet("Plain Text — ", "Direct text file ingestion with encoding detection.")

    pdf.sub_sub_section("Chunking Strategy")
    pdf.body_text(
        "Documents are split using a two-stage approach. First, RecursiveCharacterTextSplitter divides the text "
        "at sensible boundaries (paragraphs, sentences, then characters). Second, a semantic splitter ensures "
        "chunks maintain topical coherence. Default configuration: chunk_size=512 tokens, chunk_overlap=50 tokens."
    )

    pdf.sub_sub_section("Metadata Extraction")
    pdf.body_text(
        "Each chunk is enriched with metadata including: document title, source URL or file path, page number, "
        "section heading hierarchy, chunk index, creation timestamp, and document type. This metadata enables "
        "fine-grained filtering during retrieval and accurate citation generation."
    )

    # --- 4.2 ---
    pdf.sub_section_title("Embedding Pipeline")
    pdf.body_text(
        "The embedding service uses the BAAI/bge-base-en-v1.5 model from the BAAI family. This model produces "
        "768-dimensional dense vectors optimized for retrieval tasks. The model is selected for its strong "
        "performance on the MTEB (Massive Text Embedding Benchmark) and its efficient inference speed."
    )

    pdf.sub_sub_section("Model Specifications")
    tech_items = [
        ("Model", "BAAI/bge-base-en-v1.5"),
        ("Dimensions", "768"),
        ("Max Sequence Length", "512 tokens"),
        ("Normalization", "L2-normalized (suitable for cosine similarity)"),
        ("Framework", "sentence-transformers"),
        ("Performance", "MTEB Average: 63.7"),
        ("Inference", "CPU-optimized, ~50 docs/sec on modern hardware"),
    ]
    for label, val in tech_items:
        pdf.tech_spec(label, val)

    pdf.ln(2)
    pdf.sub_sub_section("Caching Strategy")
    pdf.body_text(
        "Embeddings are cached on disk using a key-value store (diskcache). When a document chunk is re-ingested, "
        "its hash is computed and checked against the cache. This avoids redundant computation for unchanged "
        "documents and significantly speeds up re-indexing operations."
    )

    # --- 4.3 ---
    pdf.sub_section_title("Vector Database — Qdrant")
    pdf.body_text(
        "Qdrant serves as the primary vector store. It is an open-source, high-performance vector similarity search "
        "engine written in Rust. Qdrant is chosen for its production-grade features: filtering, payload storage, "
        "HNSW index configuration, and built-in quantization for memory efficiency."
    )

    pdf.sub_sub_section("Collection Configuration")
    pdf.bold_bullet("Vector Size — ", "768 dimensions (matching BGE-base-en-v1.5)")
    pdf.bold_bullet("Distance Metric — ", "Cosine similarity")
    pdf.bold_bullet("Index — ", "HNSW (Hierarchical Navigable Small World) with m=16 and ef_construct=200")
    pdf.bold_bullet("Quantization — ", "Scalar quantization for 4x memory reduction")
    pdf.bold_bullet("Payload — ", "Full metadata stored for filtering and citation")
    pdf.bold_bullet("Write-Ahead Log — ", "Enabled for crash recovery and durability")

    pdf.sub_sub_section("Query Process")
    pdf.body_text(
        "On query, the embedding model encodes the user question into a 768-dimensional vector. Qdrant performs "
        "a nearest neighbor search using cosine similarity with the HNSW index. The search returns the top-k "
        "most similar chunks along with their payload data. The system retrieves k=20 chunks initially, which "
        "are then filtered and re-ranked in subsequent stages."
    )

    # --- 4.4 ---
    pdf.sub_section_title("Hybrid Search (BM25 + Dense Retrieval)")
    pdf.body_text(
        "Hybrid search combines the strengths of keyword-based (lexical) search and semantic (dense) search. "
        "BM25 excels at exact keyword matching and handling rare terms, while dense retrieval captures semantic "
        "similarity even when there is no lexical overlap. The fusion of both approaches significantly improves "
        "retrieval robustness."
    )

    pdf.sub_sub_section("Reciprocal Rank Fusion (RRF)")
    pdf.body_text(
        "The results from BM25 and dense vector search are merged using the RRF algorithm. Each document receives "
        "a combined score calculated as the sum of reciprocal ranks from both result lists. The formula is: "
        "RRF(d) = 1/(k + rank_bm25(d)) + 1/(k + rank_dense(d)), where k=60 is a constant. This method produces "
        "stable, high-quality merged rankings without score normalization."
    )

    pdf.sub_sub_section("Query Transformation")
    pdf.body_text(
        "Before retrieval, the user's query undergoes transformations to improve search quality. Three techniques "
        "are applied: (1) query expansion — generating alternative phrasings using the LLM, (2) HyDE (Hypothetical "
        "Document Embeddings) — generating a hypothetical ideal document and embedding it for retrieval, and "
        "(3) multi-query search — executing multiple query variants and merging results."
    )

    # --- 4.5 ---
    pdf.sub_section_title("Re-Ranking System")
    pdf.body_text(
        "After hybrid search retrieves the top-k candidates, a cross-encoder re-ranker scores each chunk against "
        "the original query. Unlike bi-encoders (used in dense retrieval), cross-encoders process the query and "
        "chunk together through a transformer, producing a more accurate relevance score."
    )

    pdf.sub_sub_section("Re-Ranker Specifications")
    pdf.bold_bullet("Model — ", "BAAI/bge-reranker-v2-m3")
    pdf.bold_bullet("Architecture — ", "Cross-encoder (query + document processed together)")
    pdf.bold_bullet("Input — ", "Top 20 chunks from hybrid search")
    pdf.bold_bullet("Output — ", "Relevance scores 0-1, re-ranked list")
    pdf.bold_bullet("Top-k Selection — ", "Top 3-5 most relevant chunks passed to generation")

    # --- 4.6 ---
    pdf.sub_section_title("LangGraph Workflow Engine")
    pdf.body_text(
        "LangGraph is the orchestration layer that manages the entire query-to-answer pipeline as a state machine. "
        "Unlike linear chains, LangGraph supports branching, loops, conditional logic, and parallel execution. "
        "This enables sophisticated behaviors like self-correction, hallucination checking, and fallback handling."
    )

    pdf.sub_sub_section("Workflow Nodes")
    workflow_data = [
        ["query_parse", "Parse and validate user input, extract metadata filters"],
        ["query_transform", "Generate query variants and hypothetical document"],
        ["hybrid_search", "Execute BM25 + dense vector search in parallel"],
        ["re_rank", "Score and re-rank retrieved chunks"],
        ["hallucination_check", "Verify retrieved context is sufficient for answer"],
        ["generate", "Generate answer with citations using LLM"],
        ["format_response", "Structure response with citations and metadata"],
        ["log_trace", "Send trace data to Langfuse"],
    ]
    pdf.draw_table(["Node Name", "Description"], workflow_data, [40, 120])

    pdf.ln(2)
    pdf.sub_sub_section("State Machine Design")
    pdf.body_text(
        "The workflow uses a StateGraph with typed state schema. Each node reads from and writes to a shared state "
        "dictionary. Conditional edges enable branching: if hallucination_check fails, the workflow routes to a "
        "fallback handler instead of generation. If multiple query variants are used, hybrid_search runs in "
        "parallel branches."
    )

    # --- 4.7 ---
    pdf.sub_section_title("Generation Engine — Qwen3 8B")
    pdf.body_text(
        "The generation component uses Qwen3 8B, a state-of-the-art open-source language model from Alibaba Cloud. "
        "The model runs locally via Ollama, eliminating API costs and ensuring data privacy. Qwen3 8B provides "
        "strong instruction following, long context handling (up to 128K tokens), and multilingual capabilities."
    )

    pdf.sub_sub_section("Prompt Strategy")
    pdf.body_text(
        "The generation prompt follows a structured template: system instruction specifying the role as a "
        "documentation assistant, instructions to answer only from provided context, citation format requirements, "
        "and a &#34;don&#39;t know&#34; fallback. The retrieved chunks are injected as context, and the user query "
        "is appended. Temperature is set to 0.1 for deterministic, factual responses."
    )

    pdf.sub_sub_section("Response Format")
    pdf.body_text(
        "The LLM generates a structured response with inline citations. Each factual claim is followed by a "
        "citation number in square brackets, referencing the source document. The generation is streamed token "
        "by token via Server-Sent Events (SSE) from FastAPI to the frontend for real-time display."
    )

    # --- 4.8 ---
    pdf.sub_section_title("Citation System")
    pdf.body_text(
        "The citation system is a critical component that ensures answer traceability. It maps each generated "
        "claim to its source document chunk, providing users with verifiable evidence."
    )
    pdf.sub_sub_section("Citation Format")
    pdf.body_text(
        "Citations follow the format [N] where N is a number referencing a source document. At the end of each "
        "answer, a &#34;Sources&#34; section lists all cited documents with titles, page numbers, and direct links. "
        "Example: [1] Next.js Documentation - dynamic-routes.md - Page 12"
    )
    pdf.sub_sub_section("Chunk-to-Source Mapping")
    pdf.body_text(
        "When the LLM generates a citation token, the system maps it to the corresponding chunk metadata. "
        "This ensures that every citation can be traced back to a specific document, page, and section. "
        "The frontend renders citations as clickable links that open the source document."
    )

    # ========================================================================
    # 5. DATA FLOW
    # ========================================================================
    pdf.section_title("Data Flow")

    pdf.sub_section_title("Ingestion Flow")
    pdf.body_text("The document ingestion process follows these sequential steps:")
    steps = [
        "Document Upload — User uploads a file via the React frontend or API endpoint. Supported formats: PDF, HTML, MD, TXT.",
        "Content Extraction — The document loader extracts raw text, preserving structure where possible. PDFs use PyMuPDF, HTML uses BeautifulSoup.",
        "Text Chunking — The extracted text is split into overlapping chunks using the two-stage strategy (recursive + semantic).",
        "Embedding Generation — Each chunk is passed through BGE-base-en-v1.5 to produce a 768-dimensional vector.",
        "Metadata Enrichment — Chunk metadata is assembled: title, source, page number, section hierarchy, etc.",
        "Qdrant Storage — Chunks and their vectors are upserted into the Qdrant collection with full payload.",
        "Indexing Confirmation — Qdrant confirms storage, and the user receives a success notification.",
    ]
    for i, step in enumerate(steps, 1):
        pdf.number_line(i, step)

    pdf.ln(2)
    pdf.sub_section_title("Query Flow")
    pdf.body_text("When a user submits a query, the following pipeline executes:")
    steps = [
        "User Query — User types a question in the React chat interface (e.g., &#34;How do I implement dynamic routing in Next.js?&#34;).",
        "API Reception — FastAPI receives the query, authenticates the user, and passes it to the LangGraph workflow.",
        "Query Transformation — The query is expanded into variants and optionally used to generate a hypothetical document (HyDE).",
        "Hybrid Search — Dense vector search (Qdrant) and BM25 keyword search run in parallel. Both return top-20 results.",
        "RRF Fusion — Reciprocal Rank Fusion merges the two result sets into a single ranked list.",
        "Re-Ranking — The cross-encoder re-ranker scores the top-20 chunks against the original query, selecting top-3 to top-5.",
        "Hallucination Check — The system verifies that retrieved chunks contain sufficient relevant information to answer the query.",
        "LLM Generation — Qwen3 8B receives the query + context and generates an answer with inline citations.",
        "Citation Formatting — The output processor formats citations and appends the source reference section.",
        "Streaming Response — The response is streamed token-by-token via SSE to the frontend.",
        "Monitoring Log — Langfuse records the entire trace: query, retrieval scores, LLM call, latency, tokens used.",
        "User Display — The React UI renders the answer with clickable citations, source cards, and relevance scores.",
    ]
    for i, step in enumerate(steps, 1):
        pdf.number_line(i, step)

    # ========================================================================
    # 6. API LAYER
    # ========================================================================
    pdf.section_title("API Layer")

    pdf.body_text(
        "The FastAPI backend exposes a RESTful API for all system operations. The API is designed with async "
        "endpoints for non-blocking I/O, automatic OpenAPI documentation, request validation via Pydantic, "
        "and JWT-based authentication."
    )

    pdf.sub_section_title("API Endpoints")
    api_data = [
        ["POST", "/api/auth/login", "Authenticate user, return JWT token"],
        ["POST", "/api/auth/register", "Register new user account"],
        ["POST", "/api/ingest/upload", "Upload document(s) for ingestion"],
        ["GET",  "/api/ingest/status/{id}", "Check ingestion status"],
        ["POST", "/api/query/chat", "Submit a query, get streamed response"],
        ["POST", "/api/query/search", "Submit a query, get raw search results"],
        ["GET",  "/api/documents", "List all ingested documents"],
        ["GET",  "/api/documents/{id}", "Get document details and chunks"],
        ["DELETE", "/api/documents/{id}", "Delete document and its chunks"],
        ["GET",  "/api/evaluate/run", "Run evaluation suite on test dataset"],
        ["GET",  "/api/evaluate/results", "Get evaluation results and metrics"],
        ["GET",  "/api/health", "System health check"],
        ["GET",  "/api/stats", "System usage statistics"],
    ]
    pdf.draw_table(["Method", "Endpoint", "Description"], api_data, [18, 55, 87])

    pdf.ln(2)
    pdf.sub_section_title("Authentication & Authorization")
    pdf.body_text(
        "Access to the API is secured using JSON Web Tokens (JWT). Users authenticate via the /auth/login endpoint "
        "and receive an access token (15-minute expiry) and a refresh token (7-day expiry). Protected endpoints "
        "validate the token via OAuth2 dependency injection. Role-based access control (RBAC) distinguishes "
        "admin users (can ingest/delete) from regular users (can query only)."
    )

    # ========================================================================
    # 7. FRONTEND APPLICATION
    # ========================================================================
    pdf.section_title("Frontend Application")

    pdf.body_text(
        "The frontend is a modern single-page application built with React 18 and TypeScript. It provides an "
        "intuitive chat interface with real-time streaming responses, interactive citations, and document "
        "management capabilities. The UI is styled with TailwindCSS for a clean, responsive design."
    )

    pdf.sub_section_title("Key Features")
    pdf.bold_bullet("Chat Interface — ", "Message-based Q&A with streaming token-by-token response display. Markdown rendering for formatted answers.")
    pdf.bold_bullet("Citation Cards — ", "Each answer includes collapsible citation cards showing source document title, page number, and a preview of the relevant chunk.")
    pdf.bold_bullet("Document Upload — ", "Drag-and-drop interface for uploading documents. Real-time progress tracking and ingestion status updates.")
    pdf.bold_bullet("Dashboard — ", "System statistics: total documents, queries today, average latency, token usage, and retrieval success rate.")
    pdf.bold_bullet("Document Manager — ", "Browse, search, and delete ingested documents. View document details and chunk previews.")
    pdf.bold_bullet("Authentication UI — ", "Login and registration pages with form validation and session management.")
    pdf.bold_bullet("Dark/Light Mode — ", "Theme toggle for comfortable viewing in any environment.")

    pdf.sub_section_title("Component Architecture")
    frontend_data = [
        ["App", "Root component, routing, theme provider"],
        ["ChatPage", "Main chat interface with message list and input"],
        ["MessageList", "Virtualized message list with streaming support"],
        ["MessageBubble", "Individual message with markdown and citations"],
        ["CitationCard", "Collapsible source document card"],
        ["UploadPage", "File upload with drag-drop and progress"],
        ["Dashboard", "System statistics and charts"],
        ["DocManager", "Document list with search and delete"],
        ["LoginForm", "User authentication form"],
        ["Sidebar", "Navigation sidebar"],
        ["Layout", "Page layout with header, sidebar, content"],
    ]
    pdf.draw_table(["Component", "Description"], frontend_data, [38, 122])

    # ========================================================================
    # 8. EVALUATION FRAMEWORK
    # ========================================================================
    pdf.section_title("Evaluation Framework")

    pdf.body_text(
        "A rigorous evaluation framework ensures the system meets quality standards before deployment. "
        "The framework includes a golden test dataset, automated metric computation using the RAGAS library, "
        "and regression testing integrated into the CI pipeline."
    )

    pdf.sub_section_title("Golden Dataset")
    pdf.body_text(
        "The evaluation dataset consists of 50+ curated question-answer pairs derived from the ingested "
        "documentation. Each entry includes: question, ground truth answer, relevant document IDs, relevant "
        "chunk IDs, and expected citation sources. The dataset covers simple factual questions, comparative "
        "questions, multi-document questions, and edge cases."
    )

    pdf.sub_section_title("Retrieval Metrics")
    ret_metrics = [
        ["Recall@k", "Proportion of relevant documents retrieved in top-k", "Target > 0.85 @ k=5"],
        ["MRR", "Mean Reciprocal Rank — rank position of first relevant result", "Target > 0.90"],
        ["NDCG@k", "Normalized Discounted Cumulative Gain", "Target > 0.80 @ k=5"],
        ["Precision@k", "Proportion of retrieved documents that are relevant", "Target > 0.70 @ k=5"],
    ]
    pdf.draw_table(["Metric", "Description", "Target"], ret_metrics, [25, 90, 45])

    pdf.ln(2)
    pdf.sub_section_title("Generation Metrics")
    gen_metrics = [
        ["Faithfulness", "Proportion of claims in answer that are supported by context", "Target > 0.90"],
        ["Answer Relevance", "How relevant the answer is to the question", "Target > 0.85"],
        ["Context Precision", "Proportion of retrieved context actually used in answer", "Target > 0.80"],
        ["Context Recall", "Proportion of relevant context that was retrieved", "Target > 0.85"],
        ["BLEU Score", "N-gram overlap between generated and reference answer", "Target > 0.30"],
        ["ROUGE-L", "Longest common subsequence between generated and reference", "Target > 0.45"],
    ]
    pdf.draw_table(["Metric", "Description", "Target"], gen_metrics, [30, 85, 45])

    pdf.ln(2)
    pdf.sub_section_title("Automated Evaluation Pipeline")
    pdf.body_text(
        "The evaluation pipeline runs automatically on every pull request via GitHub Actions. When triggered, "
        "the pipeline: (1) builds the system, (2) ingests the golden dataset documents, (3) runs all test queries, "
        "(4) computes retrieval and generation metrics, (5) compares against baseline thresholds, and "
        "(6) reports pass/fail status. Any regression in metrics blocks the PR from merging."
    )

    # ========================================================================
    # 9. PRODUCTION DEPLOYMENT
    # ========================================================================
    pdf.section_title("Production Deployment")

    pdf.sub_section_title("Docker Compose Architecture")
    pdf.body_text(
        "The entire system is containerized using Docker and orchestrated with Docker Compose. Each service runs "
        "in its own container with explicit resource limits, health checks, and dependency management. "
        "The compose file defines the following services:"
    )

    svc_data = [
        ["frontend", "React app served via Nginx", "Port 3000"],
        ["backend", "FastAPI application (uvicorn)", "Port 8000"],
        ["qdrant", "Qdrant vector database", "Port 6333"],
        ["ollama", "Ollama LLM server", "Port 11434"],
        ["langfuse", "Langfuse monitoring server", "Port 3001"],
        ["postgres", "Langfuse database (PostgreSQL)", "Port 5432"],
        ["nginx", "Reverse proxy (API gateway)", "Port 80/443"],
    ]
    pdf.draw_table(["Service", "Description", "Port"], svc_data, [25, 90, 45])

    pdf.ln(2)
    pdf.sub_section_title("CI/CD Pipeline — GitHub Actions")
    pdf.body_text(
        "Two GitHub Actions workflows ensure code quality and automated deployment:"
    )
    pdf.sub_sub_section("CI Pipeline (ci.yml)")
    pdf.bold_bullet("Trigger — ", "On every push and pull request to main branch.")
    pdf.bold_bullet("Steps — ", "Checkout -> Set up Python -> Install dependencies -> Run ruff (linting) -> Run mypy (type checking) -> Run pytest (unit tests + integration tests) -> Build Docker images.")
    pdf.bold_bullet("Cache — ", "Python venv, Docker layers, and model downloads are cached for fast execution.")

    pdf.sub_sub_section("CD Pipeline (cd.yml)")
    pdf.bold_bullet("Trigger — ", "On merge to main branch (after CI passes).")
    pdf.bold_bullet("Steps — ", "Build and tag Docker images -> Push to container registry -> Deploy to staging -> Run smoke tests -> Promote to production.")
    pdf.bold_bullet("Rollback — ", "Automatic rollback if smoke tests fail or health checks return non-200 status.")

    pdf.sub_section_title("Monitoring & Observability — Langfuse")
    pdf.body_text(
        "Langfuse provides comprehensive observability for the LLM pipeline. It captures:"
    )
    pdf.bold_bullet("Traces — ", "End-to-end request tracing from query to response, with timing for each step.")
    pdf.bold_bullet("LLM Calls — ", "Prompt and completion logging, token counts, and cost estimation.")
    pdf.bold_bullet("Retrieval Metrics — ", "Number of chunks retrieved, scores, re-ranking impact.")
    pdf.bold_bullet("Evaluation Scores — ", "Inference-time evaluation of answer faithfulness and relevance.")
    pdf.bold_bullet("Latency Analysis — ", "P50, P95, and P99 latency for each pipeline stage.")
    pdf.bold_bullet("User Feedback — ", "Thumbs up/down for each answer to collect training data for improvement.")

    # ========================================================================
    # 10. USE CASES
    # ========================================================================
    pdf.section_title("Use Cases")

    pdf.sub_section_title("1. SaaS Documentation Assistant")
    pdf.body_text(
        "The primary use case is answering questions about software documentation. By ingesting documentation "
        "from frameworks like React, Next.js, LangChain, and FastAPI, developers can get instant, accurate "
        "answers with source references."
    )
    pdf.bold_bullet("Example Query — ", "&#34;How do I implement dynamic routing in Next.js?&#34;")
    pdf.bold_bullet("System Action — ", "Retrieves the relevant section from Next.js docs about dynamic routes, generates an answer with code examples, and cites the exact documentation page.")
    pdf.bold_bullet("Value — ", "Eliminates hours of manual documentation searching. Developers get answers in seconds with confidence in accuracy.")

    pdf.sub_section_title("2. Research Paper Assistant")
    pdf.body_text(
        "Researchers can upload collections of academic papers and query the system for key findings, "
        "methodologies, and comparisons."
    )
    pdf.bold_bullet("Example Query — ", "&#34;What are the main contributions of paper #7 regarding attention mechanisms?&#34;")
    pdf.bold_bullet("Value — ", "Enables rapid literature review across hundreds of papers with verifiable citations to specific paragraphs.")

    pdf.sub_section_title("3. Legal Document Assistant")
    pdf.body_text(
        "Law firms and legal departments can ingest contracts, agreements, and legal documents for instant clause retrieval."
    )
    pdf.bold_bullet("Example Query — ", "&#34;What is the termination notice period in the service agreement with vendor X?&#34;")
    pdf.bold_bullet("Value — ", "Reduces contract review time from hours to seconds with exact clause citations.")

    pdf.sub_section_title("4. Healthcare Policy Assistant")
    pdf.body_text(
        "Healthcare organizations can query internal policies, treatment guidelines, and regulatory documents."
    )
    pdf.bold_bullet("Example Query — ", "&#34;What is the recommended protocol for patient data access under HIPAA?&#34;")
    pdf.bold_bullet("Value — ", "Ensures compliance by grounding answers in official policy documents with exact references.")

    pdf.sub_section_title("5. University Student Assistant")
    pdf.body_text(
        "Universities can ingest handbooks, course catalogs, and policy documents for student self-service."
    )
    pdf.bold_bullet("Example Query — ", "&#34;How many credit hours are required for the Computer Science major?&#34;")
    pdf.bold_bullet("Value — ", "Reduces administrative workload by enabling students to find answers independently.")

    # ========================================================================
    # 11. IMPLEMENTATION ROADMAP
    # ========================================================================
    pdf.section_title("Implementation Roadmap")

    pdf.body_text(
        "The project is organized into seven implementation phases, each building on the previous one. "
        "Estimated total time: 17-23 days of part-time work."
    )

    roadmap_data = [
        ["1", "Foundation", "Project setup, Docker Compose, config, loaders, splitters, embedding pipeline, Qdrant integration", "3-4 days"],
        ["2", "Retrieval Stack", "BM25 implementation, RRF fusion, cross-encoder re-ranker, query transformation", "2-3 days"],
        ["3", "LangGraph & Generation", "StateGraph workflow, prompt engineering, citation system, streaming", "3-4 days"],
        ["4", "API & Authentication", "FastAPI routes, JWT auth, request validation, rate limiting", "2 days"],
        ["5", "Frontend Application", "React UI, chat interface, citation cards, document upload, dashboard", "3-4 days"],
        ["6", "Evaluation & Testing", "Golden dataset, RAGAS metrics, pytest suite, regression testing", "2-3 days"],
        ["7", "Production Readiness", "CI/CD pipelines, Docker optimization, monitoring config, documentation", "2-3 days"],
    ]
    pdf.draw_table(["Phase", "Name", "Key Activities", "Duration"], roadmap_data, [10, 30, 95, 25])

    # ========================================================================
    # 12. SUCCESS METRICS
    # ========================================================================
    pdf.section_title("Success Metrics & Acceptance Criteria")

    pdf.body_text(
        "The following metrics define project success and serve as acceptance criteria for production deployment:"
    )

    metrics_data = [
        ["Retrieval Recall@5", "> 0.85", "Proportion of relevant documents in top-5 results"],
        ["Answer Faithfulness", "> 0.90", "Claims supported by retrieved context"],
        ["Answer Relevance", "> 0.85", "Answer addresses the user query"],
        ["P50 Latency", "< 3 seconds", "Median query-to-response time"],
        ["P95 Latency", "< 8 seconds", "95th percentile response time"],
        ["Citation Accuracy", "> 95%", "Citations correctly map to source documents"],
        ["System Uptime", "> 99.5%", "API and frontend availability"],
        ["Test Coverage", "> 80%", "Code coverage from pytest suite"],
        ["CI Pass Rate", "100%", "All CI checks pass before merge"],
        ["Token Efficiency", "< 1000 tokens/response", "Average tokens per generated answer"],
    ]
    pdf.draw_table(["Metric", "Target", "Description"], metrics_data, [38, 20, 102])

    pdf.ln(2)
    pdf.sub_section_title("Monitoring Dashboard Metrics")
    pdf.body_text(
        "The Grafana dashboard displays real-time metrics including: queries per minute, average latency by stage, "
        "retrieval score distribution, token consumption, error rates by endpoint, and active users. "
        "Alerts are configured for: latency exceeding P95 threshold, error rate > 5%, and service health check failures."
    )

    # ========================================================================
    # 13. CONCLUSION
    # ========================================================================
    pdf.section_title("Conclusion")

    pdf.body_text(
        "The Production-Grade RAG System represents a complete, enterprise-ready solution for building trustworthy "
        "AI-powered knowledge assistants. By combining state-of-the-art retrieval techniques with rigorous "
        "evaluation and production infrastructure, the system delivers accurate, verifiable answers from "
        "organizational knowledge bases."
    )

    pdf.body_text(
        "Key differentiators of this system include: hybrid search with RRF fusion for robust retrieval, "
        "cross-encoder re-ranking for precision, LangGraph orchestration for sophisticated workflow control, "
        "a comprehensive citation system for answer traceability, local LLM inference for cost efficiency "
        "and data privacy, automated evaluation with RAGAS metrics, and full production infrastructure "
        "with monitoring, logging, and CI/CD."
    )

    pdf.info_box(
        "Portfolio Impact",
        "This project demonstrates capability across the full AI engineering stack: data processing, "
        "vector databases, LLM orchestration, evaluation, monitoring, and production deployment. "
        "It showcases not just &#34;chatbot building&#34; but production-grade AI system engineering."
    )

    pdf.ln(4)
    pdf.set_draw_color(*COLOR_SECONDARY)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(*COLOR_TEXT_LIGHT)
    pdf.multi_cell(0, 6, "This document is intended as a technical reference and project overview. "
                   "For implementation details, refer to the project source code and inline documentation.", align="C")

    # ========================================================================
    # SAVE
    # ========================================================================
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf.output(OUTPUT_FILE)
    return OUTPUT_FILE


if __name__ == "__main__":
    path = build_document()
    print(f"PDF generated: {path}")
    print(f"Size: {os.path.getsize(path) / 1024:.1f} KB")
    print(f"Pages: (opening PDF to count...)")
