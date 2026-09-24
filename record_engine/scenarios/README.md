# Changed-input scenarios

Thirteen end-to-end scenarios that change the supplied packet the way a reviewer might in the
follow-up call: new wording and formats, corrections, withdrawals, another patient's document, a
shared visit number, a plan amendment, and new questions about each change. None of these
documents or questions were used to develop the engine.

```
python -m record_engine.scenarios.run            # all 13 (≈ $3 at list prices; cached reruns are free)
python -m record_engine.scenarios.run --only S04 S13
python -m record_engine.scenarios.run --judge    # also grade each answer against its reference
```

Each scenario gets its own workspace under `.local/scenarios/<id>/documents` (the supplied
`documents/` folder is never written to). Unchanged documents come from the extraction cache,
so only the new document costs an extraction call. The report is `.local/scenarios/report.md`.

Two kinds of check:

- **Record checks** (deterministic, no model): totals, weekly goal status, a fact's value and
  status, that another patient's visit is absent, that an open item was raised.
- **Answer checks** (deterministic): the answer is published, contains what it must
  (`must`, regular expressions) and not what it must not (`must_not`). `--judge` adds the
  held-out judge against the written reference; it is advisory.

| ID | Change | Format being tested | Expected record |
|---|---|---|---|
| S01 | Addendum corrects HG-E115 arrival to 9:00 | late entry, 12-hour times, abbreviations, `/s/` signature | HG-E115 = 50 (established); 595 min; week 4 met |
| S02 | New session HG-E121 on 01/27 | CSV scheduling export, US dates, 2:00 PM | 13 sessions, 12 days, 630 or 640 |
| S03 | New family session, length only | "1 hr 15 min", "23 January 2026" | HG-E122 = 75; week 3 met |
| S04 | Attendance entered for the wrong patient | e-mail correction | HG-E113 excluded; 11 sessions; week 3 not met |
| S05 | Draft says 30 min for HG-E107 | OCR errors (0/O, l/I), unsigned draft | HG-E107 stays 45 |
| S06 | Paid claim for a cancelled visit | 835 remittance line | HG-E117 stays excluded |
| S07 | Another patient's note | same clinic, different MRN | set aside; totals unchanged |
| S08 | Another clinic reuses HG-E115 | other organisation's visit | HG-E115 unchanged |
| S09 | Treatment plan withdrawn | removal | visits `attended_no_goal`; no goal status |
| S10 | Minute goal raised to 180 from 19 Jan | plan amendment, day-month dates | week 3 met under 180 |
| S11 | New video session with call log | JSON, ISO timestamps with seconds | HG-E123 ≈ 47 min |
| S12 | Re-imported form + score after the period | measures table | Feb 2 score exists; not "latest in period" |
| S13 | Equal-standing no-show note for HG-E113 | co-facilitator note | attendance conflicting; week 3 cannot determine |

Validated offline: with hand-written observations standing in for extraction, every record
check passes, and the checks for S07, S08, S09 and S13 fail on an engine without the matching
fixes, so they detect the bugs they were written for. A live run also tests extraction of the
new formats and the answers.

**Results** (run on engine 0.2)**:** 30/30 record checks, 14/14 answers published, 13/14 answer checks, judge factual
26/28, $2.96 cold. The one failed check is S12: the answer gives the PHQ-9 change as 8 points
(judge 2/2), and the check also expects the percentage.

The judge sees each scenario's changed documents and what each answer cites.
