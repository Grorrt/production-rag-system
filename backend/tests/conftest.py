"""
Pytest configuration and shared fixtures for testing.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pytest


@pytest.fixture
def sample_pdf_path():
    """Returns path to a sample PDF for testing."""
    path = Path(__file__).parent.parent / "sample_documents" / "sample.pdf"
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, text="Sample PDF for testing", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(200, 10, text="This is a test document.", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(200, 10, text="Dynamic routing in Next.js uses the app directory.", new_x="LMARGIN", new_y="NEXT")
        pdf.output(str(path))

    return str(path)


@pytest.fixture
def sample_text_path():
    """Creates and returns a sample text file path."""
    path = Path(__file__).parent.parent / "sample_documents" / "sample.txt"
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        "React useEffect Cleanup\n\n"
        "The cleanup function in useEffect runs when the component unmounts.\n"
        "It is used to clean up subscriptions, timers, and event listeners.\n"
        "Return a function from the effect to set up cleanup.\n",
        encoding="utf-8",
    )

    return str(path)
