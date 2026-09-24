"""Typed values and the text patterns the recall sweep looks for.

Everything here is format-level (how dates, times and durations are written), never clinical.
"""

from __future__ import annotations

import re
from datetime import date

from record_engine.dates import date_spans, find_dates

# HH:MM, optionally with :SS (seconds are dropped: minute precision) and am/pm; also the time
# part of an ISO timestamp (2026-01-29T15:18:30)
TIME = re.compile(
    r"(?:(?<=T)|\b)([01]?\d|2[0-3])[:.]([0-5]\d)(?::[0-5]\d(?:\.\d+)?)?"
    r"\s*(am|pm|a\.m\.|p\.m\.)?(?![\d:])",
    re.I,
)
DURATION = re.compile(
    r"\b(\d+(?:\.\d+)?)\s*(?:-\s*)?(minutes?|mins?|hours?|hrs?|h)\b(?:\s*(?:and\s*)?(\d+)\s*(?:minutes?|mins?))?",
    re.I,
)
IDENTIFIER = re.compile(r"\b(?=[A-Z0-9-]*\d)(?=[A-Z0-9-]*[A-Z])[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+\b")
SCORE = re.compile(r"\b(?:score[sd]?|total)\b[^.\n]{0,20}?\b(\d+(?:\.\d+)?)\b", re.I)
NUMBER = re.compile(r"(?<![\w.:-])\d+(?:\.\d+)?(?![\w:])")


def parse_time(text: str) -> str | None:
    """'9:05', '09:05', '9.05 pm', '15:18:30', '2026-01-29T15:18:30' -> 'HH:MM' (24 h)."""
    m = TIME.search(text.strip())
    if not m:
        return None
    hour, minute, suffix = int(m.group(1)), int(m.group(2)), (m.group(3) or "").lower()
    if suffix.startswith("p") and hour < 12:
        hour += 12
    if suffix.startswith("a") and hour == 12:
        hour = 0
    return f"{hour:02d}:{minute:02d}"


def times_in(text: str) -> set[str]:
    return {t for m in TIME.finditer(text) if (t := parse_time(m.group(0)))}


def minutes_of(text: str) -> float | None:
    m = DURATION.search(text)
    if not m:
        return None
    value, unit = float(m.group(1)), m.group(2).lower()
    total = value * 60 if unit.startswith("h") else value
    if m.group(3):
        total += float(m.group(3))
    return total


def durations_in(text: str) -> set[float]:
    found = set()
    for m in DURATION.finditer(text):
        value = minutes_of(m.group(0))
        if value is not None:
            found.add(value)
    return found


def numbers_in(text: str) -> set[float]:
    """Numbers written in the text, excluding digits inside dates and clock times."""
    cleaned = text
    spans = date_spans(text) + [m.span() for m in TIME.finditer(text)]
    for start, end in sorted(spans, reverse=True):
        cleaned = cleaned[:start] + " " + cleaned[end:]
    return {float(n) for n in NUMBER.findall(cleaned)}


def parse_date(value: str) -> date | None:
    try:
        return date.fromisoformat(value.strip()[:10])
    except ValueError:
        return None


def dates_in(text: str, first: date | None = None, last: date | None = None) -> set[date]:
    return find_dates(text, first, last)


def clock(value: str) -> int:
    hours, minutes = map(int, value.split(":"))
    return hours * 60 + minutes


def mentions(text: str) -> list[tuple[str, str, int, int]]:
    """(kind, text, start, end) for every time, date, duration, identifier and score in text."""
    found: list[tuple[str, str, int, int]] = []
    for kind, pattern in (
        ("time", TIME),
        ("duration", DURATION),
        ("identifier", IDENTIFIER),
        ("score", SCORE),
    ):
        found += [(kind, m.group(0), m.start(), m.end()) for m in pattern.finditer(text)]
    found += [("date", text[s:e], s, e) for s, e in date_spans(text)]
    return found
