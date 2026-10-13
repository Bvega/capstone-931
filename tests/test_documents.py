import pytest

from sales_agent.documents import DocumentInputError, extract_document_text


def test_extract_plain_text_and_truncate():
    assert extract_document_text("overview.txt", b"Cloud platform\nFor enterprise teams") == "Cloud platform\nFor enterprise teams"


def test_reject_unsupported_and_empty_files():
    with pytest.raises(DocumentInputError):
        extract_document_text("overview.exe", b"data")
    with pytest.raises(DocumentInputError):
        extract_document_text("overview.txt", b"  \n")

