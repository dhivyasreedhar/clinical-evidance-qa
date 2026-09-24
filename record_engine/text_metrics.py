"""Secondary lexical diagnostics for answers against the benchmark reference answers.

Pure-Python, dependency-free implementations so results are reproducible offline. They measure
wording overlap with a reference answer, not clinical correctness: never gate on them and never
average them into a headline score.

Variants (report these names with any number):
- Tokenization ``lower-alnum-v1``: lowercase; tokens are runs of letters/digits, keeping ``:`` and
  ``.`` inside numbers (``10:45``, ``44.4``) as one token.
- ``bleu4-corpus`` / ``bleu4-sentence``: BLEU with uniform 1–4-gram weights and brevity penalty
  (Papineni et al. 2002); sentence BLEU uses add-one smoothing on n>1 precisions (Lin & Och 2004
  method 2).
- ``rouge1/2/L-f1``: F1 of unigram/bigram overlap and of the longest common subsequence
  (Lin 2004), single reference.
"""

import math
import re
from collections import Counter
from collections.abc import Sequence

TOKENIZATION = "lower-alnum-v1"
TOKEN = re.compile(r"\d+(?:[:.]\d+)*|[a-z]+")


def tokens(text: str) -> list[str]:
    return TOKEN.findall(text.lower())


def ngrams(words: Sequence[str], n: int) -> Counter[tuple[str, ...]]:
    return Counter(tuple(words[i : i + n]) for i in range(len(words) - n + 1))


def _bleu_parts(candidate: list[str], reference: list[str]) -> tuple[list[int], list[int]]:
    matches, totals = [], []
    for n in range(1, 5):
        cand, ref = ngrams(candidate, n), ngrams(reference, n)
        matches.append(sum(min(c, ref[g]) for g, c in cand.items()))
        totals.append(max(len(candidate) - n + 1, 0))
    return matches, totals


def _bleu(matches: list[int], totals: list[int], c_len: int, r_len: int, smooth: bool) -> float:
    if c_len == 0:
        return 0.0
    logs = []
    for n, (m, t) in enumerate(zip(matches, totals, strict=True)):
        if smooth and n > 0:
            m, t = m + 1, t + 1
        if m == 0 or t == 0:
            return 0.0
        logs.append(math.log(m / t))
    brevity = 1.0 if c_len > r_len else math.exp(1 - r_len / c_len)
    return brevity * math.exp(sum(logs) / 4)


def sentence_bleu(candidate: str, reference: str) -> float:
    c, r = tokens(candidate), tokens(reference)
    matches, totals = _bleu_parts(c, r)
    return _bleu(matches, totals, len(c), len(r), smooth=True)


def corpus_bleu(candidates: Sequence[str], references: Sequence[str]) -> float:
    matches, totals, c_len, r_len = [0] * 4, [0] * 4, 0, 0
    for candidate, reference in zip(candidates, references, strict=True):
        c, r = tokens(candidate), tokens(reference)
        m, t = _bleu_parts(c, r)
        matches = [a + b for a, b in zip(matches, m, strict=True)]
        totals = [a + b for a, b in zip(totals, t, strict=True)]
        c_len, r_len = c_len + len(c), r_len + len(r)
    return _bleu(matches, totals, c_len, r_len, smooth=False)


def _f1(overlap: int, candidate: int, reference: int) -> float:
    if overlap == 0 or candidate == 0 or reference == 0:
        return 0.0
    precision, recall = overlap / candidate, overlap / reference
    return 2 * precision * recall / (precision + recall)


def rouge_n(candidate: str, reference: str, n: int) -> float:
    c, r = ngrams(tokens(candidate), n), ngrams(tokens(reference), n)
    return _f1(sum((c & r).values()), sum(c.values()), sum(r.values()))


def rouge_l(candidate: str, reference: str) -> float:
    c, r = tokens(candidate), tokens(reference)
    if not c or not r:
        return 0.0
    previous = [0] * (len(r) + 1)
    for word in c:
        current = [0]
        for j, other in enumerate(r):
            current.append(previous[j] + 1 if word == other else max(previous[j + 1], current[j]))
        previous = current
    return _f1(previous[-1], len(c), len(r))


def set_f1(predicted: set[str], gold: set[str]) -> tuple[float, float, float]:
    """Precision, recall, F1 with the plan's empty-set convention."""
    if not predicted and not gold:
        return 1.0, 1.0, 1.0
    if not predicted or not gold:
        return 0.0, 0.0, 0.0
    tp = len(predicted & gold)
    precision, recall = tp / len(predicted), tp / len(gold)
    return precision, recall, (2 * precision * recall / (precision + recall) if tp else 0.0)
