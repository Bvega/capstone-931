from __future__ import annotations

import ipaddress
from urllib.parse import urlparse


class InputValidationError(ValueError):
    """Raised when a user-supplied account URL is invalid or unsafe."""


def validate_public_url(value: str) -> str:
    raw = value.strip()
    if not raw:
        raise InputValidationError("Enter a company URL.")
    parsed = urlparse(raw)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise InputValidationError("Use a full public URL beginning with https:// or http://.")
    host = parsed.hostname.rstrip(".").lower()
    if host in {"localhost", "localhost.localdomain"} or host.endswith(".local"):
        raise InputValidationError("Use a public company website, not a local address.")
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        address = None
    if address is not None and (not address.is_global):
        raise InputValidationError("Use a public company website, not a private or reserved IP address.")
    return raw


def parse_competitor_urls(value: str, limit: int = 5) -> list[str]:
    candidates = [line.strip() for line in value.splitlines() if line.strip()]
    if len(candidates) > limit:
        raise InputValidationError(f"Enter no more than {limit} competitor URLs.")
    seen: set[str] = set()
    results: list[str] = []
    for candidate in candidates:
        url = validate_public_url(candidate)
        normalized = url.rstrip("/").lower()
        if normalized not in seen:
            seen.add(normalized)
            results.append(url)
    return results

