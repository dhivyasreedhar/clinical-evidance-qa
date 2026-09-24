from dataclasses import replace

import pytest
from clinical.domain.evidence import InvalidSource, decode_source, identity_disposition, span_for


def test_exact_unicode_crlf_offsets_and_repeated_quotes():
    raw = "Document ID: example\r\nMRN: A-1 | DOB: 1980-01-01\r\n\r\nRepeated 🧪\r\n\r\nRepeated 🧪\r\n".encode()
    source = decode_source(raw, "note.txt", 1000)
    assert source.text.encode() == raw
    assert source.line_count == 6
    for block in source.blocks:
        block.validate(source.text)
    assert source.blocks[-1].quote == source.blocks[-2].quote
    assert source.blocks[-1].start_char != source.blocks[-2].start_char
    assert identity_disposition(source, "A-1", "1980-01-01") is None
    assert identity_disposition(source, "A-2", "1980-01-01") == "identity_mismatch"


def test_invented_quote_and_wrong_lines_rejected():
    text = "one\n\ntwo"
    span = span_for(text, 5, 8)
    with pytest.raises(InvalidSource, match="quote_mismatch"):
        replace(span, quote="six").validate(text)
    with pytest.raises(InvalidSource, match="line_mismatch"):
        replace(span, start_line=1).validate(text)


@pytest.mark.parametrize(
    "raw,filename",
    [
        (b"", "a.txt"),
        (b"\xff", "a.txt"),
        (b"a\x00b", "a.txt"),
        (b"abc", "a.pdf"),
        (b"  \r\n", "a.txt"),
    ],
)
def test_invalid_sources_rejected(raw, filename):
    with pytest.raises(InvalidSource):
        decode_source(raw, filename, 1000)


def test_missing_and_multiple_identities_never_silently_attach():
    missing = decode_source(b"A narrative without a header.", "a.txt", 1000)
    assert identity_disposition(missing, "X", "1980-01-01") == "identity_unconfirmed"
    mixed = decode_source(b"MRN X | DOB 1980-01-01\nMRN Y | DOB 1981-01-01", "a.txt", 1000)
    assert identity_disposition(mixed, "X", "1980-01-01") == "identity_mismatch"
