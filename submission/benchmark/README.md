# Benchmark results

The 65-question development benchmark (`clinical_qa_benchmark/`) on the 31 supplied documents,
run on `record-engine-0.3` with policy-2. Only the evaluator (`python -m record_engine.evaluate`)
reads the gold data. A withheld answer counts as a failure in every denominator. Every model call
ran at temperature 0 except the independent second reading of each document. The answers were
produced before the 90-second answer budget and the latest answer-check fixes. DEV-01 to DEV-05
were re-run cold on the current code afterwards (`../dev01-05_answers.md`): all five published in
47–76 s (DEV-01 as partial), factual 2 and evidence 2 on all five; the DEV-01 and DEV-05 losses
below are fixed in that run.

| | |
|---|---|
| Published | 65/65 (63 answered, 2 partial) |
| Blinded model judge, factual (0–2) | 1.83 (119/130), 95% interval 1.72–1.92 (exploratory) |
| Published and fully correct (factual 2) | 55/65 |
| Judge, evidence (0–2) | 1.92 |
| Exact calculations (4 structured gold answers, 55 fields) | 4/4 |
| Citation blocks vs gold source lines, micro precision / recall / F1 | 0.61 / 0.43 / 0.50 |
| Citation blocks, macro precision / recall / F1 | 0.71 / 0.53 / 0.56 |
| ROUGE-1 / ROUGE-L / BLEU-4 (secondary; measures wording overlap only) | 0.35 / 0.23 / 0.052 |

For each question the judge sees the question, the reference answer, the required facts, the gold
source excerpts, and the answer. Each statement comes with the source lines behind it, which the
grader copies from the documents, including the records behind each cited query row. The judge is
told this cited text is genuine even when it is not among the reference excerpts.

**Stability** (`stability.json`): the record was built a second time from scratch, with every
model call fresh, and compared with this one. The episode ledger is identical: every count,
total, weekly result and encounter contribution. Of 402 non-text facts, 22 differ. None of them
is counted anywhere: they are mostly administrative contacts that one build recorded and the
other did not, or a difference in how strongly a value is confirmed (one source vs several).

**Cross-check of the two readings:** in the main build the two readings of the documents
disagreed on 40 points. A focused re-read settled 30, and the other 10 stay as open items (mostly
dates and times of outreach calls in the missed-visit log).

**Lost points (11):**

- **DEV-61 (0):** asked which records document the same event, the answer lists the unresolved
  candidate links rather than each encounter's group of linked documents, which the record holds.
- **Scored 1:**
  - DEV-01: adds a count of all attended visits including medication visits (14 on 12 days),
    which was not asked for.
  - DEV-05: does not say that the January 26 import repeats the January 16 form.
  - DEV-19: adds the week's therapy minutes, which the question did not ask about.
  - DEV-31: labels the 375 minutes of patient presence as session running time.
  - DEV-49: describes a January 13 medication-review statement as a safety finding.
  - DEV-56: applies a January 19 statement to the early-January sessions.
  - DEV-58: gives a different third example from the reference.
  - DEV-59: gets the January 19 case of the "latest document wins" rule wrong (the resent copy
    still shows 11:30).
  - DEV-60: gives the strongest weekly conclusion for the wrong week.

**Held-out set** (15 questions, reported separately in `heldout_grades.json`): 15/15 published,
factual 26/30. The losses:

- HO-03 counts the coordination call among the appointments not delivered.
- HO-05 leaves out the 15 partner-only minutes of January 30.
- HO-06 is marked down for naming the January 19 individual clinician, who is correctly named in
  BH-D105 (a grader error).
- HO-10 gives the day count without listing the days.

A regrade after these results were known, with the same evidence the development judge sees, gave
27/30; the first grading is the reported result.

HO-02 informed an earlier fix, so the set is not fully held out.

**Changed-input scenarios:** `scenarios_report.md` comes from an earlier engine version (0.2) and
was not re-run for this version.

**Citations:** the unit of citation is a document block (a paragraph or a table row), and the
gold set is every block that overlaps a gold source line range. Answers cite the records behind
each row they use, so a statement about one encounter often cites every document that records
it, which lowers precision. Recall is lower because on-point answers cite only what their
statements need.

## Cost and time

`../run_stats.json` gives two views. `this_run` is what the last run paid: cached calls are free
and near instant, and it says whether its timing was cold, cached or partly cached. `cold` is
what the answers would cost and take to produce from scratch.

| Run | Cold cost | Cold time |
|---|---|---|
| Extraction with cross-check, 31 documents | $3.92 | about 7 minutes in total |
| 65 questions | $12.58 (≈ $0.19 each) | median 42 s, max 152 s per question |
| 15 held-out questions | $2.12 (≈ $0.14 each) | median 31 s, max 69 s per question |

## Limitations

- One graded run, graded by a model and not adjudicated by a clinician.
- A single synthetic patient.
- The intervals resample questions that share encounters, so they are exploratory.
- The engine's author wrote the held-out references, and HO-02 informed a fix.

## Files

- `metrics.json`: deterministic metrics and the judge summary.
- `grades.json`: the judge's grade for each question.
- `stability.json`: the second build's comparison, fact by fact.
- `heldout_answers.json`, `heldout_grades.json`, `heldout_run_stats.json`: the held-out set.
- `scenarios_report.md`, `scenarios_report.json`: changed-input scenarios (engine 0.2).
- `../answers.md`: all 65 answers.
- `../dev01-05_answers.md`: DEV-01 to DEV-05 from the current code's cold re-run, with source lines and grades.
- `../logs/run.log`: this run's log. `../logs/dev01-05_run.log`, `../logs/dev01-05_trace.md`,
  `../logs/dev01-05_answers.json`, `../logs/dev01-05_grades.json`: the DEV-01 to DEV-05 re-run.
- `../extraction_stats.json`: the cross-check report (every disputed point and how it ended).
