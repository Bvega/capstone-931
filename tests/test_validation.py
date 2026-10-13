import pytest

from sales_agent.validation import InputValidationError, parse_competitor_urls, validate_public_url


def test_validate_public_https_url():
    assert validate_public_url(" https://example.com/about ") == "https://example.com/about"


@pytest.mark.parametrize("value", ["", "example.com", "file:///tmp/x", "http://localhost", "http://127.0.0.1"])
def test_reject_invalid_or_non_public_urls(value):
    with pytest.raises(InputValidationError):
        validate_public_url(value)


def test_parse_competitors_deduplicates_and_limits():
    assert parse_competitor_urls("https://a.example\nhttps://a.example/\nhttps://b.example") == [
        "https://a.example",
        "https://b.example",
    ]
    with pytest.raises(InputValidationError):
        parse_competitor_urls("\n".join(f"https://{n}.example" for n in range(6)))

