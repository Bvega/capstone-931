from __future__ import annotations

from io import BytesIO
from pathlib import Path


class DocumentInputError(ValueError):
    """Raised when an optional product overview cannot be read."""


MAX_FILE_BYTES = 5 * 1024 * 1024
MAX_TEXT_CHARS = 20_000


def extract_document_text(filename: str, content: bytes) -> str:
    if len(content) > MAX_FILE_BYTES:
        raise DocumentInputError("The uploaded file is larger than 5 MB.")
    suffix = Path(filename).suffix.lower()
    try:
        if suffix in {".txt", ".md"}:
            text = content.decode("utf-8", errors="replace")
        elif suffix == ".pdf":
            from pypdf import PdfReader

            reader = PdfReader(BytesIO(content))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        elif suffix == ".docx":
            from docx import Document

            document = Document(BytesIO(content))
            text = "\n".join(paragraph.text for paragraph in document.paragraphs)
        else:
            raise DocumentInputError("Supported overview files: .txt, .md, .pdf, and .docx.")
    except DocumentInputError:
        raise
    except Exception as exc:
        raise DocumentInputError("The uploaded file could not be read. Try a text, PDF, or DOCX file.") from exc
    cleaned = "\n".join(line.strip() for line in text.splitlines() if line.strip())
    if not cleaned:
        raise DocumentInputError("No readable text was found in the uploaded file.")
    return cleaned[:MAX_TEXT_CHARS]

