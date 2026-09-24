"""Find calendar dates in free text, whatever the common format, anchored to an episode.

Handles ISO (2026-01-26), month-name forms (Jan 26, January 26th, 26 January), numeric month/day
(1/26, 01/26/2026, 1/26/26) and day ranges (Jan 5–11). A missing year is the year that places the
date closest to the episode, so dates across a year boundary resolve correctly.
"""

import re
from datetime import date, timedelta

MONTHS = {
    name: number
    for number, names in enumerate(
        [
            ("january", "jan"),
            ("february", "feb"),
            ("march", "mar"),
            ("april", "apr"),
            ("may",),
            ("june", "jun"),
            ("july", "jul"),
            ("august", "aug"),
            ("september", "sep", "sept"),
            ("october", "oct"),
            ("november", "nov"),
            ("december", "dec"),
        ],
        start=1,
    )
    for name in names
}
_MONTH = "|".join(sorted(MONTHS, key=len, reverse=True))
ISO = re.compile(r"\b(\d{4})-(\d{1,2})-(\d{1,2})\b")
MONTH_FIRST = re.compile(
    rf"\b({_MONTH})\.?\s*(\d{{1,2}})(?:st|nd|rd|th)?(?:\s*[-–]\s*(\d{{1,2}}))?(?:,?\s+(\d{{4}}))?\b",
    re.I,
)
DAY_FIRST = re.compile(rf"\b(\d{{1,2}})(?:st|nd|rd|th)?\s+({_MONTH})\.?(?:,?\s+(\d{{4}}))?\b", re.I)
NUMERIC = re.compile(r"\b(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?\b")


def _resolve(
    month: int, day: int, year: int | None, first: date | None, last: date | None
) -> date | None:
    if year is not None and year < 100:
        year += 2000
    candidates = (
        [year]
        if year is not None
        else sorted(
            {d.year + k for d in (first, last) if d for k in (-1, 0, 1)} or {date.today().year}
        )
    )
    options = []
    for y in candidates:
        try:
            options.append(date(y, month, day))
        except ValueError:
            continue
    if not options:
        return None
    anchors = [d for d in (first, last) if d]
    if not anchors:
        return options[0]
    lo, hi = min(anchors), max(anchors)

    # a year-less date takes the year that puts it inside (or nearest to) the anchoring range
    def distance(d: date) -> int:
        return 0 if lo <= d <= hi else min(abs((d - lo).days), abs((d - hi).days))

    return min(options, key=distance)


def find_dates(
    text: str, first: date | None = None, last: date | None = None, expand: bool = True
) -> set[date]:
    """Every calendar date the text names (ranges expand to each day unless expand is False,
    which keeps only a range's endpoints)."""
    found: set[date] = set()
    for y, m, d in ISO.findall(text):
        resolved = _resolve(int(m), int(d), int(y), first, last)
        if resolved:
            found.add(resolved)
    cleaned = ISO.sub(" ", text)
    for month, day, end_day, year in MONTH_FIRST.findall(cleaned):
        number = MONTHS[month.lower()]
        start = _resolve(number, int(day), int(year) if year else None, first, last)
        if start is None:
            continue
        found.add(start)
        if end_day and int(end_day) > int(day) and not expand:
            found.add(start + timedelta(days=int(end_day) - int(day)))
        elif end_day and int(end_day) > int(day):
            found |= {start + timedelta(days=k) for k in range(1, int(end_day) - int(day) + 1)}
    for day, month, year in DAY_FIRST.findall(cleaned):
        resolved = _resolve(
            MONTHS[month.lower()], int(day), int(year) if year else None, first, last
        )
        if resolved:
            found.add(resolved)
    for m, d, y in NUMERIC.findall(cleaned):
        if 1 <= int(m) <= 12:
            resolved = _resolve(int(m), int(d), int(y) if y else None, first, last)
            if resolved:
                found.add(resolved)
    return found


def date_spans(text: str) -> list[tuple[int, int]]:
    """Character spans of every date expression, so numbers inside dates are not read as values."""
    spans = []
    for pattern in (ISO, MONTH_FIRST, DAY_FIRST, NUMERIC):
        spans += [m.span() for m in pattern.finditer(text)]
    return spans
