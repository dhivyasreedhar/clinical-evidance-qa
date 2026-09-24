"""① Ingest: numbered lines and citable blocks.

Blocks break on blank lines, and every table row (a line with two or more "|" inside a table) is
its own block. A block ID is ``<document key>:L<start>-<end>``, or ``<document key>:L<n>`` for a
one-line block (1-based, inclusive), so a citation is also a file:line link. A document is
identified by the SHA-256 of its bytes.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from pydantic import BaseModel

TABLE_ROW = re.compile(r"^[^|]*(\|[^|]*){2,}$")


class Block(BaseModel):
    id: str
    start: int
    end: int
    text: str


class Document(BaseModel):
    key: str  # filename stem; unique within a record
    filename: str
    sha256: str
    lines: list[str]
    blocks: list[Block]


def block_id(key: str, start: int, end: int) -> str:
    return f"{key}:L{start}" if start == end else f"{key}:L{start}-{end}"


def split_blocks(key: str, lines: list[str]) -> list[Block]:
    blocks: list[Block] = []
    current: list[tuple[int, str]] = []

    def flush() -> None:
        if current:
            start, end = current[0][0], current[-1][0]
            blocks.append(
                Block(
                    id=block_id(key, start, end),
                    start=start,
                    end=end,
                    text="\n".join(t for _, t in current),
                )
            )
            current.clear()

    for number, line in enumerate(lines, start=1):
        if not line.strip():
            flush()
        elif TABLE_ROW.search(line) and _is_table(lines, number):
            flush()
            current.append((number, line))
            flush()
        else:
            current.append((number, line))
    flush()
    return blocks


def _is_table(lines: list[str], number: int) -> bool:
    """A row is part of a table when a neighbouring line has the same number of separators."""
    row = lines[number - 1]
    count = row.count("|")
    neighbours = [lines[i] for i in (number - 2, number) if 0 <= i < len(lines)]
    return any(n.count("|") == count for n in neighbours)


def ingest_text(filename: str, text: str) -> Document:
    key = Path(filename).stem
    lines = text.splitlines()
    return Document(
        key=key,
        filename=filename,
        sha256=hashlib.sha256(text.encode()).hexdigest(),
        lines=lines,
        blocks=split_blocks(key, lines),
    )


def ingest_folder(folder: Path) -> list[Document]:
    return [ingest_text(p.name, p.read_text()) for p in sorted(folder.glob("*.txt"))]
