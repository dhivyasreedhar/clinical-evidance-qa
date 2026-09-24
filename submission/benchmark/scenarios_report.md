# Scenario run

Record checks passed: 30/30. Answers published: 14/14; answer checks passed: 13/14; judge factual 26/28.

| Scenario | Record checks | Answers | Cost | Time |
|---|---|---|---|---|
| S01 Late-entry addendum resolves the HG-E115 conflict (12-hour times, abbreviations, /s/ signature) | 3/3 | 2/2 | $0.26 | 92.4 s |
| S02 New session arrives in a CSV scheduling export (US dates, 12-hour times) | 2/2 | 1/1 | $0.14 | 45.0 s |
| S03 Family session documented only by a stated length ('1 hr 15 min'), day-month date format | 3/3 | 1/1 | $0.27 | 86.2 s |
| S04 E-mail correction: the January 22 attendance row belonged to another patient | 3/3 | 1/1 | $0.20 | 95.7 s |
| S05 OCR-damaged unsigned draft gives a shorter duration | 2/2 | 1/1 | $0.13 | 50.3 s |
| S06 Paid claim line (835 remittance) for a cancelled appointment | 2/2 | 1/1 | $0.15 | 78.4 s |
| S07 A different patient's note is in the folder | 3/3 | 1/1 | $0.14 | 54.3 s |
| S08 Another organisation uses the same visit number HG-E115 | 3/3 | 1/1 | $0.23 | 137.2 s |
| S09 The signed treatment plan is withdrawn (no documented goal) | 2/2 | 1/1 | $0.19 | 58.5 s |
| S10 Plan amendment raises the weekly minute goal to 180 from 19 Jan (day-month dates) | 2/2 | 1/1 | $0.62 | 179.2 s |
| S11 Video session with a JSON platform log (seconds, ISO timestamps, dropped call) | 2/2 | 1/1 | $0.24 | 140.3 s |
| S12 Measures import with a re-imported form and a score after the review period | 1/1 | 0/1 | $0.13 | 63.8 s |
| S13 Equal-standing note says the patient was a no-show for HG-E113 | 2/2 | 1/1 | $0.26 | 75.8 s |

## S01: Late-entry addendum resolves the HG-E115 conflict (12-hour times, abbreviations, /s/ signature)

- PASS `{"type": "fact", "subject": "HG-E115", "field": "minutes", "value": 50, "status": ["established"]}` → got `{"value": 50.0, "scenarios": [], "status": "established"}`
- PASS `{"type": "total", "sessions": 12, "days": 11, "minutes": [595]}` → got `{"sessions": 12, "days": 11, "minutes": [595.0]}`
- PASS `{"type": "week", "start": "2026-01-26", "status": "met"}` → got `{"by_threshold": [{"threshold": "at least 3 days", "measured": 3.0, "outcome": "met"}, {"threshold": "at least 150 minutes", "measured": 155.0, "outcome": "met"}], "overall": "met", "status": "met", "checks": [{"unit": "days", "threshold": 3.0, "comparator": "at_least", "measured": 3.0, "outcome": "`

**S01-Q1 (PASS, answered)** How many patient-present therapy minutes did Rowan receive in the week of January 26 to February 1, 2026, and was the weekly treatment-plan goal met?

> Rowan received 155 patient-present therapy minutes in the week of January 26–February 1, 2026, across three attended sessions: 50 minutes of individual therapy on January 26, 75 minutes of group therapy on January 29, and 30 minutes of family therapy on January 30. The weekly treatment-plan goal (at least 150 patient-present therapy minutes per week) was met: the 150-minute threshold measured 155 minutes (met). Note that the goal's episode end date is January 30, 2026, so the check covers January 26–30 as a partial week; all three counted sessions fell within that window. Three encounters were not counted toward the goal: the January 27 group session (no-show), the January 28 individual session (cancelled by patient), and the January 30 medication management visit (service type excluded from the goal).
- judge: factual 2, evidence 2; []

**S01-Q2 (PASS, answered)** What was Rowan's total patient-present therapy time for the whole episode, in minutes and hours?

> Rowan's total patient-present therapy time for the whole episode (all 12 attended, goal-eligible therapy visits from 2026-01-05 to 2026-01-30, covering individual, group, and family psychotherapy) was 595 minutes, or 9 hours 55 minutes.
- judge: factual 2, evidence 1; []

## S02: New session arrives in a CSV scheduling export (US dates, 12-hour times)

- PASS `{"type": "fact", "subject": "HG-E121", "field": "minutes", "value": 45}` → got `{"value": 45.0, "scenarios": [], "status": "documented"}`
- PASS `{"type": "total", "sessions": 13, "days": 12, "minutes": [630, 640]}` → got `{"sessions": 13, "days": 12, "minutes": [630.0, 640.0]}`

**S02-Q1 (PASS, answered)** How many individual psychotherapy sessions did Rowan attend during the episode, and on which dates?

> Rowan attended 6 individual psychotherapy sessions during the episode, on January 5, January 14, January 19, January 21, January 26, and January 27, 2026. One additional individual psychotherapy appointment (January 8) was a no-show, and one (January 28) was cancelled by Rowan before the appointment; neither counts as an attended session.
- judge: factual 2, evidence 2; []

## S03: Family session documented only by a stated length ('1 hr 15 min'), day-month date format

- PASS `{"type": "fact", "subject": "HG-E122", "field": "minutes", "value": 75}` → got `{"value": 75.0, "scenarios": [], "status": "documented"}`
- PASS `{"type": "total", "sessions": 13, "days": 12, "minutes": [660, 670]}` → got `{"sessions": 13, "days": 12, "minutes": [660.0, 670.0]}`
- PASS `{"type": "week", "start": "2026-01-19", "status": "met"}` → got `{"by_threshold": [{"threshold": "at least 3 days", "measured": 4.0, "outcome": "met"}, {"threshold": "at least 150 minutes", "measured": 255.0, "outcome": "met"}], "overall": "met", "status": "met", "checks": [{"unit": "days", "threshold": 3.0, "comparator": "at_least", "measured": 4.0, "outcome": "`

**S03-Q1 (PASS, answered)** How much family therapy did Rowan receive, session by session and in total?

> Rowan received family therapy in three sessions: January 9 (45 minutes), January 23 (75 minutes), and January 30 (30 minutes). The total family therapy minutes received across all three sessions was 150 minutes. On January 30, Rowan joined the session at 13:15 and participated through the end at 13:45; the first 15 minutes (13:00–13:15) were partner-only time and are not counted in Rowan's 30 credited minutes, though the full therapist session ran 45 minutes.
- judge: factual 2, evidence 2; []

## S04: E-mail correction: the January 22 attendance row belonged to another patient

- PASS `{"type": "fact", "subject": "HG-E113", "field": "disposition", "value": "excluded"}` → got `{"value": "excluded", "scenarios": [], "status": "established"}`
- PASS `{"type": "total", "sessions": 11, "days": 10, "minutes": [540, 550]}` → got `{"sessions": 11, "days": 10, "minutes": [540.0, 550.0]}`
- PASS `{"type": "week", "start": "2026-01-19", "status": "not_met"}` → got `{"by_threshold": [{"threshold": "at least 3 days", "measured": 2.0, "outcome": "not_met"}, {"threshold": "at least 150 minutes", "measured": 135.0, "outcome": "not_met"}], "overall": "not_met", "status": "not_met", "checks": [{"unit": "days", "threshold": 3.0, "comparator": "at_least", "measured": 2`

**S04-Q1 (PASS, answered)** Did Rowan attend the January 22 skills group, and what does that mean for the weekly goal in the week of January 19 to 25?

> Rowan did not attend the January 22 skills group. The attendance register initially recorded an arrival at 10:30 and departure at 11:30, but a signed correction established that this register row was entered in error and belongs to a different group member; there was no patient contact for Rowan on January 22. For the full week of January 19–25, the weekly goals were not met on either threshold. The three included visits (group and individual on January 19, individual on January 21) covered only 2 distinct therapy days against the threshold of at least 3 days (not met), and totaled 135 minutes against the threshold of at least 150 minutes (not met). Overall status: not met. Because Rowan did not attend, the January 22 group encounter is excluded from goal-eligible visits and does not count toward either weekly threshold.
- judge: factual 2, evidence 2; []

## S05: OCR-damaged unsigned draft gives a shorter duration

- PASS `{"type": "fact", "subject": "HG-E107", "field": "minutes", "value": 45}` → got `{"value": 45.0, "scenarios": [], "status": "established"}`
- PASS `{"type": "total", "sessions": 12, "days": 11, "minutes": [585, 595]}` → got `{"sessions": 12, "days": 11, "minutes": [585.0, 595.0]}`

**S05-Q1 (PASS, answered)** How long was the January 14 individual session, and is there any conflicting account of its length?

> The January 14 individual session_minutes are either 30 or 45 minutes — the record is conflicting. The signed therapy note records an 11:00–11:45 patient-present session (45 minutes), while a draft note records the session as 11:00–11:30 (30 minutes); the two accounts are unresolved.
- judge: factual 1, evidence 2; ['Fails to resolve the conflict: the signed final note (45 min) outranks the unsigned auto-saved draft (30 min), so 45 minutes stands as the authoritative record. The answer treats the two accounts as equally unresolved, which loses the required uncertainty-resolution.']

## S06: Paid claim line (835 remittance) for a cancelled appointment

- PASS `{"type": "fact", "subject": "HG-E117", "field": "disposition", "value": "excluded"}` → got `{"value": "excluded", "scenarios": [], "status": "established"}`
- PASS `{"type": "total", "sessions": 12, "days": 11, "minutes": [585, 595]}` → got `{"sessions": 12, "days": 11, "minutes": [585.0, 595.0]}`

**S06-Q1 (PASS, answered)** A paid claim exists for the January 28 individual appointment. Was that session delivered, and does it count toward Rowan's therapy minutes?

> The January 28 individual session (scheduled 14:00–14:45) was not delivered. Rowan cancelled before the appointment start, citing a personal scheduling conflict, and is recorded as not attended. Because Rowan did not attend, the session is excluded and does not count toward the therapy minutes goal. Although a paid claim (code 90834, $160.00) exists for this date, the clinical record documents a patient cancellation with no service delivered.
- judge: factual 2, evidence 2; []

## S07: A different patient's note is in the folder

- PASS `{"type": "no_event", "id": "HG-E201"}` → got `[]`
- PASS `{"type": "open_item", "kind": "other_patient", "min": 1}` → got `["S07_other_patient_note was set aside: MRN HG-M999 is not the record's patient (HG-M042); date of birth 1985-02-02 is not the record's patient (1991-04-12). None of its content is in this record."]`
- PASS `{"type": "total", "sessions": 12, "days": 11, "minutes": [585, 595]}` → got `{"sessions": 12, "days": 11, "minutes": [585.0, 595.0]}`

**S07-Q1 (PASS, answered)** How many therapy sessions did Rowan attend in the week of January 19 to 25, and how many patient-present minutes?

> Rowan attended 4 therapy sessions in the week of January 19–25 (a group and an individual session on January 19, an individual session on January 21, and a group session on January 22), totaling 180 patient-present minutes. A fifth encounter that week (January 23, care coordination) is excluded from both counts because Rowan did not participate — the contact was between the clinician and an outside social worker only, with no patient contact.
- judge: factual 2, evidence 2; []

## S08: Another organisation uses the same visit number HG-E115

- PASS `{"type": "fact", "subject": "HG-E115", "field": "service", "value": "individual"}` → got `{"value": "individual", "scenarios": [], "status": "corroborated"}`
- PASS `{"type": "fact", "subject": "HG-E115", "field": "minutes", "scenarios": [40, 50]}` → got `{"value": null, "scenarios": [40.0, 50.0], "status": "conflicting"}`
- PASS `{"type": "total", "sessions": 12, "days": 11, "minutes": [585, 595]}` → got `{"sessions": 12, "days": 11, "minutes": [585.0, 595.0]}`

**S08-Q1 (PASS, answered)** What happened at encounter HG-E115 on January 26, 2026?

> Encounter HG-E115 on January 26, 2026 was an individual psychotherapy session delivered in person, attended by the patient and counted as included toward the goal. Clinical notes document: ongoing anxiety, low mood, and functional difficulty around work demands; uneven sleep with repetitive work-related thoughts at night; difficulty moving from a supervisor's reply to scheduling a follow-up conversation; continued postponement of choosing a meeting time; worry about being asked for commitments; a tendency to over-edit messages; and anticipation of becoming overwhelmed if multiple work issues arose at once. No suicidal ideation was reported. The patient was attentive, collaborative, and expressed a wish to resume a steadier routine. Interventions included role-play to rehearse a brief, focused response to the supervisor's request (identifying when the patient shifted into apologizing or over-explaining), a grounding exercise using chair contact and feet on the floor, and rehearsal of requesting a brief initial conversation with a specific purpose. Nora Ellis participated directly in the clinical work and helped rehearse a grounding cue. The patient could use the grounding cue during rehearsal but remained uncertain about independent use when anxious; with prompting, the patient was able to return to the main request during role-play. Plan: continue work on avoidance and the bedtime routine, maintain scheduled treatment contact during return-to-work planning, and bring the resp
- judge: factual 2, evidence 2; []

## S09: The signed treatment plan is withdrawn (no documented goal)

- PASS `{"type": "fact", "subject": "HG-E101", "field": "disposition", "value": "attended_no_goal"}` → got `{"value": "attended_no_goal", "scenarios": [], "status": "established"}`
- PASS `{"type": "fact", "subject": "HG-E106", "field": "disposition", "value": "attended_no_goal"}` → got `{"value": "attended_no_goal", "scenarios": [], "status": "established"}`

**S09-Q1 (PASS, answered)** Did Rowan meet the weekly therapy goal in the week of January 19 to 25?

> Because no weekly therapy goal exists, goal status by threshold cannot be determined: there is no weekly threshold to measure against. The goal computation confirms no_goal for this week. No documented care goal specifies a weekly therapy session threshold for the week of January 19–25. The only active goal covering that period is an episode-level authorization permitting at most 8 outpatient therapeutic group sessions across the entire episode (January 5–30, 2026); it sets no weekly minimum or target and does not constitute a weekly therapy goal. The record does not document a weekly therapy goal for the week of January 19–25. Documentation of a care plan or treatment goal specifying eligible service types and a weekly session threshold would be needed to determine whether Rowan met such a goal.
- judge: factual 2, evidence 2; []

## S10: Plan amendment raises the weekly minute goal to 180 from 19 Jan (day-month dates)

- PASS `{"type": "week", "start": "2026-01-12", "status": "not_met"}` → got `{"by_threshold": [{"threshold": "at least 3 days", "measured": 2.0, "outcome": "not_met"}, {"threshold": "at least 150 minutes", "measured": 120.0, "outcome": "not_met"}], "overall": "not_met", "status": "not_met", "checks": [{"unit": "minutes", "outcome": "not_applicable", "facts": ["F-a588772a", "`
- PASS `{"type": "week", "start": "2026-01-19", "status": "met"}` → got `{"by_threshold": [{"threshold": "at least 180 minutes", "measured": 180.0, "outcome": "met"}, {"threshold": "at least 3 days", "measured": 3.0, "outcome": "met"}], "overall": "met", "status": "met", "checks": [{"unit": "minutes", "threshold": 180.0, "comparator": "at_least", "measured": 180.0, "outc`

**S10-Q1 (PASS, answered)** Using the treatment goals in effect in each week, was the weekly minute goal met in the week of January 19 to 25 and in the week of January 26 to February 1?

> Week of January 19–25: the weekly minute goal (at least 150 minutes per the January 5 plan, which was in effect for this week) was met. The four attended, goal-eligible therapy sessions — group therapy on January 19 (HG-E110, 60 min), individual therapy on January 19 (HG-E111, 30 min), individual therapy on January 21 (HG-E112, 45 min), and group therapy on January 22 (HG-E113, 45 min) — totaled 180 minutes, meeting the at-least-150-minute threshold. The at-least-3-therapy-days threshold was also met (3 distinct days). Overall goal status: met. Week of January 26–February 1: the weekly minute goal (at least 180 minutes per the January 19 amendment, which replaced the prior minute goal effective January 19) cannot be determined. The three attended, goal-eligible therapy sessions — individual therapy on January 26 (HG-E115, 40 or 50 minutes due to a conflicting start-time record), group therapy on January 29 (HG-E118, 75 min), and family therapy on January 30 (HG-E119, 30 min) — total either 145 or 155 minutes, both below 180. However, the review period ends January 30 and the week runs through February 1, so sessions on January 31 and February 1 are not in the record; the goal cannot be determined for this partial week. The at-least-3-therapy-days threshold was met (3 distinct days). The three excluded encounters in the week of January 26–February 1 were correctly omitted from the goal-eligible count: HG-E116 (January 27, group therapy) was a no-show — the patient did not atte
- judge: factual 1, evidence 2; ["Week of Jan 19–25: candidate states the 150-minute goal (Jan 5 plan) was in effect and met, but the amendment signed 19 Jan 2026 replaced the minute goal effective 19 Jan 2026, so the 180-minute goal was already in effect for that entire week; the correct conclusion is that 180 minutes were accumulated and the 180-minute goal was met — the candidate reaches the right 'met' outcome but for the wrong reason (citing the superseded 150-minute threshold)", "Week of Jan 26–Feb 1: candidate says goal 'cannot be determined' due to partial week, but the reference answer and evidence show the documented sessions (145 or 155 min) are already below 180 in both scenarios, so the minute goal is not met for the documented days; the partial-week caveat is valid but the candidate omits the clear finding that documented minutes fall short"]

## S11: Video session with a JSON platform log (seconds, ISO timestamps, dropped call)

- PASS `{"type": "fact", "subject": "HG-E123", "field": "minutes", "between": [46, 48]}` → got `{"value": 47.0, "scenarios": [], "status": "documented"}`
- PASS `{"type": "total", "sessions": 13, "days": 11}` → got `{"sessions": 13, "days": 11, "minutes": [632.0, 642.0]}`

**S11-Q1 (PASS, answered)** How many minutes of patient contact occurred in the January 29 video session, excluding the dropped connection?

> The January 29 individual video session recorded 47 minutes of patient contact, with the dropped connection (a gap from approximately 15:18 to 15:21 during which there was no therapeutic contact) already excluded from that figure.
- judge: factual 2, evidence 2; []

## S12: Measures import with a re-imported form and a score after the review period

- PASS `{"type": "measurement", "instrument": "PHQ-9", "completed_on": "2026-02-02"}` → got `["M:PHQ-9 2026-02-02"]`

**S12-Q1 (FAIL, answered)** What was Rowan's latest PHQ-9 total within the January 5 to 30 review period, and how much did it change from intake?

> Rowan's latest PHQ-9 total within the January 5–30 review period was 10, recorded on January 30, 2026. Compared to the intake (first) PHQ-9 score of 18 on January 5, the January 30 score of 10 represents a decrease of 8 points.
- missing: ['44\\.4']; forbidden present: []
- judge: factual 2, evidence 2; []

## S13: Equal-standing note says the patient was a no-show for HG-E113

- PASS `{"type": "fact", "subject": "HG-E113", "field": "attendance", "status": ["conflicting"]}` → got `{"value": null, "scenarios": ["not_attended", "attended"], "status": "conflicting"}`
- PASS `{"type": "week", "start": "2026-01-19", "status": "cannot_determine"}` → got `{"by_threshold": [{"threshold": "at least 3 days", "measured": [2.0, 3.0], "outcome": "cannot_determine"}, {"threshold": "at least 150 minutes", "measured": [135.0, 180.0], "outcome": "cannot_determine"}], "overall": "cannot_determine", "status": "cannot_determine", "checks": [{"unit": "days", "thre`

**S13-Q1 (PASS, partial)** Did Rowan attend the January 22 skills group, and can the weekly goal for January 19 to 25 be judged?

> Rowan's attendance at the January 22 skills group is disputed: the attendance register and the facilitator's session note record that Rowan arrived at 10:30 and remained until the group closed (attended, late arrival), while the co-facilitator's separate note states Rowan did not attend and no contact occurred. Sources of equal standing disagree, so attendance is either attended or not attended and cannot be resolved from the record as it stands. The weekly goal for January 19–25 cannot be judged. The three confirmed included encounters (January 19 group, January 19 individual, January 21 individual) cover 2 distinct therapy days and 135 minutes; if the January 22 encounter is also counted, the figures become 3 days and 180 minutes. Days threshold (at least 3): measured 2 or 3 — cannot determine. Minutes threshold (at least 150): measured 135 or 180 — cannot determine. Overall goal status: cannot be determined.
- judge: factual 2, evidence 2; []
