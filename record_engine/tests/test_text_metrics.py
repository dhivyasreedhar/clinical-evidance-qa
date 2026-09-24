import pytest

from record_engine.text_metrics import (
    corpus_bleu,
    rouge_l,
    rouge_n,
    sentence_bleu,
    set_f1,
    tokens,
)


def test_tokens_keep_times_and_decimals() -> None:
    assert tokens("Session 10:45–11:30, 44.4 min.") == ["session", "10:45", "11:30", "44.4", "min"]


def test_identical_text_scores_one() -> None:
    text = "The patient attended five individual sessions in week one"
    assert sentence_bleu(text, text) == pytest.approx(1.0)
    assert corpus_bleu([text], [text]) == pytest.approx(1.0)
    assert rouge_n(text, text, 2) == pytest.approx(1.0)
    assert rouge_l(text, text) == pytest.approx(1.0)


def test_disjoint_and_empty_text_score_zero() -> None:
    assert sentence_bleu("alpha beta", "gamma delta") == 0.0
    assert rouge_n("", "gamma", 1) == 0.0
    assert rouge_l("alpha", "") == 0.0


def test_rouge_l_uses_subsequence() -> None:
    # LCS "a c d" = 3 of 4 tokens each side.
    assert rouge_l("a b c d", "a c x d") == pytest.approx(0.75)


def test_set_f1_empty_convention() -> None:
    assert set_f1(set(), set()) == (1.0, 1.0, 1.0)
    assert set_f1({"S1"}, set()) == (0.0, 0.0, 0.0)
    assert set_f1({"S1", "S2"}, {"S2", "S3"}) == (0.5, 0.5, 0.5)
