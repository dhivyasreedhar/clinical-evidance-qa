# record_engine: observations first, facts by code

The abstraction and question-answering engine of the clinical workspace. From the command line
it reads `documents/*.txt` directly; the clinical service runs it over a patient's stored
documents (see *Database and API*).

## Principles

- **Observations, not conclusions.** Extraction records what each document says, with an exact
  quote for every value. Deciding what is true is a separate step, done by code.
- **One generic algorithm plus a readable policy file.** All domain knowledge lives in
  `policy.toml`: observation kinds and fields, admissibility, precedence, service vocabulary,
  counting and link weights. A new kind of document is new data, not new code.
- **Questions compile to queries.** Code runs every calculation. Conflicting values carry
  through as scenarios and are never added together.
- **Temperature 0, and never one reading.** Every model call runs at temperature 0 except the
  second reading: each document is also read a second time, independently (temperature 1), and code compares the two readings; a
  disagreement is settled by a focused re-read (two of three) or stays visible as an open item.
- **Answers cite fact and result IDs**, so they can be checked by lookup. Code checks values,
  completeness and status. A small model checks only checklist coverage and narrative support.
  Code failures always block.
- **Answers are on point.** A framing step selects and orders the checked statements that answer
  the question; everything else is held back. It never rewrites a statement.

## Pipeline

```
documents/*.txt
  ① ingest (code)           numbered lines, blocks (blank lines / table rows), sha256
  ② extract (Sonnet)        one call per document, every field {value, quote, block}, cached by hash
  ③ validate + sweep (code) value must be inside its quote (so no subtraction, no unstated dates);
                            every time/date/duration/ID/score must be covered by some quote →
                            one targeted re-extraction → leftovers become open items
  ②' cross-check            ② – ③ again as an independent second reading; records are built from
                            both and code compares every event's key fields per document (dates,
                            times, durations, numbers, statuses, IDs, service category, provenance,
                            relations). A document where the readings disagree gets one focused
                            re-read (temperature 0) told what was disputed; its observations of the
                            disputed kinds replace the first reading's. A point is settled when the
                            re-read agrees with one reading (two of three), otherwise it is an open
                            item. A re-read may add what both readings left out but may not
                            contradict both; one that does is rejected for its document.
observations.jsonl
  ④ link (code)             same ID + issuer → one event (a record naming no issuer joins the one
                            issuer using that ID, flagged); otherwise a weighted match on date,
                            service, time, participants with hand-set weights (candidate links
                            reported, not merged); copies detected, their findings not repeated
  ⑤ reconcile (code+policy) per event × field: admissible → supersede (latest correction, only
                            the fields it names; copies fall with their original) → rank (signed >
                            unsigned > draft; at the time > later, used only when every competing
                            account's timing is known) → decide documented / corroborated /
                            established / conflicting (scenarios). Minutes are computed per
                            surviving document account (its own start, end, breaks, gaps); the
                            scenarios are the distinct account results, never mixed across
                            documents; disagreeing break accounts are scenarios too. Partial
                            attendance is derived from the times (presence inside the booking), and
                            a patient-absent segment at the start or end of a session moves the
                            patient's own arrival or departure to its edge
abstraction.json / abstraction.md   facts, timelines, encounter table, open items
question
  ⑥ plan (Sonnet)           queries in the small query language, each with its population in
                            plain words, + checklist; one retry on a query error or when a date
                            the question names is outside every query's window
  ⑦ execute (code)          scenario arithmetic, provenance per row, excluded rows listed, an
                            "all groups" total row for grouped results
  ⑧ answer (Sonnet)         typed statements (value/conflict/missing/inference/narrative) citing
                            result/fact/open-item IDs and source passages; the writer gets the
                            record around the question (every fact of the events it names or the
                            results return, findings on its dates, open items), not only results
  ⑨ check                   code: binding (code-proven citations, verified arithmetic), dates,
                            weekdays, goal outcomes per threshold (and for the goal as a whole),
                            remaining balances, checklist totals, completeness, conflict status,
                            not-documented facts; every absence claim is looked up in the facts
                            table (the patient's identity included) first, then in the source
                            passages; Haiku: question parts, checklist, support and whether each
                            counted population is the one asked. A population mismatch, a
                            "missing" quantity the record holds, or a figure no query computed
                            re-plans once. Code repairs what it can prove (cites the passage
                            holding a stray date, or drops that clause); one model repair, a second
                            only when every remaining failure is a code finding. Code findings and
                            model-judged errors withhold; when only coverage gaps remain the answer
                            is published as partial with the gaps listed.
  ⑩ frame (Haiku + code)    selects and orders the checked statements: the lead that answers the
                            question, then only the context needed to read it (a conflict or gap
                            about a figure it states). Code keeps every part of the question
                            answered and keeps a conflict about what the lead states; the rest is
                            held back under `omitted`. Statements are never rewritten.
answers.json / answers.md
```

Model calls: two readings per document (each with a targeted sweep for about a quarter of them)
and a focused re-read for each document the readings disagree about, once. Then 4 per question:
plan, answer, check and frame (plus an absence check when the answer says something is not
documented). A repair adds 2 more, a failed query or window one planner retry, and a population
mismatch one re-plan.

## Cost and time (list prices: Sonnet 4.6 $3 / $15, Haiku 4.5 $1 / $5 per million tokens)

Cold figures: what a run costs and takes with nothing cached.

| Step | Cost | Time |
|---|---|---|
| Extraction with cross-check, 31 documents (two readings, 12 re-reads) | $3.92 | about 7 minutes with 6 workers |
| Build (code only) | $0 | under 1 second |
| 65 benchmark questions | $12.58 (≈ $0.19 per question) | median 42 s, max 152 s per question (before the 90-second answer budget) |
| 15 held-out questions | $2.12 (≈ $0.14 per question) | median 31 s, max 69 s per question |
| Stability check (a second build from scratch) | $3.84 | about 7 minutes |

Every answer carries its own `usage`: calls, tokens, `cost_usd` and `seconds` for this run, and
`full_cost_usd` and `cold_seconds` as if nothing were cached. `run_stats.json` holds both views
(`this_run` and `cold`) per question and in total, and says whether the run's own timing was
cold, cached or partly cached. `extraction_stats.json` has the extraction run.

## Run

```
python -m record_engine observe                 # ① – ③  → .local/record_engine/observations.jsonl
python -m record_engine build                   # ④ – ⑤  → abstraction.json, abstraction.md
python -m record_engine ask --questions clinical_qa_benchmark/questions.json [--ids DEV-01 ...] \
                           --gate DEV-01..05     # exit 1 if any gated question is withheld
python -m record_engine add NEW.txt ... [--workspace DIR]
                                                # copy into a working copy of documents/ (never
                                                # the supplied folder), re-observe, rebuild, changes.md
python -m record_engine.evaluate grade          # blinded judge on the 65 benchmark answers (gold only here)
python -m record_engine.evaluate score          # deterministic metrics, no model calls
python -m record_engine.evaluate stability      # rebuild the record from nothing and compare
python -m record_engine.heldout.grade           # grade the held-out answers (references only here)
python -m record_engine diff --before OLD.json    # what changed between two records
python -m record_engine trace HG-E115             # fact or event → rule → evidence → observation
python -m pytest record_engine/tests            # offline, no model calls
```

The API key comes from `ANTHROPIC_API_KEY` or `EHR_ANTHROPIC_API_KEY` (environment or `.env`).
Model outputs are cached under `.local/record_engine/cache`, so re-running costs nothing unless a
prompt or input changes.

## Results (development packet, 31 documents)

**Record, built by code alone.** It reproduces the reference ledger:

- 12 included sessions (5 individual, 5 group, 2 family) on 11 days;
- 585 or 595 minutes: HG-E115 is conflicting (09:00 vs 09:10 start);
- the HG-E110 departure correction supersedes the original roster and its copy (60 minutes);
- the telehealth gap is subtracted (45 minutes);
- weekly goal status: not met, not met, met, cannot determine (partial last week flagged).

Values that a finding's own quote does not state are rejected by validation; those findings take
their encounter's date by a named rule. Mentions the sweep cannot cover after re-extraction are
listed as open items.

**65-question benchmark** (withheld answers count as failures; `make evaluate` writes
`submission/benchmark/metrics.json`):

| | |
|---|---|
| Published | 65/65 (63 answered, 2 partial) |
| Blinded model judge, factual | 119/130 (mean 1.83, 95% interval 1.72–1.92) |
| Exact calculations | 4/4 |
| Citation blocks vs gold lines, micro precision / recall | 0.61 / 0.43 |

**Stability:** a second build from scratch gives an identical episode ledger. 22 of 402
non-text facts differ, none of them counted anywhere (mostly administrative contacts that one
build recorded and the other did not).
`submission/benchmark/README.md` lists the remaining losses.

**Held-out set** (15 questions written from the documents, reported separately): 15/15
published, factual 27/30. One held-out question (HO-02) informed a fix, so the set is not fully
held out. Held-out answers are graded with the same rubric, against references the engine's
author wrote.

**Changed-input scenarios** (`scenarios/`, 13 scenarios with new wording, formats and questions):
record checks 30/30, 14/14 answers published, 13/14 answer checks, judge factual 26/28 (run on
engine 0.2). See
`scenarios/README.md`.

## What the checks cover

Generic behaviours, each with offline tests (`tests/test_engine.py`, `tests/test_inputs.py`):

- **Patient identity.** The record's patient is the MRN most documents state (or `[patient]` in
  the policy); a document stating a different MRN or date of birth is set aside with an
  `other_patient` open item. The identity is a fact (`patient`: name, date of birth, MRN), so
  "the MRN is not documented" is checked against it. Document headers (record number, date of
  birth, document ID) are facts too.
- **Issuers.** Spellings of one organisation are one issuer (`[link] issuer_generic_words`).
  One visit number used by two organisations is two events: the issuer most documents come from
  keeps the plain ID, the other becomes `ID@issuer`. A correction joins the record it corrects
  whatever issuer is written on it.
- **Corrections.** Record time comes from the author's signature (`[precedence]
  authoring_roles`), not a co-signature or receipt stamp. An addendum that names the fields it
  changes is a correction of those fields. A stated duration that restates corrected times falls
  with them, and a corrected account gives no second session length.
- **Attendance.** Appointment status is its own reconciled field (no-show, cancelled by patient /
  clinic / unspecified, partial, not present). Attendance the sources disagree about is a
  scenario in `goal_met()`, so the week is "cannot determine" instead of silently not met. Rows
  carry `delivered` (partial attendance counts), `weekday` and `documents` (the linked-document
  group).
- **Goals.** Only care goals define what counts; an authorization or payer limit does not. With
  no documented care goal, attended visits are `attended_no_goal`. A later plan replaces an
  earlier goal for the same unit and period from its own effective start (`[goals]
  later_supersedes`). `goal_met()` returns each threshold's measured value and outcome
  (`by_threshold`), then `overall`.
- **Formats.** Clock times with seconds and ISO timestamps parse. A re-imported form under
  another form ID is one administration (same instrument, date and score; an open item names both
  IDs).
- **Answer checks.** A stated goal outcome must match the per-threshold result; a weekday next
  to a date must be that date's weekday; a remaining balance the writer worked out is blocked
  unless a result states it; a total the question asks for must come from the "all groups" row
  (or the named week's row for a checklist item about one week); a "not documented" claim is
  looked up in the facts table first. A "missing" quantity the record holds, or a figure no
  query computed, re-plans the question once. When only coverage gaps remain, the answer is
  published as `partial` with the gaps listed.
- **Citations** reached through a cited row's members are pruned to the lines that overlap the
  statement (a shared date, time, record ID or number, or two content words).

## Database and API

The clinical service (`services/clinical/application/engine_runs.py`) runs the engine as durable
runs on the task queue, with leases, idempotency keys, one active run per patient and audit
events:

- a **record build** reads a snapshot's document revisions (integrity checked against the snapshot
  manifest) and stores the reconciled record, the abstraction, and a view for the workspace:
  ledger, weekly goals, totals, facts per event, findings by date, documents and open items, with
  every value's line citations resolved to the snapshot's source spans;
- a **question** is answered over a finished record; each statement's citations are resolved the
  same way.

Model calls run outside database transactions, and the lease is re-checked before a result is
written. The worker builds each patient's latest snapshot automatically; unchanged documents come
from the extraction cache. The endpoints are listed in the repository README.

## Files

| File | Stage |
|---|---|
| `ingest.py` | ① lines and blocks |
| `pipeline.py`, `llm.py`, `model.py` | observation I/O, model calls and cache, data model |
| `extract.py` | ② prompt (generated from the policy), schema, targeted re-extraction |
| `crosscheck.py` | ②' second reading, comparison, focused re-read |
| `validate.py`, `values.py`, `dates.py` | ③ grounding checks and recall sweep |
| `link.py` | ④ events and copy detection |
| `reconcile.py` | ⑤ facts, creditable minutes, disposition, open items |
| `changes.py` | diff between records, trace of a fact to its sources |
| `evaluate.py`, `text_metrics.py` | benchmark judge and deterministic metrics |
| `heldout/` | 15 held-out questions, references (grader only) and `grade.py` |
| `query.py` | ⑦ query language and scenario arithmetic |
| `evidence.py` | passage search and absence verification |
| `qa.py` | ⑥ ⑧ ⑨ ⑩ plan, answer, checks, repair/withhold, framing |
| `render.py` | abstraction.md, answers.md |
| `__main__.py` | command line: observe, build, ask, add, diff, trace |
| `policy.toml`, `policy.py` | all domain knowledge |
| `../submission/` | outputs on the development packet |

## Tests

`tests/test_engine.py` covers the stages on a synthetic physical-therapy patient (Tuesday weeks,
other ID formats); `tests/test_inputs.py` covers changed inputs and the answer checks on that
patient; `tests/test_crosscheck.py` and `tests/test_framing.py` cover the cross-check and framing
with fake readings and framings; `tests/test_text_metrics.py` covers the secondary metrics.
`tests/test_metamorphic.py` changes the real record (a frozen extraction,
`tests/observations.jsonl`) the way records differ and checks the result changes exactly as it
should:

| Change | Expected |
|---|---|
| D111's signature time removed | HG-E115 stays 40 or 50 (timing unknown cannot rank) |
| D111 ends 09:40 and states 30 minutes | HG-E115 is 30 or 50 (never 40) |
| a second note gives a different HG-E102 break | 40 or 45 (breaks are scenarios, not both subtracted) |
| query window ends mid-week | that week is cannot determine, not not met |
| query without the disposition filter | goal status unchanged (the goal applies its own services and dates) |
| a byte-identical copy of a note added | nothing changes but the document list |
| the correction BH-D103 removed | HG-E110 departure back to 11:30, 75 minutes |
| the correction's relation removed | the departure is conflicting, not corrected |

## Known limits

- **Evaluation:** one graded run (a spread of about ±2 factual points between runs), and the
  judge is a model whose grades were not adjudicated by a clinician. There is one synthetic
  patient, so every result comes from a single record. Confidence intervals resample questions
  that share encounters and are exploratory. The held-out references were written by the
  engine's author, not independently.
- **Extraction variance:** two readings compared by code catch what one reading gets wrong at
  random, but not an error both readings share. The code-derived checks (partial attendance and
  arrival from the times, one issuer for an organisation and its units) cover known cases; the
  stability check measures what is left. Ten disputed points in the development packet remain
  open, mostly dates and times of outreach calls.
- **Record-linking questions:** asked which records document the same event (DEV-61), the answer
  lists unresolved candidate links rather than each encounter's linked-document group, which the
  record holds.
- `policy.toml` is TOML so the standard library reads it (no YAML dependency).
- The service vocabulary in the policy is the one domain-specific list. Unmatched service text
  is kept as written.
- The query language covers counting, grouping by week/service/date, scenario sums,
  change/percent and goal status. Anything outside it is marked unanswerable instead of being
  guessed.
