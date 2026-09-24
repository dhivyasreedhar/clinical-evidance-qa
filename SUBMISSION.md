# Submission: clinical abstraction and evidence-grounded QA

A working prototype that turns the 31 supplied records into an auditable clinical record of Rowan
Mercer's episode of care and answers questions from it. Extraction records only what each document
says, with an exact quote for every value. Linking, reconciliation and every calculation are done by
code under a readable policy, and every answer statement cites source lines.

## Where to look

| Artifact | Location |
|---|---|
| Readable abstraction: encounter ledger, weekly goal results, facts by event, open items, with file:line links | `submission/abstraction.md` |
| The reconciled record: every fact with its status, rule and quoted evidence | `submission/abstraction.json` |
| Observations extracted from each document (the only model output the record is built from) | `submission/observations.jsonl`, `submission/extraction_issues.jsonl` |
| Answers to the 65 benchmark questions (DEV-01–05 first), with sources and checks | `submission/answers.md`, `submission/answers.json` |
| DEV-01 to DEV-05 from the current code, compact, with source lines | `submission/dev01-05_answers.md` |
| Cost and time per question and for the extraction, cached and cold | `submission/run_stats.json`, `submission/extraction_stats.json` |
| Benchmark results, held-out set and changed-input scenarios | `submission/benchmark/README.md`, `submission/benchmark/metrics.json` |
| Engine design, checks and limits | `record_engine/README.md` |
| Design decisions and system diagram | `docs/adr/`, `docs/system-design.png` |

## Run it

Requirements: Python 3.13, uv, Node 24, Docker (or PostgreSQL 16), and `EHR_ANTHROPIC_API_KEY` in `.env`.

```sh
make setup && make db && make migrate          # install, start Postgres, migrate
make evaluate                                  # record + 65 answers + judge + metrics -> submission/
make heldout                                   # 15 held-out questions, graded separately
make scenarios                                 # 13 changed-input scenarios
make dev                                       # web app at http://localhost:3000
```

Model outputs are cached by everything that shapes them, so a re-run pays only for what changed.
Other question files run with `python -m record_engine ask --questions FILE --out DIR`. New documents
can be uploaded in the app (the record is rebuilt automatically, extracting only the new
documents) or added on the command line with `python -m record_engine add FILE ...`, which works on
a copy of `documents/` and reports what changed.

## Approach

1. **Ingest (code):** numbered lines and citable blocks (paragraphs, table rows) per document. In
   the app, TXT files become immutable revisions routed to their patient by the MRN and date of
   birth in the header; mismatches are quarantined.
2. **Extract (Sonnet, one call per document, temperature 0):** observations, each field as
   `{value, quote, block}`. The prompt is generated from the policy's observation kinds and fields.
3. **Validate and sweep (code):** a value must be inside its own quote, so a subtraction or an
   unstated date cannot pass. Every time, date, duration, ID and score in the text must be covered by
   some quote; uncovered mentions get one targeted re-extraction, and what remains becomes an open
   item.
3a. **Cross-check (two readings):** every document is read a second time, independently. Code
   builds records from both and compares every event's key fields per document. A document where
   the readings disagree gets one focused re-read told what was disputed; a point is settled when
   the re-read agrees with one reading (two of three), otherwise it stays visible as an open item. A
   re-read may add what both readings left out, but one that contradicts both is rejected.
4. **Link (code):** the same visit ID and issuer make one event; otherwise a weighted match on date,
   service, time and participants proposes candidate links, which are reported, not merged. Copies
   are detected and their findings not repeated. A document naming another patient is set aside.
5. **Reconcile (code + policy):** per event and field, admissible observations are superseded by a
   later correction (only the fields it names), ranked (signed over unsigned over draft; recorded at
   the time over later, when every account's timing is known), and decided as documented,
   corroborated, established or conflicting. Conflicting values stay as scenarios (40 **or** 50
   minutes) and are never averaged or added together. Partial attendance is derived from the times
   (presence inside the booking), not from wording.
6. **Answer:** a planner (Sonnet) writes queries in a small query language, each stating its
   population, plus a checklist; code executes them (scenario arithmetic, provenance per row, an
   "all groups" total row); the writer (Sonnet) states typed statements citing result, fact and
   open-item IDs and source passages.
7. **Check:** code checks citations, arithmetic, dates, weekdays, goal outcomes per threshold,
   remaining balances, required totals, conflict status and "not documented" claims (looked up in
   the facts first); a small model (Haiku) checks question parts, checklist coverage, narrative
   support and whether each counted population is the one asked. Code repairs what it can prove,
   one model repair follows, and an answer that still fails a code check is withheld with the
   reasons. Answers whose only gaps are coverage are published as partial with the gaps listed.
   Counts written as words are checked like digits, and a count that introduces a list must match
   the items listed. When a question asks what could be double-counted or is ineligible, code lists
   every such record (bookings not received, copies, corrections, drafts, billing records, exports
   listing several visits) and each must be explained. Each answer has a 90-second budget.
8. **Frame:** a small model selects and orders the checked statements that answer the question
   (lead, then only the context needed to read it) and holds back the rest; code keeps every part
   of the question answered and never drops a conflict about what the lead states. Statements are
   never rewritten, so framing cannot add anything unchecked.

Nothing in code is specific to this patient or specialty: all domain knowledge (observation kinds,
precedence, service vocabulary, counting rules) is in `record_engine/policy.toml`, and the engine is
also tested on a synthetic physical-therapy patient with other ID formats and week starts.

## Results

**Record (code only, from the extracted observations)** reproduces the reference ledger:

- 12 included sessions (5 individual, 5 group, 2 family) on 11 days;
- 585 or 595 minutes: HG-E115 stays conflicting (09:00 vs 09:10 start);
- the HG-E110 departure correction supersedes the original roster and its copy;
- weekly goal: not met, not met, met, cannot determine (partial last week flagged).

**65-question development benchmark** (`submission/benchmark/metrics.json`; withheld answers count
as failures):

| | |
|---|---|
| Published | 65/65 (63 answered, 2 partial) |
| Blinded model judge, factual | 119/130 (mean 1.83, 95% interval 1.72–1.92) |
| Published and fully correct (factual 2) | 55/65 |
| Judge, evidence | mean 1.92 |
| Exact calculations (4 structured gold answers) | 4/4 |
| Citation blocks vs gold source lines, micro precision / recall | 0.61 / 0.43 (macro F1 0.56) |
| ROUGE-1 / BLEU-4 (secondary only) | 0.35 / 0.052 |

**Stability:** a second build from scratch (every model call fresh) gives an identical episode
ledger. 22 of 402 non-text facts differ, none of them counted anywhere: mostly administrative
contacts that one build recorded and the other did not
(`submission/benchmark/stability.json`).

**Held-out set** (15 questions written from the documents, graded separately): 15/15 published,
factual 27/30. **Changed-input scenarios** (run on engine 0.2, not re-run for 0.3): record checks
30/30, answers published 14/14, answer checks 13/14, judge 26/28.

`submission/benchmark/README.md` lists every lost point and its cause.

## Checks and experiments

- **Tests:** 144 in total (plus 2 browser tests), run without model calls: the engine's stage tests on the real record and
  a synthetic second patient, metamorphic tests (the real record changed the way records differ,
  with the expected change checked), changed-input tests, and service unit and integration tests
  against real PostgreSQL with row-level security, including record builds and answers with the
  model steps replaced by fakes; the cross-check and framing are tested with fake readings,
  re-reads and framings.
- **Static checks:** ruff, mypy (strict), TypeScript and Prettier.
- **Stability:** `make evaluate` rebuilds the record from nothing and compares it fact by fact
  with the benchmarked one (`submission/benchmark/stability.json`).
- **Changed inputs:** the 13 scenarios cover a late-entry addendum, a CSV export, a stated length
  only, an e-mail correction, an OCR-damaged draft, a remittance line, another patient's note, a
  reused visit number at another clinic, a withdrawn plan, a plan amendment, a JSON call log, a
  re-imported form, and an equal-standing no-show note. Each has deterministic record checks and
  answer checks.
- **Leakage guard:** gold answers are read only by the evaluator and the held-out grader. Prompts
  contain no patient-specific text.

## One observed limitation, and how to investigate it next

**One extraction is a sample, and a benchmark on one sample overstates stability.** A fresh
extraction on another machine read an appointment export's issuer as "Harbor Grove Behavioral
Health | Appointment desk", and the rule that separates two organisations sharing a visit number
split five visits in two (17 sessions instead of 12). The same comparison showed other silent
differences: a therapist's session start taken for the patient's arrival, a no-show read as
attended. The benchmark had measured only one extraction, so it could not see this.

What changed: every call runs at temperature 0 except the independent second reading, every
document is read twice and compared by code,
disagreements are re-read or left open, a department named after an organisation is the same
issuer, and partial attendance and arrival times are derived from the times. A stability check
now rebuilds the record from nothing: the ledger is identical.

What remains: an error both readings share is not caught by comparing them. Next steps:

1. Run the stability check several times and on the changed-input scenarios, and report the
   distribution of differing facts, not one comparison.
2. For fields that feed counts (status, presence, service, IDs), add code-derived cross-checks
   where the record allows one, as for partial attendance and arrival times.
3. Review the open reading disagreements with a clinician to see which the re-read should have
   settled.

## Models, settings, runtime and cost

- **Models:** `claude-sonnet-4-6` for extraction, planning and answers; `claude-haiku-4-5-20251001`
  for the answer review and framing. Every call at temperature 0, except the independent second
  reading of each document. Structured JSON output with local schema validation; outputs cached by a
  hash of everything that shapes them.
- **Extraction with cross-check, 31 documents:** two readings and 12 focused re-reads, $3.92,
  about 7 minutes with 6 workers. Building the record is code only and takes under a second.
- **65 questions (cold):** $12.58 (≈ $0.19 per question), median 42 s and max 152 s per question.
  Answers now have a 90-second budget: a repair starts only when there is time to finish it.
- **15 held-out questions (cold):** $2.12. **Stability check:** $3.84. **13 scenarios:** $2.96.
- Prices are list prices (Sonnet $3 / $15, Haiku $1 / $5 per million tokens).

## Coding assistance

Built with Anthropic Claude (Cowork, `claude-opus-5-5`): the record engine, its checks, the API and web integration, the evaluation and this document. All changes are covered by the test suite and were
validated on live runs.

## Not production-ready yet

The app is locked to development mode. It uses a development sign-in (no OIDC), local object storage
and non-secure cookies, and has no reviewer sign-off on facts or answers. The judge is a model whose
grades were not adjudicated by a clinician, and every result comes from one synthetic patient.
Exclude `.env`, `.local/`, `.venv/`, `.cache/` and `node_modules/` from any ZIP; `.gitignore`
already does this.
