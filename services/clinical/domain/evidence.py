"""Immutable text and source selectors. No framework, database, or model dependencies."""

import hashlib
import re
from dataclasses import dataclass


class InvalidSource(ValueError):
    pass


@dataclass(frozen=True)
class Span:
    start_char: int
    end_char: int
    start_line: int
    end_line: int
    quote: str

    def validate(self, text: str) -> None:
        if not 0 <= self.start_char < self.end_char <= len(text):
            raise InvalidSource("invalid_span_bounds")
        if text[self.start_char : self.end_char] != self.quote:
            raise InvalidSource("quote_mismatch")
        expected = span_for(text, self.start_char, self.end_char)
        if (self.start_line, self.end_line) != (expected.start_line, expected.end_line):
            raise InvalidSource("line_mismatch")


def span_for(text: str, start: int, end: int) -> Span:
    """Offsets are Unicode code points into exact decoded text, never UTF-16 or bytes."""
    if not 0 <= start < end <= len(text):
        raise InvalidSource("invalid_span_bounds")
    lines = text.splitlines(keepends=True)
    offset = 0
    first = last = 0
    for index, line in enumerate(lines, 1):
        if offset <= start < offset + len(line):
            first = index
        if offset <= end - 1 < offset + len(line):
            last = index
        offset += len(line)
    return Span(start, end, first, last, text[start:end])


@dataclass(frozen=True)
class Source:
    sha256: str
    text: str
    line_count: int
    declared_id: str | None
    mrns: frozenset[str]
    birth_dates: frozenset[str]
    blocks: tuple[Span, ...]


def decode_source(raw: bytes, filename: str, max_bytes: int) -> Source:
    if not filename.lower().endswith(".txt"):
        raise InvalidSource("unsupported_format")
    if not raw or len(raw) > max_bytes:
        raise InvalidSource("invalid_file_size")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise InvalidSource("invalid_utf8") from exc
    if "\x00" in text or not text.strip("\ufeff \t\r\n"):
        raise InvalidSource("invalid_text")
    # Deliberately structural segmentation only. Clinical sub-blocks and shared
    # header context are a later extraction stage; no semantic completeness claim.
    blocks = tuple(
        span_for(text, match.start(), match.end())
        for match in re.finditer(r"[^\r\n]+(?:\r?\n(?![ \t]*\r?\n)[^\r\n]+)*", text)
        if match.group().strip()
    )
    declared = re.search(r"(?mi)^\ufeff?Document ID:\s*([^\r\n]+)", text)
    return Source(
        hashlib.sha256(raw).hexdigest(),
        text,
        len(text.splitlines()),
        declared.group(1).strip() if declared else None,
        frozenset(re.findall(r"\bMRN\s*:?\s*([A-Za-z0-9_-]+)", text)),
        frozenset(re.findall(r"\bDOB\s*:?\s*(\d{4}-\d{2}-\d{2})", text)),
        blocks,
    )


def identity_disposition(source: Source, mrn: str, birth_date: str) -> str | None:
    """Conservative TXT header gate, not general clinical identity resolution."""
    if not source.mrns or not source.birth_dates:
        return "identity_unconfirmed"
    if source.mrns != {mrn} or source.birth_dates != {birth_date}:
        return "identity_mismatch"
    return None
