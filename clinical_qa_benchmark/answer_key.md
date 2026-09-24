# Rowan Mercer: questions and ground truth

65 questions grounded in 31 supplied documents. DEV-01–DEV-05 preserve the example questions verbatim. Sources use one-based lines in the original text files. Full verbatim evidence excerpts are in ground_truth.json.

The last calendar week ends February 1; this benchmark includes only review-period services through January 30. The January 26 duration conflict is intentionally unresolved.

## DEV-01 · episode abstraction

For January 5–30, 2026, how many therapy sessions did Rowan attend, by service type and in total, and on how many distinct days? Provide a reviewable abstraction with source support and explain records that could lead to duplicate or ineligible counts.

**Difficulty:** hard · **Answerability:** determinate

**Ground truth**

Rowan attended 12 patient-present psychotherapy encounters: 5 individual (January 5, 14, 19, 21, 26), 5 group (January 6, 12, 19, 22, 29), and 2 family (January 9, 30), on 11 distinct dates. January 19 contains two different therapy encounters on one day. The two January 9 notes describe one family encounter; the two January 26 notes describe one individual encounter despite their unresolved duration conflict; the January 21 video calls are one encounter. Exclude January 8 and 27 no-shows, January 15 clinic cancellation, January 28 patient cancellation, January 16 partner-only collateral, January 23 professional coordination, both medication visits, questionnaire reviews/imports, the resent roster and correction as new services, and authorization/charge/template records as evidence of additional attendance. The January 27 posted charge and draft do not outweigh the signed no-show attestation.

**Required facts for grading**

- Individual 5, group 5, family 2; total 12.
- 11 distinct therapy dates; January 19 counts twice as encounters but once as a day.
- Deduplicate January 9, January 21 and January 26 by encounter; duration uncertainty does not alter attendance counts.
- Exclude absent-patient, administrative, medication-only and cancelled/no-show contacts using patient-specific evidence.

**Failure modes:** document count as visit count, call count as session count, authorization as attendance, billing as attendance, absent patient included, same day deduplication error.

**Evidence**

- BH-D002 · `intake_and_individual_jan05.txt` · lines 6–8
- BH-D004 · `group_facilitator_jan06.txt` · lines 12
- BH-D005 · `early_group_attendance_roster.txt` · lines 9–11
- BH-D007 · `family_primary_jan09.txt` · lines 6–9
- BH-D008 · `family_cofacilitator_jan09.txt` · lines 6–9
- BH-D009 · `group_facilitator_jan12.txt` · lines 12
- BH-D011 · `individual_therapy_jan14.txt` · lines 6–8
- BH-D101 · `BH-D101_group_content_2026-01-19.txt` · lines 6–8
- BH-D103 · `BH-D103_attendance_correction_2026-01-20.txt` · lines 7–11
- BH-D105 · `BH-D105_individual_2026-01-19.txt` · lines 3–6
- BH-D106 · `BH-D106_telehealth_2026-01-21.txt` · lines 3–7
- BH-D107 · `BH-D107_group_activity_records_2026-01-22_and_29.txt` · lines 7–17
- BH-D108 · `BH-D108_final_attendance_and_cancellation_register.txt` · lines 8–20
- BH-D110 · `BH-D110_individual_primary_record_2026-01-26.txt` · lines 3–7
- BH-D111 · `BH-D111_individual_second_record_2026-01-26.txt` · lines 4–10
- BH-D113 · `BH-D113_family_therapy_2026-01-30.txt` · lines 3–7
- BH-D001 · `group_authorization_letter.txt` · lines 10–15
- BH-D010 · `medication_review_jan13.txt` · lines 17
- BH-D012 · `partner_collateral_jan16.txt` · lines 6–17
- BH-D013 · `symptom_measure_review_jan16.txt` · lines 15
- BH-D014 · `imported_measure_summary_received_jan26.txt` · lines 17–19
- BH-D015 · `missed_visit_outreach_jan08.txt` · lines 9–17
- BH-D016 · `group_cancellation_notice_jan15.txt` · lines 9–15
- BH-D104 · `BH-D104_resent_roster_received_2026-01-26.txt` · lines 8–20
- BH-D109 · `BH-D109_care_coordination_2026-01-23.txt` · lines 5–13
- BH-D112 · `BH-D112_draft_note_and_charge_extract_2026-01-27.txt` · lines 7–25
- BH-D114 · `BH-D114_medication_management_2026-01-30.txt` · lines 5–12
- BH-D115 · `BH-D115_symptom_measure_review_2026-01-30.txt` · lines 14
- BH-D003 · `signed_treatment_plan_jan05.txt` · lines 12

## DEV-02 · time aggregation

How many therapy minutes and hours did Rowan actually receive during the review period, overall and for each Monday–Sunday week? Show calculations or supporting detail, and report any conclusion the available documents do not settle.

**Difficulty:** hard · **Answerability:** partially_determinate

**Ground truth**

The documented patient-present therapy total is 585 minutes (9 hours 45 minutes; 9.75 hours) if January 26 lasted 40 minutes, or 595 minutes (9 hours 55 minutes; approximately 9.9167 hours) if it lasted 50. The 10-minute conflict is unresolved; these are two source-supported scenarios, not an exact reconciled total. Monday–Sunday weeks: January 5–11 = 50+45+45 = 140 minutes (2h20m); January 12–18 = 75+45 = 120 (2h); January 19–25 = 60+30+45+45 = 180 (3h); January 26–February 1, counting services in the review period through January 30, = (40 or 50)+75+30 = 145 or 155 (2h25m or 2h35m). Individual totals are 210 or 220 minutes, group 300, family 75. Use actual patient participation, subtract nontherapeutic breaks/disconnection, and never sum concurrent clinician durations.

**Required facts for grading**

- Total is 585 or 595 minutes, conditional on the unresolved January 26 conflict.
- Weekly totals are 140, 120, 180, and 145 or 155.
- Hours conversions preserve minutes; 595 minutes is not 9.95 hours.
- No services beyond January 30 are inferred for the last calendar week.

**Failure modes:** false precision, scheduled duration as treatment, breaks included, clinician minutes summed, wrong week boundary, hours conversion error.

**Evidence**

- BH-D002 · `intake_and_individual_jan05.txt` · lines 6–8
- BH-D004 · `group_facilitator_jan06.txt` · lines 12
- BH-D005 · `early_group_attendance_roster.txt` · lines 9–11
- BH-D007 · `family_primary_jan09.txt` · lines 6–9
- BH-D008 · `family_cofacilitator_jan09.txt` · lines 6–9
- BH-D009 · `group_facilitator_jan12.txt` · lines 12
- BH-D011 · `individual_therapy_jan14.txt` · lines 6–8
- BH-D101 · `BH-D101_group_content_2026-01-19.txt` · lines 6–8
- BH-D103 · `BH-D103_attendance_correction_2026-01-20.txt` · lines 7–11
- BH-D105 · `BH-D105_individual_2026-01-19.txt` · lines 3–6
- BH-D106 · `BH-D106_telehealth_2026-01-21.txt` · lines 3–7
- BH-D107 · `BH-D107_group_activity_records_2026-01-22_and_29.txt` · lines 7–17
- BH-D108 · `BH-D108_final_attendance_and_cancellation_register.txt` · lines 8–20
- BH-D110 · `BH-D110_individual_primary_record_2026-01-26.txt` · lines 3–7
- BH-D111 · `BH-D111_individual_second_record_2026-01-26.txt` · lines 4–10
- BH-D113 · `BH-D113_family_therapy_2026-01-30.txt` · lines 3–7
- BH-D003 · `signed_treatment_plan_jan05.txt` · lines 6–12

## DEV-03 · goal evaluation

For each week, did the delivered therapy meet the goal documented in Rowan’s treatment plan? State the goal, the relevant therapy-day and minute totals, and whether it was met, not met, or cannot be determined from the current record.

**Difficulty:** hard · **Answerability:** partially_determinate

**Ground truth**

The individualized local goal requires BOTH at least 3 therapy days and at least 150 patient-present therapy minutes per Monday–Sunday week. January 5–11: 3 days/140 minutes, not met because minutes are short. January 12–18: 2 days/120 minutes, not met on both criteria. January 19–25: 3 days/180 minutes, met. January 26–February 1 (review-period services through January 30): 3 days/145 or 155 minutes, cannot determine overall; the day goal is met, while the minute goal fails under the 40-minute January 26 record and passes under the 50-minute record. No final reconciliation or additional January 31–February 1 services are documented in the supplied episode records.

**Required facts for grading**

- Goal is conjunctive: >=3 distinct days AND >=150 eligible minutes.
- Weekly statuses: not met, not met, met, cannot determine.
- Last week has 3 days in either duration scenario; only its minute threshold is unresolved.
- The threshold is a local individualized treatment-plan goal.

**Failure modes:** and or error, session count as day count, uncertainty collapsed, external standard invented.

**Evidence**

- BH-D002 · `intake_and_individual_jan05.txt` · lines 6–8
- BH-D004 · `group_facilitator_jan06.txt` · lines 12
- BH-D005 · `early_group_attendance_roster.txt` · lines 9–11
- BH-D007 · `family_primary_jan09.txt` · lines 6–9
- BH-D008 · `family_cofacilitator_jan09.txt` · lines 6–9
- BH-D009 · `group_facilitator_jan12.txt` · lines 12
- BH-D011 · `individual_therapy_jan14.txt` · lines 6–8
- BH-D101 · `BH-D101_group_content_2026-01-19.txt` · lines 6–8
- BH-D103 · `BH-D103_attendance_correction_2026-01-20.txt` · lines 7–11
- BH-D105 · `BH-D105_individual_2026-01-19.txt` · lines 3–6
- BH-D106 · `BH-D106_telehealth_2026-01-21.txt` · lines 3–7
- BH-D107 · `BH-D107_group_activity_records_2026-01-22_and_29.txt` · lines 7–17
- BH-D108 · `BH-D108_final_attendance_and_cancellation_register.txt` · lines 8–20
- BH-D110 · `BH-D110_individual_primary_record_2026-01-26.txt` · lines 3–7
- BH-D111 · `BH-D111_individual_second_record_2026-01-26.txt` · lines 4–10
- BH-D113 · `BH-D113_family_therapy_2026-01-30.txt` · lines 3–7
- BH-D003 · `signed_treatment_plan_jan05.txt` · lines 6–12

## DEV-04 · encounter reconstruction

Reconstruct the care on January 19 and January 21. How many therapy contacts and patient therapy minutes occurred on each date, and how do the attendance records, clinical notes, later documents, and telehealth records affect your answer?

**Difficulty:** hard · **Answerability:** determinate

**Ground truth**

January 19: group HG-E110 from 10:00–11:15, minus the 10:45–11:00 nontherapeutic break, gives 60 minutes. Separate individual HG-E111 from 11:15–11:45 gives 30 minutes. Thus 2 psychotherapy encounters, 90 treatment minutes and 1 therapy day. BH-D103 explicitly corrects the original 11:30 departure; BH-D104, received January 26, merely retransmits the uncorrected original and does not supersede the correction. There is no actual overlap after correction. January 21: HG-E112/HG-A112 comprises 13:00–13:20 and 13:30–13:55, 20+25=45 minutes, with no treatment in the 10-minute outage. The two platform call IDs are reconnections within one encounter: 1 psychotherapy encounter and 1 therapy day.

**Required facts for grading**

- January 19 group 60 + individual 30 = 90 minutes across 2 encounters on 1 day.
- Correction controls departure; later receipt is not a new correction or service.
- January 21 is 1 encounter, 45 minutes; exclude outage and deduplicate call IDs.

**Failure modes:** latest receipt wins, correction ignored, apparent overlap double count, reconnection double count, outage as therapy.

**Evidence**

- BH-D101 · `BH-D101_group_content_2026-01-19.txt` · lines 6–10
- BH-D102 · `BH-D102_original_attendance_2026-01-19.txt` · lines 8–18
- BH-D103 · `BH-D103_attendance_correction_2026-01-20.txt` · lines 7–13
- BH-D104 · `BH-D104_resent_roster_received_2026-01-26.txt` · lines 8–20
- BH-D105 · `BH-D105_individual_2026-01-19.txt` · lines 3–13
- BH-D106 · `BH-D106_telehealth_2026-01-21.txt` · lines 3–20

## DEV-05 · longitudinal synthesis

Summarize the documented symptom course during the episode and the reason for the additional individual contact on January 19. Which symptom assessments are distinct, and what conclusions about progress can and cannot be supported?

**Difficulty:** hard · **Answerability:** partially_determinate

**Ground truth**

There are three distinct PHQ-9 administrations: January 5 score 18, January 16 score 14 (HG-Q116), and January 30 score 10 with item 9=0. The January 26 import is a copy of the January 16 form, not a fourth assessment. The scores decline by 4 points in each interval and 8 overall. Narratives describe some improvement in activity, mood and initial work communication, but persistent sleep variability, anxiety, avoidance and work-related functional difficulty. January 19 individual therapy was added after Rowan became overwhelmed by workplace discussion in group; grounding, paced breathing and a smaller drafting task eased immediate anxiety. This supports partial improvement, not remission, established work readiness, sustained normal sleep, or proof that a specific treatment caused the improvement. Later records document sending a message but continued delay arranging follow-up.

**Required facts for grading**

- Three distinct scores/dates: 18 on January 5, 14 on January 16, 10 on January 30; January 26 import is duplicate.
- Additional January 19 individual contact responded to anxiety/overwhelm during group.
- Improvement coexists with persistent functional and sleep problems.
- Do not infer remission, actual return to work or causal efficacy.

**Failure modes:** import date as assessment date, score only recovery, functional recovery invented, crisis reason invented.

**Evidence**

- BH-D002 · `intake_and_individual_jan05.txt` · lines 11–17
- BH-D013 · `symptom_measure_review_jan16.txt` · lines 6–15
- BH-D014 · `imported_measure_summary_received_jan26.txt` · lines 12–19
- BH-D101 · `BH-D101_group_content_2026-01-19.txt` · lines 10
- BH-D105 · `BH-D105_individual_2026-01-19.txt` · lines 9–13
- BH-D110 · `BH-D110_individual_primary_record_2026-01-26.txt` · lines 9–13
- BH-D115 · `BH-D115_symptom_measure_review_2026-01-30.txt` · lines 5–14

## DEV-06 · interval arithmetic

How many psychotherapy minutes did Rowan receive in the January 6 group, and how do the attendance roster and facilitator note jointly support the calculation?

**Difficulty:** medium · **Answerability:** determinate

**Ground truth**

HG-E102 counts as one attended group encounter with 45 patient therapy minutes. Actual presence was 10:15–11:15 (60 minutes); the 10:45–11:00 nontherapeutic break removes 15 minutes. Equivalently, 10:15–10:45 gives 30 minutes and 11:00–11:15 gives 15. The 90-minute booking is not delivered time.

**Required facts for grading**

- Actual presence 60 minutes; subtract 15-minute break for 45.
- Count 1 attended encounter despite partial attendance.

**Failure modes:** scheduled duration as treatment, breaks included, partial visit excluded.

**Evidence**

- BH-D004 · `group_facilitator_jan06.txt` · lines 5–12
- BH-D005 · `early_group_attendance_roster.txt` · lines 9–13

## DEV-07 · interval arithmetic

The January 12 roster says Rowan attended the full group. How much patient therapy time should be credited, and why?

**Difficulty:** medium · **Answerability:** determinate

**Ground truth**

Credit 75 minutes for one group encounter: Rowan was present 10:00–11:30 (90 minutes), but the facilitator records no therapeutic activity during 10:40–10:55 (15 minutes). Full attendance includes the break; it does not turn the break into therapy.

**Required facts for grading**

- 90 minutes present minus 15 nontherapeutic minutes equals 75.
- The actual break is 10:40–10:55, not the 10:45–11:00 used on other dates.

**Failure modes:** full attendance as full treatment, break time copied between dates.

**Evidence**

- BH-D005 · `early_group_attendance_roster.txt` · lines 9–15
- BH-D009 · `group_facilitator_jan12.txt` · lines 6–12

## DEV-08 · source reconciliation

Which January 19 group departure time should be used after considering all versions of the attendance record, and what makes that version authoritative for this field?

**Difficulty:** hard · **Answerability:** determinate

**Ground truth**

Use 11:15. The original final roster BH-D102 lists 11:30, but final correction BH-D103 explicitly replaces that departure based on the room-transfer record reviewed with the receiving clinician. It preserves the 10:00 arrival and group break. BH-D104 was received January 26 but retransmits the January 19 original, has no new clinician signature and omits the correction; its later receipt does not reverse the explicit amendment.

**Required facts for grading**

- 11:15 explicitly replaces 11:30 for HG-E110.
- The later received original copy contains no new correction.
- Arrival, service date and break remain unchanged.

**Failure modes:** latest receipt wins, all final records equal, scope of correction overextended.

**Evidence**

- BH-D102 · `BH-D102_original_attendance_2026-01-19.txt` · lines 8–18
- BH-D103 · `BH-D103_attendance_correction_2026-01-20.txt` · lines 7–16
- BH-D104 · `BH-D104_resent_roster_received_2026-01-26.txt` · lines 8–20

## DEV-09 · deduplication

The January 21 video export contains two call IDs. How many therapy sessions should an encounter-level abstraction contain, and how much contact time?

**Difficulty:** medium · **Answerability:** determinate

**Ground truth**

One individual psychotherapy session, HG-E112 under appointment HG-A112, with 45 minutes. VC-112A is 20 minutes and VC-112B is 25 minutes; the second call rejoins the original appointment after a network loss. Exclude 13:20–13:30.

**Required facts for grading**

- One encounter despite two call IDs.
- 20+25=45 minutes and 10-minute outage excluded.

**Failure modes:** call count as session count, outage as therapy.

**Evidence**

- BH-D106 · `BH-D106_telehealth_2026-01-21.txt` · lines 3–7
- BH-D106 · `BH-D106_telehealth_2026-01-21.txt` · lines 15–20

## DEV-10 · interval arithmetic

Calculate Rowan’s eligible group minutes on January 22. Does participation after the break establish attendance at the beginning of the group?

**Difficulty:** medium · **Answerability:** determinate

**Ground truth**

Actual arrival was 10:30 and departure 11:30. Remove the 10:45–11:00 nontherapeutic break: 15 minutes before plus 30 after = 45 minutes. The narrative of post-break participation does not establish presence at the 10:00 opening; the final register explicitly documents late arrival.

**Required facts for grading**

- Actual attendance 10:30–11:30; eligible therapy 45 minutes.
- Narrative participation cannot override patient-specific late arrival.

**Failure modes:** group schedule as patient attendance, narrative as full attendance.

**Evidence**

- BH-D107 · `BH-D107_group_activity_records_2026-01-22_and_29.txt` · lines 7–10
- BH-D107 · `BH-D107_group_activity_records_2026-01-22_and_29.txt` · lines 17
- BH-D108 · `BH-D108_final_attendance_and_cancellation_register.txt` · lines 6–14

## DEV-11 · interval arithmetic

How many therapy minutes should be assigned to the January 29 group, and which records are needed to establish them?

**Difficulty:** medium · **Answerability:** determinate

**Ground truth**

Assign 75 minutes: the final attendance register confirms Rowan present 10:00–11:30, and the activity record excludes a nontherapeutic break from 10:45–11:00. Attendance and content/break records together establish the patient-specific treatment time.

**Required facts for grading**

- 90 minutes present minus 15-minute break = 75.
- Use BH-D108 attendance with BH-D107 break.

**Failure modes:** breaks included, single source incomplete.

**Evidence**

- BH-D107 · `BH-D107_group_activity_records_2026-01-22_and_29.txt` · lines 12–17
- BH-D108 · `BH-D108_final_attendance_and_cancellation_register.txt` · lines 12
- BH-D108 · `BH-D108_final_attendance_and_cancellation_register.txt` · lines 20–22

## DEV-12 · patient presence

How much of the January 30 family appointment contributes to Rowan’s treatment-plan minute goal? Explain the difference from the therapist’s session duration.

**Difficulty:** medium · **Answerability:** determinate

**Ground truth**

One family therapy encounter contributes 30 minutes. The therapist’s session lasted 13:00–13:45 (45 minutes), but 13:00–13:15 was partner-only. Rowan participated 13:15–13:45. Exclude the initial 15 minutes under the patient-present therapy definition.

**Required facts for grading**

- 30 eligible minutes and 1 family encounter.
- Exclude 15 minutes of partner-only contact.

**Failure modes:** therapist minutes as patient minutes, partner only included.

**Evidence**

- BH-D003 · `signed_treatment_plan_jan05.txt` · lines 12
- BH-D113 · `BH-D113_family_therapy_2026-01-30.txt` · lines 3–11

## DEV-13 · deduplication

Do the two family notes signed on January 9 and January 10 represent separate visits? State the service date, encounter count, and patient therapy minutes.

**Difficulty:** medium · **Answerability:** determinate

**Ground truth**

Both document HG-E104 on January 9, 14:00–14:45 with Rowan and Casey present throughout. Count one family session and 45 patient minutes on January 9. Leena Park’s accompanying note was signed January 10; its signature date is not a second service date. Two clinicians do not double patient time.

**Required facts for grading**

- Service date January 9; HG-E104 is one encounter.
- 45 patient minutes, not 90; no January 10 therapy day created.

**Failure modes:** signature date as service date, cofacilitator double count.

**Evidence**

- BH-D007 · `family_primary_jan09.txt` · lines 6–10
- BH-D007 · `family_primary_jan09.txt` · lines 18
- BH-D008 · `family_cofacilitator_jan09.txt` · lines 6–11

## DEV-14 · unresolved conflict

Reconcile the January 26 individual psychotherapy records. What can be concluded with certainty, and what remains unresolved about duration?

**Difficulty:** hard · **Answerability:** partially_determinate

**Ground truth**

Both final signed notes identify the same individual encounter HG-E115 and appointment HG-A115, so one session and one therapy day are certain. BH-D110 states full patient contact 09:00–09:50, 50 minutes. BH-D111 explicitly states the full encounter began with Rowan entering at 09:10 and lasted to 09:50, 40 minutes. It is not merely a clinician joining ten minutes late. No supplied correction adjudicates the start time. Preserve 40- and 50-minute alternatives; do not sum to 90, average to 45, infer a 10-minute solo segment, or choose by signature recency or primary-note label alone.

**Required facts for grading**

- One encounter HG-E115/HG-A115.
- Final notes conflict on full encounter duration: 40 versus 50 minutes.
- Exact time remains unresolved; no record establishes a separate initial 10-minute segment.

**Failure modes:** primary note automatically wins, later signature automatically wins, concurrent clinician time summed, conflict averaged, solo segment invented.

**Evidence**

- BH-D110 · `BH-D110_individual_primary_record_2026-01-26.txt` · lines 3–16
- BH-D111 · `BH-D111_individual_second_record_2026-01-26.txt` · lines 4–17

## DEV-15 · source reconciliation

A January 27 draft says Rowan attended group and a group charge is posted. Did Rowan receive group psychotherapy that day? Explain the evidence conflict.

**Difficulty:** hard · **Answerability:** determinate

**Ground truth**

No. HG-E116 is a no-show with zero patient treatment minutes and no therapy day. The final signed attendance attestation says Rowan was absent for the entire group and no treatment contact occurred. The progress note was generated before the group, remains unsigned, has no manual clinical entry, and repeats a scheduling template. CH-116 shows a posted charge, which does not establish service delivery. Outreach left afterward contained no clinical discussion.

**Required facts for grading**

- 0 delivered encounters, 0 minutes, 0 therapy days for January 27.
- Signed patient-specific no-show attestation controls over unsigned autogenerated attendance text and posted charge.
- Outreach does not create treatment.

**Failure modes:** billing as attendance, template hallucination, outreach as therapy.

**Evidence**

- BH-D108 · `BH-D108_final_attendance_and_cancellation_register.txt` · lines 10
- BH-D108 · `BH-D108_final_attendance_and_cancellation_register.txt` · lines 16
- BH-D112 · `BH-D112_draft_note_and_charge_extract_2026-01-27.txt` · lines 5–25

## DEV-16 · service eligibility

What happened to the January 8 individual appointment and follow-up call, and how should each affect therapy counts and minutes?

**Difficulty:** medium · **Answerability:** determinate

**Ground truth**

HG-E103, scheduled 11:00–11:45, was a no-show; Rowan was not seen. A 13:20 outbound call went unanswered, and the 15:36 callback discussed the next appointment and resending the schedule. The log explicitly says no therapy intervention occurred. Neither the reserved 45-minute slot nor the callback contributes a session, therapy day, or treatment minutes. Rowan attributed the missed morning to a poor night of sleep.

**Required facts for grading**

- January 8 no-show contributes zero therapy.
- Callback was scheduling only, not a replacement therapy session.
- Documented explanation was a difficult morning after poor sleep.

**Failure modes:** scheduled slot counted, callback as therapy, no show reason invented.

**Evidence**

- BH-D006 · `early_appointment_status_export.txt` · lines 12
- BH-D015 · `missed_visit_outreach_jan08.txt` · lines 6–17

## DEV-17 · event classification

Why was the January 15 group not delivered, and is it accurate to describe this as a patient no-show or a refusal of therapy?

**Difficulty:** easy · **Answerability:** determinate

**Ground truth**

The clinic cancelled HG-E108 due to staff illness and lack of a covering facilitator. Rowan acknowledged the notice. No group was held, no participants were seen and no replacement group occurred in that slot. Classify clinic cancellation, not a patient no-show or refusal; credit zero therapy.

**Required facts for grading**

- Clinic cancellation caused by staff illness.
- Not a patient no-show or refusal; no delivered group.

**Failure modes:** clinic cancellation as nonadherence, notification call as therapy.

**Evidence**

- BH-D006 · `early_appointment_status_export.txt` · lines 17–20
- BH-D016 · `group_cancellation_notice_jan15.txt` · lines 9–15

## DEV-18 · event classification

What is the final disposition of the January 28 individual appointment, including the stated reason and any replacement within January?

**Difficulty:** easy · **Answerability:** determinate

**Ground truth**

HG-E117, scheduled 14:00–14:45, was cancelled by Rowan before the appointment. Cancellation was received at 08:12 because of a personal scheduling conflict. The register says no replacement appointment was booked within January 2026. Credit zero therapy for that appointment; this does not mean all later January care was cancelled.

**Required facts for grading**

- Patient cancellation before start, for personal scheduling conflict.
- No replacement booked within January; zero therapy for HG-E117.

**Failure modes:** cancellation as no show, replacement invented, all later care cancelled.

**Evidence**

- BH-D108 · `BH-D108_final_attendance_and_cancellation_register.txt` · lines 11
- BH-D108 · `BH-D108_final_attendance_and_cancellation_register.txt` · lines 18

## DEV-19 · patient presence

Does the completed January 16 family collateral contact count toward Rowan’s patient-present therapy goal? Describe who participated and the treatment-time implication.

**Difficulty:** easy · **Answerability:** determinate

**Ground truth**

No. Casey alone attended HG-E109, 14:00–14:40. Rowan was absent throughout and did not join by phone or video. Although a 40-minute collateral contact was completed, it yields zero patient-present psychotherapy encounters, minutes and therapy days for Rowan under the local plan.

**Required facts for grading**

- Casey only; Rowan absent entire contact.
- 40 collateral minutes but zero eligible patient therapy minutes.

**Failure modes:** completed status as patient attendance, collateral as family therapy.

**Evidence**

- BH-D003 · `signed_treatment_plan_jan05.txt` · lines 12
- BH-D006 · `early_appointment_status_export.txt` · lines 18–20
- BH-D012 · `partner_collateral_jan16.txt` · lines 6–17

## DEV-20 · service eligibility

How should the January 23 care-coordination call be represented when counting Rowan’s therapy, and did it change treatment frequency or medication?

**Difficulty:** easy · **Answerability:** determinate

**Ground truth**

HG-E114 was a 20-minute professional-only call between Mira Patel and outside social worker Daniel Shaw, 09:00–09:20. Rowan did not participate and no patient psychotherapy occurred, so it contributes zero patient therapy encounters, minutes or days. No medication or psychotherapy-frequency change was made. They discussed practical work-return supports but made no employment determination.

**Required facts for grading**

- 20 minutes between professionals; zero patient therapy.
- No frequency or medication change and no employment determination.

**Failure modes:** coordination as therapy, treatment change invented, work clearance invented.

**Evidence**

- BH-D003 · `signed_treatment_plan_jan05.txt` · lines 12
- BH-D109 · `BH-D109_care_coordination_2026-01-23.txt` · lines 3–13

## DEV-21 · service eligibility

Which medication visits occurred during the episode, how much time did they take, and how much of that time is eligible for the psychotherapy goal?

**Difficulty:** medium · **Answerability:** determinate

**Ground truth**

January 13 HG-E106: Elias Brenner, NP, 09:00–09:25, 25 minutes. January 30 HG-E120: Elena Ortiz, PMHNP, 15:00–15:20, 20 minutes. There were two medication visits totaling 45 minutes, with zero minutes eligible for the psychotherapy goal. Both records specify medication management without a separately documented psychotherapy component.

**Required facts for grading**

- Two medication visits totaling 45 minutes.
- None of those minutes contribute to the patient-present psychotherapy goal.

**Failure modes:** all clinical contact as psychotherapy, medication counseling as psychotherapy.

**Evidence**

- BH-D003 · `signed_treatment_plan_jan05.txt` · lines 12
- BH-D010 · `medication_review_jan13.txt` · lines 6–8
- BH-D010 · `medication_review_jan13.txt` · lines 17
- BH-D114 · `BH-D114_medication_management_2026-01-30.txt` · lines 3–12

## DEV-22 · service eligibility

Do the January 16 and January 30 questionnaire-review entries establish additional therapy sessions or durations?

**Difficulty:** easy · **Answerability:** determinate

**Ground truth**

No. BH-D013 records review of a portal submission and explicitly states no clinical appointment occurred at review. BH-D115 is questionnaire review within ongoing care, not a separate treatment appointment, and claims no additional patient-contact interval. They support symptom assessment, not extra psychotherapy sessions, days or minutes.

**Required facts for grading**

- Both review entries add zero separate therapy sessions and minutes.
- Questionnaire completion and review timestamps are not therapy start/end times.

**Failure modes:** questionnaire as visit, review duration invented.

**Evidence**

- BH-D013 · `symptom_measure_review_jan16.txt` · lines 6–15
- BH-D115 · `BH-D115_symptom_measure_review_2026-01-30.txt` · lines 5–14

## DEV-23 · authorization interpretation

What does the group authorization establish about service type, dates, and quantity, and what does it not establish about delivered treatment?

**Difficulty:** medium · **Answerability:** determinate

**Ground truth**

HG-A260104-88 authorizes 8 group sessions during January 5–30, 2026; one unit represents one scheduled group session. It does not authorize individual, family or medication visits under that quantity. It permits scheduling but is not an attendance record and supplies no delivered minutes. It cannot by itself establish that eight groups occurred or were attended.

**Required facts for grading**

- 8 group units, January 5–30; one unit is one scheduled group session.
- Other service types excluded from this group quantity.
- Authorization does not prove attendance or treatment duration.

**Failure modes:** authorization as attendance, unit as hour, authorization scope expanded.

**Evidence**

- BH-D001 · `group_authorization_letter.txt` · lines 5–15

## DEV-24 · mixed service aggregation

For January 30, report the number of patient-attended clinical visits, the total documented patient-contact minutes across those visits, and the psychotherapy minutes and therapy-day count.

**Difficulty:** hard · **Answerability:** determinate

**Ground truth**

There were two patient-attended clinical visits: family psychotherapy HG-E119 with 30 minutes of Rowan’s participation, and medication management HG-E120 with 20 minutes. Total patient contact across those visits is 50 minutes; only 30 minutes qualify as psychotherapy, across 1 psychotherapy encounter and 1 therapy day. The family therapist’s initial 15 partner-only minutes and the separate questionnaire-review entry add no Rowan contact time.

**Required facts for grading**

- 2 patient-attended visits and 50 documented patient-contact minutes.
- Only 1 psychotherapy encounter, 30 psychotherapy minutes, and 1 therapy day.
- Exclude partner-only interval and do not add questionnaire review.

**Failure modes:** all contact as therapy, therapist minutes as patient minutes, review double count.

**Evidence**

- BH-D003 · `signed_treatment_plan_jan05.txt` · lines 12
- BH-D113 · `BH-D113_family_therapy_2026-01-30.txt` · lines 3–11
- BH-D114 · `BH-D114_medication_management_2026-01-30.txt` · lines 3–12
- BH-D115 · `BH-D115_symptom_measure_review_2026-01-30.txt` · lines 14

## DEV-25 · temporal provenance

Several documents were received or signed around January 26. Which establish a new January 26 therapy encounter, and which describe earlier services or assessments?

**Difficulty:** hard · **Answerability:** determinate

**Ground truth**

BH-D110 and BH-D111 establish one January 26 individual encounter, HG-E115/HG-A115, with unresolved 40-versus-50-minute duration. BH-D104, received January 26, is a retransmission of the January 19 HG-E110 roster, not a new group or a new correction. BH-D014, received January 26, copies the PHQ-9 completed January 16 on HG-Q116, not a new questionnaire or visit. Thus these records support one new therapy encounter and one therapy day on January 26.

**Required facts for grading**

- BH-D110/BH-D111 represent one January 26 encounter.
- BH-D104 refers to January 19 service; BH-D014 refers to January 16 assessment.
- Receipt date does not establish a new service or assessment.

**Failure modes:** import date as service date, latest receipt wins, duplicate note counted.

**Evidence**

- BH-D110 · `BH-D110_individual_primary_record_2026-01-26.txt` · lines 3–7
- BH-D111 · `BH-D111_individual_second_record_2026-01-26.txt` · lines 4–10
- BH-D104 · `BH-D104_resent_roster_received_2026-01-26.txt` · lines 4–20
- BH-D014 · `imported_measure_summary_received_jan26.txt` · lines 6–19

## DEV-26 · time aggregation

Across January 5–30, how many patient-present therapy minutes belong to individual, group, and family therapy? Include uncertainty only where the records require it.

**Difficulty:** hard · **Answerability:** partially_determinate

**Ground truth**

Individual: 50+45+30+45+(40 or 50)=210 or 220 minutes. Group: 45+75+60+45+75=300 minutes. Family: 45+30=75 minutes. The combined total is 585 or 595 minutes. Only the January 26 individual encounter causes duration uncertainty; group and family totals are determinate.

**Required facts for grading**

- Individual 210 or 220; group 300; family 75 minutes.
- Overall 585 or 595; ambiguity confined to January 26 individual therapy.

**Failure modes:** uncertainty spread to all services, incorrect aggregation, conflict silently resolved.

**Evidence**

- BH-D002 · `intake_and_individual_jan05.txt` · lines 6–8
- BH-D004 · `group_facilitator_jan06.txt` · lines 12
- BH-D005 · `early_group_attendance_roster.txt` · lines 9–11
- BH-D007 · `family_primary_jan09.txt` · lines 6–9
- BH-D008 · `family_cofacilitator_jan09.txt` · lines 6–9
- BH-D009 · `group_facilitator_jan12.txt` · lines 12
- BH-D011 · `individual_therapy_jan14.txt` · lines 6–8
- BH-D101 · `BH-D101_group_content_2026-01-19.txt` · lines 6–8
- BH-D103 · `BH-D103_attendance_correction_2026-01-20.txt` · lines 7–11
- BH-D105 · `BH-D105_individual_2026-01-19.txt` · lines 3–6
- BH-D106 · `BH-D106_telehealth_2026-01-21.txt` · lines 3–7
- BH-D107 · `BH-D107_group_activity_records_2026-01-22_and_29.txt` · lines 7–17
- BH-D108 · `BH-D108_final_attendance_and_cancellation_register.txt` · lines 8–20
- BH-D110 · `BH-D110_individual_primary_record_2026-01-26.txt` · lines 3–7
- BH-D111 · `BH-D111_individual_second_record_2026-01-26.txt` · lines 4–10
- BH-D113 · `BH-D113_family_therapy_2026-01-30.txt` · lines 3–7

## DEV-27 · comparative aggregation

Compare therapy participation in January 5–18 with January 19–30 by sessions, distinct days, and minutes. What changed numerically, without attributing a cause?

**Difficulty:** hard · **Answerability:** partially_determinate

**Ground truth**

January 5–18: 5 sessions on 5 days, 260 minutes. January 19–30: 7 sessions on 6 days, 325 or 335 minutes. The later period therefore has 2 more sessions, 1 more therapy day, and 65 or 75 more patient therapy minutes. It includes two sessions on January 19. The records do not establish that the difference caused symptom change or reflects a formally changed treatment frequency.

**Required facts for grading**

- Early period: 5 sessions/5 days/260 minutes.
- Later: 7 sessions/6 days/325 or 335 minutes.
- Difference: +2 sessions, +1 day, +65 or 75 minutes; no causal claim.

**Failure modes:** same day count error, comparison without uncertainty, causal overclaim.

**Evidence**

- BH-D002 · `intake_and_individual_jan05.txt` · lines 6–8
- BH-D004 · `group_facilitator_jan06.txt` · lines 12
- BH-D005 · `early_group_attendance_roster.txt` · lines 9–11
- BH-D007 · `family_primary_jan09.txt` · lines 6–9
- BH-D008 · `family_cofacilitator_jan09.txt` · lines 6–9
- BH-D009 · `group_facilitator_jan12.txt` · lines 12
- BH-D011 · `individual_therapy_jan14.txt` · lines 6–8
- BH-D101 · `BH-D101_group_content_2026-01-19.txt` · lines 6–8
- BH-D103 · `BH-D103_attendance_correction_2026-01-20.txt` · lines 7–11
- BH-D105 · `BH-D105_individual_2026-01-19.txt` · lines 3–6
- BH-D106 · `BH-D106_telehealth_2026-01-21.txt` · lines 3–7
- BH-D107 · `BH-D107_group_activity_records_2026-01-22_and_29.txt` · lines 7–17
- BH-D108 · `BH-D108_final_attendance_and_cancellation_register.txt` · lines 8–20
- BH-D110 · `BH-D110_individual_primary_record_2026-01-26.txt` · lines 3–7
- BH-D111 · `BH-D111_individual_second_record_2026-01-26.txt` · lines 4–10
- BH-D113 · `BH-D113_family_therapy_2026-01-30.txt` · lines 3–7
- BH-D109 · `BH-D109_care_coordination_2026-01-23.txt` · lines 11

## DEV-28 · counting units

Why are the total number of attended therapy encounters and the number of therapy days different in this episode? Identify the date responsible.

**Difficulty:** easy · **Answerability:** determinate

**Ground truth**

There are 12 therapy encounters but 11 distinct therapy days because January 19 includes both group HG-E110 and individual HG-E111. They are separate services, but both occur on one calendar day. Concurrent clinicians and video reconnections do not account for extra encounters.

**Required facts for grading**

- 12 encounters versus 11 days.
- January 19 has two distinct encounters on one day.

**Failure modes:** encounters as days, same day encounters merged.

**Evidence**

- BH-D002 · `intake_and_individual_jan05.txt` · lines 6–8
- BH-D004 · `group_facilitator_jan06.txt` · lines 12
- BH-D005 · `early_group_attendance_roster.txt` · lines 9–11
- BH-D007 · `family_primary_jan09.txt` · lines 6–9
- BH-D008 · `family_cofacilitator_jan09.txt` · lines 6–9
- BH-D009 · `group_facilitator_jan12.txt` · lines 12
- BH-D011 · `individual_therapy_jan14.txt` · lines 6–8
- BH-D101 · `BH-D101_group_content_2026-01-19.txt` · lines 6–8
- BH-D103 · `BH-D103_attendance_correction_2026-01-20.txt` · lines 7–11
- BH-D105 · `BH-D105_individual_2026-01-19.txt` · lines 3–6
- BH-D106 · `BH-D106_telehealth_2026-01-21.txt` · lines 3–7
- BH-D107 · `BH-D107_group_activity_records_2026-01-22_and_29.txt` · lines 7–17
- BH-D108 · `BH-D108_final_attendance_and_cancellation_register.txt` · lines 8–20
- BH-D110 · `BH-D110_individual_primary_record_2026-01-26.txt` · lines 3–7
- BH-D111 · `BH-D111_individual_second_record_2026-01-26.txt` · lines 4–10
- BH-D113 · `BH-D113_family_therapy_2026-01-30.txt` · lines 3–7
- BH-D003 · `signed_treatment_plan_jan05.txt` · lines 12

## DEV-29 · exception abstraction

List the scheduled therapy appointments that were not delivered during January 5–30, distinguishing no-shows, clinic cancellation, and patient cancellation.

**Difficulty:** medium · **Answerability:** determinate

**Ground truth**

Four scheduled therapy appointments were not delivered: January 8 individual HG-E103, no-show; January 15 group HG-E108, clinic cancellation due to staff illness; January 27 group HG-E116, no-show; January 28 individual HG-E117, patient cancellation before the visit for a personal scheduling conflict. Each contributes zero therapy minutes/days. January 16 partner collateral was completed as collateral and is excluded for patient absence, not as one of these four no-show/cancelled appointments.

**Required facts for grading**

- No-shows January 8 and 27; clinic cancellation January 15; patient cancellation January 28.
- Each contributes zero therapy; distinguish completed collateral January 16.

**Failure modes:** cancellation types conflated, collateral misclassified, billed no show counted.

**Evidence**

- BH-D006 · `early_appointment_status_export.txt` · lines 9–20
- BH-D015 · `missed_visit_outreach_jan08.txt` · lines 9–17
- BH-D016 · `group_cancellation_notice_jan15.txt` · lines 9–15
- BH-D108 · `BH-D108_final_attendance_and_cancellation_register.txt` · lines 8–18
- BH-D012 · `partner_collateral_jan16.txt` · lines 6–11

## DEV-30 · authorization interpretation

How does the number of attended groups compare with the authorized quantity, and can the remaining billable authorization balance be determined from these documents?

**Difficulty:** hard · **Answerability:** partially_determinate

**Ground truth**

Five groups are documented as attended, compared with eight authorized group sessions: the numerical difference is three, and attended sessions are 62.5% of the authorized quantity. That comparison is not a verified remaining billable balance. The documents do not supply payer unit-consumption/reversal rules or a reconciled authorization ledger, and a charge was posted for the January 27 no-show. Do not infer three billable sessions remain, three patient no-shows, or eight delivered groups.

**Required facts for grading**

- 5 attended versus 8 authorized; arithmetic difference 3 (62.5% attended/authorized).
- Remaining billable authorization balance cannot be established.

**Failure modes:** authorization balance inferred, missing units as no shows, billing as attendance.

**Evidence**

- BH-D002 · `intake_and_individual_jan05.txt` · lines 6–8
- BH-D004 · `group_facilitator_jan06.txt` · lines 12
- BH-D005 · `early_group_attendance_roster.txt` · lines 9–11
- BH-D007 · `family_primary_jan09.txt` · lines 6–9
- BH-D008 · `family_cofacilitator_jan09.txt` · lines 6–9
- BH-D009 · `group_facilitator_jan12.txt` · lines 12
- BH-D011 · `individual_therapy_jan14.txt` · lines 6–8
- BH-D101 · `BH-D101_group_content_2026-01-19.txt` · lines 6–8
- BH-D103 · `BH-D103_attendance_correction_2026-01-20.txt` · lines 7–11
- BH-D105 · `BH-D105_individual_2026-01-19.txt` · lines 3–6
- BH-D106 · `BH-D106_telehealth_2026-01-21.txt` · lines 3–7
- BH-D107 · `BH-D107_group_activity_records_2026-01-22_and_29.txt` · lines 7–17
- BH-D108 · `BH-D108_final_attendance_and_cancellation_register.txt` · lines 8–20
- BH-D110 · `BH-D110_individual_primary_record_2026-01-26.txt` · lines 3–7
- BH-D111 · `BH-D111_individual_second_record_2026-01-26.txt` · lines 4–10
- BH-D113 · `BH-D113_family_therapy_2026-01-30.txt` · lines 3–7
- BH-D001 · `group_authorization_letter.txt` · lines 10–15
- BH-D108 · `BH-D108_final_attendance_and_cancellation_register.txt` · lines 10–16
- BH-D112 · `BH-D112_draft_note_and_charge_extract_2026-01-27.txt` · lines 18–25

## DEV-31 · interval arithmetic

For the five attended groups, reconcile booked time, actual time present, nontherapeutic breaks, and delivered patient therapy minutes.

**Difficulty:** hard · **Answerability:** determinate

**Ground truth**

The five attended groups each had 90-minute scheduled slots, totaling 450 booked minutes. Actual presence was 60, 90, 75, 60 and 90 minutes on January 6, 12, 19, 22 and 29, totaling 375. Each actual attendance interval includes a 15-minute nontherapeutic break, totaling 75 break minutes. Thus 375−75=300 therapy minutes. The 150-minute gap from booking to treatment consists of 75 minutes outside Rowan’s presence (30+0+15+30+0) and 75 minutes of breaks. This calculation covers the five attended groups, not cancelled or no-show slots.

**Required facts for grading**

- 450 booked, 375 present, 75 break, 300 therapy minutes across attended groups.
- 75 booked minutes outside presence plus 75 break minutes explain the 150-minute gap.

**Failure modes:** scheduled duration as treatment, double subtracted break, wrong partial attendance.

**Evidence**

- BH-D004 · `group_facilitator_jan06.txt` · lines 5–12
- BH-D005 · `early_group_attendance_roster.txt` · lines 9–11
- BH-D009 · `group_facilitator_jan12.txt` · lines 6–12
- BH-D101 · `BH-D101_group_content_2026-01-19.txt` · lines 6–8
- BH-D103 · `BH-D103_attendance_correction_2026-01-20.txt` · lines 7–11
- BH-D107 · `BH-D107_group_activity_records_2026-01-22_and_29.txt` · lines 7–17
- BH-D108 · `BH-D108_final_attendance_and_cancellation_register.txt` · lines 9–14
- BH-D108 · `BH-D108_final_attendance_and_cancellation_register.txt` · lines 20

## DEV-32 · error detection

A summary assigns 55 minutes to the January 21 video visit because it spans 13:00–13:55. Is that abstraction supported? Provide the corrected calculation.

**Difficulty:** medium · **Answerability:** determinate

**Ground truth**

No. The elapsed span is 55 minutes, but 13:20–13:30 was a connection loss without therapeutic contact. Correct patient psychotherapy time is 20+25=45 minutes, or 55−10=45. It remains one encounter under HG-A112.

**Required facts for grading**

- 55 elapsed minutes minus 10 noncontact minutes =45 treatment minutes.
- One encounter.

**Failure modes:** elapsed time as contact, outage as therapy.

**Evidence**

- BH-D106 · `BH-D106_telehealth_2026-01-21.txt` · lines 7
- BH-D106 · `BH-D106_telehealth_2026-01-21.txt` · lines 15–20

## DEV-33 · patient presence

Across the January 9 family visit, January 16 collateral contact, and January 30 family visit, how much documented clinician session time involved family or partner work, and how much qualifies as Rowan’s patient-present family therapy?

**Difficulty:** hard · **Answerability:** determinate

**Ground truth**

The three session intervals total 45+40+45=130 minutes of family/partner-related session time, counting concurrent cofacilitators once. Rowan’s eligible family therapy is 45+0+30=75 minutes across two patient-present family encounters. The difference is 55 minutes: all 40 minutes on January 16 and the first 15 minutes on January 30. This is session elapsed time, not a sum of individual clinicians’ labor minutes.

**Required facts for grading**

- 130 session minutes versus 75 eligible patient family therapy minutes.
- 55 minutes excluded for patient absence; only 2 eligible family encounters.
- Do not double January 9 for two clinicians.

**Failure modes:** clinician labor as session time, collateral as patient therapy, partial presence ignored.

**Evidence**

- BH-D003 · `signed_treatment_plan_jan05.txt` · lines 12
- BH-D007 · `family_primary_jan09.txt` · lines 6–9
- BH-D008 · `family_cofacilitator_jan09.txt` · lines 6–8
- BH-D012 · `partner_collateral_jan16.txt` · lines 6–17
- BH-D113 · `BH-D113_family_therapy_2026-01-30.txt` · lines 6–11

## DEV-34 · date abstraction

Provide the distinct dates on which Rowan actually received eligible psychotherapy, grouped into Monday–Sunday weeks.

**Difficulty:** medium · **Answerability:** determinate

**Ground truth**

January 5–11: January 5, 6, 9 (3 days). January 12–18: January 12, 14 (2 days). January 19–25: January 19, 21, 22 (3 days). January 26–February 1, within the review period through January 30: January 26, 29, 30 (3 days). Total 11 days. January 19 is listed once despite two sessions; medication-only, collateral-only, coordination and administrative dates are not additional therapy days.

**Required facts for grading**

- Dates exactly January 5,6,9,12,14,19,21,22,26,29,30.
- Weekly day counts 3,2,3,3; 11 overall.

**Failure modes:** signature date as service date, nontherapy date included, duplicate day.

**Evidence**

- BH-D002 · `intake_and_individual_jan05.txt` · lines 6–8
- BH-D004 · `group_facilitator_jan06.txt` · lines 12
- BH-D005 · `early_group_attendance_roster.txt` · lines 9–11
- BH-D007 · `family_primary_jan09.txt` · lines 6–9
- BH-D008 · `family_cofacilitator_jan09.txt` · lines 6–9
- BH-D009 · `group_facilitator_jan12.txt` · lines 12
- BH-D011 · `individual_therapy_jan14.txt` · lines 6–8
- BH-D101 · `BH-D101_group_content_2026-01-19.txt` · lines 6–8
- BH-D103 · `BH-D103_attendance_correction_2026-01-20.txt` · lines 7–11
- BH-D105 · `BH-D105_individual_2026-01-19.txt` · lines 3–6
- BH-D106 · `BH-D106_telehealth_2026-01-21.txt` · lines 3–7
- BH-D107 · `BH-D107_group_activity_records_2026-01-22_and_29.txt` · lines 7–17
- BH-D108 · `BH-D108_final_attendance_and_cancellation_register.txt` · lines 8–20
- BH-D110 · `BH-D110_individual_primary_record_2026-01-26.txt` · lines 3–7
- BH-D111 · `BH-D111_individual_second_record_2026-01-26.txt` · lines 4–10
- BH-D113 · `BH-D113_family_therapy_2026-01-30.txt` · lines 3–7
- BH-D003 · `signed_treatment_plan_jan05.txt` · lines 12

## DEV-35 · threshold arithmetic

For each week, quantify any shortfall against the treatment plan’s therapy-day and minute thresholds. Preserve unresolved alternatives.

**Difficulty:** hard · **Answerability:** partially_determinate

**Ground truth**

January 5–11: day threshold met, minute shortfall 10 (140 versus 150). January 12–18: short by 1 day and 30 minutes (2 days/120). January 19–25: no shortfall; 3 days/180 minutes, 30 minutes above threshold. Last week’s reviewed services: day threshold met; if January 26 was 40 minutes, 145 total is 5 short; if 50, 155 total is 5 above. These are numerical gaps, not proof that an additional contact actually occurred or a clinical recommendation about how to schedule it.

**Required facts for grading**

- Weekly minute gaps: 10 short, 30 short, 30 above, 5 short or 5 above.
- Only January 12–18 is short on days, by 1.
- Last-week conclusion remains conditional.

**Failure modes:** threshold rounding, uncertainty collapsed, hypothetical service counted.

**Evidence**

- BH-D002 · `intake_and_individual_jan05.txt` · lines 6–8
- BH-D004 · `group_facilitator_jan06.txt` · lines 12
- BH-D005 · `early_group_attendance_roster.txt` · lines 9–11
- BH-D007 · `family_primary_jan09.txt` · lines 6–9
- BH-D008 · `family_cofacilitator_jan09.txt` · lines 6–9
- BH-D009 · `group_facilitator_jan12.txt` · lines 12
- BH-D011 · `individual_therapy_jan14.txt` · lines 6–8
- BH-D101 · `BH-D101_group_content_2026-01-19.txt` · lines 6–8
- BH-D103 · `BH-D103_attendance_correction_2026-01-20.txt` · lines 7–11
- BH-D105 · `BH-D105_individual_2026-01-19.txt` · lines 3–6
- BH-D106 · `BH-D106_telehealth_2026-01-21.txt` · lines 3–7
- BH-D107 · `BH-D107_group_activity_records_2026-01-22_and_29.txt` · lines 7–17
- BH-D108 · `BH-D108_final_attendance_and_cancellation_register.txt` · lines 8–20
- BH-D110 · `BH-D110_individual_primary_record_2026-01-26.txt` · lines 3–7
- BH-D111 · `BH-D111_individual_second_record_2026-01-26.txt` · lines 4–10
- BH-D113 · `BH-D113_family_therapy_2026-01-30.txt` · lines 3–7
- BH-D003 · `signed_treatment_plan_jan05.txt` · lines 12

## DEV-36 · scope interpretation

Is the three-days/150-minutes weekly threshold a universal clinical or insurance standard in this record, and which services does it include?

**Difficulty:** medium · **Answerability:** determinate

**Ground truth**

The document explicitly identifies it as Rowan’s individualized local treatment-plan goal. It includes patient-present individual, group and family psychotherapy, with both at least 3 calendar therapy days and at least 150 minutes required per Monday–Sunday week. Medication management, collateral-only contacts and care coordination are excluded. The supplied record does not establish it as a universal standard or insurer requirement.

**Required facts for grading**

- Local individualized goal, not an established universal or payer rule.
- Patient-present individual/group/family included; medication, collateral-only and coordination excluded.
- Both thresholds apply per Monday–Sunday week.

**Failure modes:** external standard invented, and or error, service scope expanded.

**Evidence**

- BH-D003 · `signed_treatment_plan_jan05.txt` · lines 10–12

## DEV-37 · uncertainty propagation

Which episode-level conclusions change under the two January 26 duration scenarios, and which remain unchanged?

**Difficulty:** hard · **Answerability:** partially_determinate

**Ground truth**

Choosing the 40- versus 50-minute record changes individual totals (210 versus 220), final-week minutes (145 versus 155), episode minutes (585 versus 595), corresponding hour totals, and final-week goal status (not met versus met). It does not change 12 attended therapy encounters, service counts of 5 individual/5 group/2 family, 11 therapy days, final-week 3 days, group 300 minutes, family 75 minutes, or the first three weeks’ results. Neither alternative is adjudicated by the supplied evidence.

**Required facts for grading**

- Propagate 10-minute uncertainty to individual, final-week, episode totals and final-week threshold.
- Counts, therapy days and other service/week totals remain fixed.
- Do not assert a resolved scenario.

**Failure modes:** uncertainty not propagated, counts made uncertain, scenario selected without evidence.

**Evidence**

- BH-D002 · `intake_and_individual_jan05.txt` · lines 6–8
- BH-D004 · `group_facilitator_jan06.txt` · lines 12
- BH-D005 · `early_group_attendance_roster.txt` · lines 9–11
- BH-D007 · `family_primary_jan09.txt` · lines 6–9
- BH-D008 · `family_cofacilitator_jan09.txt` · lines 6–9
- BH-D009 · `group_facilitator_jan12.txt` · lines 12
- BH-D011 · `individual_therapy_jan14.txt` · lines 6–8
- BH-D101 · `BH-D101_group_content_2026-01-19.txt` · lines 6–8
- BH-D103 · `BH-D103_attendance_correction_2026-01-20.txt` · lines 7–11
- BH-D105 · `BH-D105_individual_2026-01-19.txt` · lines 3–6
- BH-D106 · `BH-D106_telehealth_2026-01-21.txt` · lines 3–7
- BH-D107 · `BH-D107_group_activity_records_2026-01-22_and_29.txt` · lines 7–17
- BH-D108 · `BH-D108_final_attendance_and_cancellation_register.txt` · lines 8–20
- BH-D110 · `BH-D110_individual_primary_record_2026-01-26.txt` · lines 3–7
- BH-D111 · `BH-D111_individual_second_record_2026-01-26.txt` · lines 4–10
- BH-D113 · `BH-D113_family_therapy_2026-01-30.txt` · lines 3–7
- BH-D003 · `signed_treatment_plan_jan05.txt` · lines 12

## DEV-38 · measurement deduplication

List the distinct PHQ-9 assessments by actual completion date and score, identifying any duplicated measurement documentation.

**Difficulty:** medium · **Answerability:** determinate

**Ground truth**

Three assessments: January 5, 2026 =18; January 16, 2026 at 08:17, portal form HG-Q116 =14; January 30, 2026 at 12:42 =10. BH-D014 received January 26 copies the January 16 result and form; it adds no assessment. January 16 clinician review at 09:10 is also not a separate administration.

**Required facts for grading**

- Three unique completion dates and scores: Jan5 18, Jan16 14, Jan30 10.
- Jan26 import and Jan16 review are not extra questionnaires.

**Failure modes:** import date as assessment date, review as new assessment.

**Evidence**

- BH-D002 · `intake_and_individual_jan05.txt` · lines 15
- BH-D013 · `symptom_measure_review_jan16.txt` · lines 6–15
- BH-D014 · `imported_measure_summary_received_jan26.txt` · lines 12–19
- BH-D115 · `BH-D115_symptom_measure_review_2026-01-30.txt` · lines 5–6

## DEV-39 · measurement arithmetic

What are the absolute and percentage changes in PHQ-9 from intake to the final assessment? Show the denominator and avoid inferring functional recovery from the calculation.

**Difficulty:** medium · **Answerability:** determinate

**Ground truth**

PHQ-9 fell from 18 on January 5 to 10 on January 30: final minus baseline is −8 points, an 8-point decrease. Relative to baseline, (18−10)/18×100=44.44% decrease, approximately 44.4%. The intermediate score was 14, so each interval fell 4 points. This numerical decline does not establish remission or recovery of work functioning; the final review documents persistent avoidance and functional impact.

**Required facts for grading**

- 8-point decrease; 44.4% relative to baseline 18.
- Do not divide by 10 or equate score change with full recovery.

**Failure modes:** wrong percentage denominator, score only recovery.

**Evidence**

- BH-D002 · `intake_and_individual_jan05.txt` · lines 15
- BH-D013 · `symptom_measure_review_jan16.txt` · lines 8–13
- BH-D115 · `BH-D115_symptom_measure_review_2026-01-30.txt` · lines 5–12

## DEV-40 · false premise

What was Rowan’s newly completed PHQ-9 score on January 26, and how did it compare with January 16?

**Difficulty:** medium · **Answerability:** not_established

**Ground truth**

No newly completed January 26 PHQ-9 is documented. The January 26 import contains the January 16 score of 14 from form HG-Q116 and explicitly says no new questionnaire was included. Therefore a January 16-to-January 26 score change cannot be calculated as a new measurement interval; calling it unchanged at 14 would falsely treat a duplicate as another assessment.

**Required facts for grading**

- Reject premise of a new January 26 administration.
- Imported 14 belongs to January 16; no new interval change established.

**Failure modes:** false premise accepted, duplicate score as stability.

**Evidence**

- BH-D013 · `symptom_measure_review_jan16.txt` · lines 6–9
- BH-D014 · `imported_measure_summary_received_jan26.txt` · lines 12–19

## DEV-41 · missing data

What item-level PHQ-9 information is available, and can item 9 be compared across all three assessments?

**Difficulty:** medium · **Answerability:** partially_determinate

**Ground truth**

The January 30 form explicitly reports item 9=0 and total=10. The supplied January 5 and January 16 entries provide total scores but no item 9 values or complete item-level responses. A longitudinal item 9 comparison is therefore not supported. Narrative safety statements are separate evidence and should not be converted into unstated questionnaire item scores.

**Required facts for grading**

- Item 9=0 documented only for January 30.
- Earlier item 9 values absent in supplied records; no three-date item comparison.
- Narrative denials do not supply missing item scores.

**Failure modes:** missing item imputed, narrative as questionnaire score.

**Evidence**

- BH-D002 · `intake_and_individual_jan05.txt` · lines 13–15
- BH-D013 · `symptom_measure_review_jan16.txt` · lines 6–13
- BH-D115 · `BH-D115_symptom_measure_review_2026-01-30.txt` · lines 5–10

## DEV-42 · clinical synthesis

By January 30, what evidence supports improvement and what evidence limits a conclusion of recovery? Integrate symptoms with functioning.

**Difficulty:** hard · **Answerability:** partially_determinate

**Ground truth**

Improvement is supported by PHQ-9 declining 18→14→10, more willingness to attempt small activities, opening and later sending a work message, and less persistently low mood. Limits include ongoing delay in follow-up work communication, anxiety when tasks expand, variable sleep and difficulty maintaining ordinary activities and a steady routine. The final clinician assessment is partial improvement with meaningful functional impact and continued treatment indicated. Full remission, work readiness, and completion of a return-to-work process are not established.

**Required facts for grading**

- Use both declining scores and concrete behavioral gains.
- Retain persistent avoidance, work-function limitations and sleep difficulty.
- Match final assessment of partial improvement; do not claim recovery.

**Failure modes:** score only recovery, negative findings omitted, planned action as completed.

**Evidence**

- BH-D002 · `intake_and_individual_jan05.txt` · lines 15
- BH-D011 · `individual_therapy_jan14.txt` · lines 11–17
- BH-D013 · `symptom_measure_review_jan16.txt` · lines 11–13
- BH-D110 · `BH-D110_individual_primary_record_2026-01-26.txt` · lines 9–13
- BH-D114 · `BH-D114_medication_management_2026-01-30.txt` · lines 8
- BH-D115 · `BH-D115_symptom_measure_review_2026-01-30.txt` · lines 5–12

## DEV-43 · longitudinal synthesis

Trace Rowan’s work-communication progress from early January through January 30. Distinguish a planned action, drafting, sending, and completed follow-up.

**Difficulty:** hard · **Answerability:** partially_determinate

**Ground truth**

January 5: planned to open the work inbox for five minutes. January 6: selected reading a work message as a next step. By January 14: reported opening a message but not replying; drafted a short acknowledgment in therapy. January 19: task narrowed to drafting two sentences, with no requirement to send that day. January 21: reported a draft but had stopped before sending. By January 26: reported sending a short message and receiving a request to discuss next steps, but still postponed scheduling that conversation. January 29: reported opening the work calendar but delaying a follow-up conversation. January 30: review confirms initial drafting/sending and ongoing follow-up delay. The exact send date and completed follow-up conversation are not established.

**Required facts for grading**

- Do not mark planned or rehearsed messages as sent.
- Unsent on Jan21; sent by Jan26, exact date unknown.
- No documented completed follow-up conversation or actual return to work.

**Failure modes:** plan as completed event, exact date invented, followup completion invented.

**Evidence**

- BH-D002 · `intake_and_individual_jan05.txt` · lines 17
- BH-D004 · `group_facilitator_jan06.txt` · lines 14
- BH-D011 · `individual_therapy_jan14.txt` · lines 11–17
- BH-D105 · `BH-D105_individual_2026-01-19.txt` · lines 11
- BH-D106 · `BH-D106_telehealth_2026-01-21.txt` · lines 9
- BH-D110 · `BH-D110_individual_primary_record_2026-01-26.txt` · lines 9–13
- BH-D107 · `BH-D107_group_activity_records_2026-01-22_and_29.txt` · lines 14
- BH-D115 · `BH-D115_symptom_measure_review_2026-01-30.txt` · lines 10

## DEV-44 · event clinical synthesis

What prompted the additional individual therapy contact on January 19, what was done, and what immediate response was documented?

**Difficulty:** medium · **Answerability:** determinate

**Ground truth**

Workplace-related group discussion made Rowan visibly tense and overwhelmed. The facilitator offered grounding and arranged a same-day individual visit. During the 30-minute contact, Mira Patel used paced breathing, orientation to the room, the coping card and a reduced task of drafting two sentences to a supervisor. Rowan reported immediate anxiety easing enough to discuss the next step. The note denies current suicidal thoughts and identifies no acute safety concern; it does not describe a suicide crisis as the reason for the extra contact or prove sustained resolution of anxiety.

**Required facts for grading**

- Triggered by overwhelm/anxiety during workplace discussion in group.
- Grounding/breathing/coping card and smaller drafting task.
- Immediate easing only; not evidence of sustained recovery or a suicidality-driven crisis.

**Failure modes:** crisis reason invented, transient response as remission, task completion invented.

**Evidence**

- BH-D101 · `BH-D101_group_content_2026-01-19.txt` · lines 10
- BH-D105 · `BH-D105_individual_2026-01-19.txt` · lines 6–13

## DEV-45 · intervention synthesis

Identify the recurring psychotherapy strategies used for avoidance and task initiation, with examples from different dates. What evidence distinguishes rehearsal from independent follow-through?

**Difficulty:** hard · **Answerability:** partially_determinate

**Ground truth**

The notes repeatedly use behavioral activation, breaking tasks into observable steps, separating anxious predictions from evidence, paced breathing/grounding, and communication rehearsal. Examples include a five-minute inbox task on January 5, drafting and reading an acknowledgment on January 14, two-sentence drafting/grounding on January 19, limiting repeated checking on January 21, and rehearsing a brief request on January 26. In-session participation shows ability to practice with support. Follow-through is separately evidenced by reported walks, opening a message, and sending one by January 26; continued delay and uncertainty using skills independently limit generalization.

**Required facts for grading**

- Multiple strategies with dated source examples.
- Separate in-session skill use from reported outside-session actions.
- Persistent follow-through limitations remain.

**Failure modes:** rehearsal as real world completion, intervention invented, independent mastery overclaimed.

**Evidence**

- BH-D002 · `intake_and_individual_jan05.txt` · lines 17
- BH-D011 · `individual_therapy_jan14.txt` · lines 11–17
- BH-D105 · `BH-D105_individual_2026-01-19.txt` · lines 11
- BH-D106 · `BH-D106_telehealth_2026-01-21.txt` · lines 9–11
- BH-D110 · `BH-D110_individual_primary_record_2026-01-26.txt` · lines 9–13
- BH-D111 · `BH-D111_individual_second_record_2026-01-26.txt` · lines 12–14

## DEV-46 · longitudinal synthesis

Summarize the course of sleep difficulty during the episode. Does the record support saying that sleep normalized by the final week?

**Difficulty:** medium · **Answerability:** partially_determinate

**Ground truth**

No sustained normalization is established. Intake describes fragmented sleep, nighttime waking/time checking and fatigue. A poor night preceded the January 8 missed appointment. January 14 still notes interrupted sleep and difficult mornings. January 21 reports one improved night followed by prolonged wakefulness; January 26 notes uneven sleep and repetitive work-related thoughts. January 30 still describes variable sleep and intermittent sleep disruption affecting routine. Brief improvement on one night does not establish resolution.

**Required facts for grading**

- Sleep problems persist across the episode including final week.
- One improved night on Jan21 is followed by a poor night.
- No supported exact nightly duration or normalization.

**Failure modes:** single good night as recovery, sleep duration invented.

**Evidence**

- BH-D002 · `intake_and_individual_jan05.txt` · lines 11–13
- BH-D015 · `missed_visit_outreach_jan08.txt` · lines 15
- BH-D011 · `individual_therapy_jan14.txt` · lines 11
- BH-D106 · `BH-D106_telehealth_2026-01-21.txt` · lines 11
- BH-D110 · `BH-D110_individual_primary_record_2026-01-26.txt` · lines 9
- BH-D114 · `BH-D114_medication_management_2026-01-30.txt` · lines 8
- BH-D115 · `BH-D115_symptom_measure_review_2026-01-30.txt` · lines 8–10

## DEV-47 · source attribution

Which January 16 observations came from Casey, and which came from Rowan’s own questionnaire update? Why does that distinction matter?

**Difficulty:** medium · **Answerability:** determinate

**Ground truth**

Casey’s collateral report describes short walks, greater willingness to discuss the coming week, difficult mornings, becoming quiet around work, fewer unplanned reminders and less argument with a planned check-in. Rowan was absent from that appointment. Rowan’s own portal update says getting out of the apartment was a little easier, work thoughts still prompted postponement and sleep was inconsistent. The accounts are distinct sources; do not describe Casey’s collateral discussion as a patient interview or count it as Rowan’s psychotherapy.

**Required facts for grading**

- Correctly attribute collateral observations to Casey and portal statements to Rowan.
- Rowan absent from collateral; the portal form is separate evidence.

**Failure modes:** collateral as patient report, sources blended, absent patient included.

**Evidence**

- BH-D012 · `partner_collateral_jan16.txt` · lines 8–17
- BH-D013 · `symptom_measure_review_jan16.txt` · lines 6–15

## DEV-48 · longitudinal synthesis

What family communication plan was developed on January 9, and how was that theme revisited on January 30? Does the later note prove the issue was already resolved?

**Difficulty:** medium · **Answerability:** partially_determinate

**Ground truth**

January 9 emphasized one predictable check-in instead of repeated reminders, asking for specific support, preserving Rowan’s ownership of work preparation, and shared activity such as an evening walk. January 30 revisited reminders that escalated discussion and withdrawal; Casey practiced asking whether Rowan wanted company, practical help or a later check-in, and both again agreed to one planned brief check-in. The later session shows continued work on the issue, not proof it had resolved. Rowan found a limited plan more manageable, but no later outcome of that home practice is provided.

**Required facts for grading**

- Compare agreed limited check-ins and specific support requests across both visits.
- January 30 includes recurrence/rehearsal, not established resolution.
- Do not invent outcome after the final session.

**Failure modes:** plan as outcome, family problem resolved invented.

**Evidence**

- BH-D007 · `family_primary_jan09.txt` · lines 12–18
- BH-D008 · `family_cofacilitator_jan09.txt` · lines 13–15
- BH-D113 · `BH-D113_family_therapy_2026-01-30.txt` · lines 9–13

## DEV-49 · clinical evidence limits

What safety-related findings are explicitly documented, and what would be too strong a conclusion about risk across the entire episode?

**Difficulty:** hard · **Answerability:** partially_determinate

**Ground truth**

Intake identifies no immediate safety concern and discussion of support/help seeking. January 19 documents denial of current suicidal thoughts, future orientation and no acute safety concern. January 21 says no urgent safety concern was reported. January 26 primary note reports no current suicidal ideation. January 30 medication note documents denial of current suicidal thoughts and no new acute safety issue; the January 30 PHQ-9 item 9 is 0. These are findings at documented contacts, not proof of zero risk at all times, no lifetime history, or earlier item 9 scores. The supplied notes do not provide a comprehensive longitudinal risk history.

**Required facts for grading**

- Distinguish dated narrative findings from Jan30 item 9=0.
- Do not infer lifetime absence, zero risk throughout, or missing questionnaire scores.

**Failure modes:** negative findings overgeneralized, missing history as negative, item scores imputed.

**Evidence**

- BH-D002 · `intake_and_individual_jan05.txt` · lines 13
- BH-D105 · `BH-D105_individual_2026-01-19.txt` · lines 13
- BH-D106 · `BH-D106_telehealth_2026-01-21.txt` · lines 11
- BH-D110 · `BH-D110_individual_primary_record_2026-01-26.txt` · lines 13
- BH-D114 · `BH-D114_medication_management_2026-01-30.txt` · lines 10
- BH-D115 · `BH-D115_symptom_measure_review_2026-01-30.txt` · lines 5–6

## DEV-50 · missing data

What medication, dose, and dosing schedule was Rowan taking, and can those details be reconstructed from the medication-management notes?

**Difficulty:** easy · **Answerability:** not_established

**Ground truth**

The supplied documents do not name the medication, dose or dosing schedule. They say the medication list/regimen was reviewed, and January 30 reports adherence and continuation of the current regimen, but the referenced active medication list is not included. These details cannot be reconstructed without that list or the prescription record.

**Required facts for grading**

- Medication name, dose and schedule are not provided.
- Referenced chart/list is not available within the supplied corpus; do not guess.

**Failure modes:** medication name hallucinated, dose inferred from symptoms, referenced document assumed available.

**Evidence**

- BH-D010 · `medication_review_jan13.txt` · lines 11–17
- BH-D114 · `BH-D114_medication_management_2026-01-30.txt` · lines 8–12

## DEV-51 · direct retrieval

Was medication changed on January 30, and what did Rowan report about adherence and new adverse effects?

**Difficulty:** easy · **Answerability:** determinate

**Ground truth**

No medication change was made on January 30; the plan was to continue the current regimen and monitor sleep/tolerability. Rowan reported taking medication as prescribed and did not describe a new adverse effect. This is patient report at that visit, not proof that no adverse effect ever occurred.

**Required facts for grading**

- No change; continue current regimen.
- Reported adherence and no newly described adverse effect.

**Failure modes:** medication change invented, negative report as universal absence.

**Evidence**

- BH-D114 · `BH-D114_medication_management_2026-01-30.txt` · lines 8–12

## DEV-52 · missing data

Which formal psychiatric diagnosis and diagnostic code are established by these documents? Distinguish clinical symptom descriptions from a coded diagnosis.

**Difficulty:** medium · **Answerability:** not_established

**Ground truth**

The supplied records describe depressive symptoms, anxiety, behavioral avoidance, sleep disruption and functional difficulty. They do not establish a named coded psychiatric diagnosis or provide an ICD diagnosis code. PHQ-9 totals and symptom descriptions alone should not be turned into a specific diagnostic code or a formal diagnosis that the records do not state.

**Required facts for grading**

- Symptoms are documented; a formal coded diagnosis is not supplied.
- Do not assign an ICD code or diagnose from PHQ-9 totals.

**Failure modes:** screening score as diagnosis, diagnostic code hallucinated.

**Evidence**

- BH-D002 · `intake_and_individual_jan05.txt` · lines 11–15
- BH-D003 · `signed_treatment_plan_jan05.txt` · lines 10
- BH-D010 · `medication_review_jan13.txt` · lines 15
- BH-D111 · `BH-D111_individual_second_record_2026-01-26.txt` · lines 14
- BH-D115 · `BH-D115_symptom_measure_review_2026-01-30.txt` · lines 8–12

## DEV-53 · false premise

On what date did Rowan return to work, and what work schedule or employment clearance had been approved by the end of the episode?

**Difficulty:** medium · **Answerability:** not_established

**Ground truth**

No actual return-to-work date, approved work schedule or employment clearance is established. The records document preparation, message drafting/sending, a supervisor request to discuss next steps, and continued delayed follow-up. The January 23 coordination note explicitly says no employment determination was made. Do not convert discussion of a possible gradual return into an approved or completed return.

**Required facts for grading**

- Actual return date, approved schedule and clearance are not established.
- Planning and communication progress are distinct from completed return or approval.

**Failure modes:** work clearance invented, planned return as actual, supervisor request as approval.

**Evidence**

- BH-D106 · `BH-D106_telehealth_2026-01-21.txt` · lines 9
- BH-D109 · `BH-D109_care_coordination_2026-01-23.txt` · lines 9–13
- BH-D110 · `BH-D110_individual_primary_record_2026-01-26.txt` · lines 9
- BH-D107 · `BH-D107_group_activity_records_2026-01-22_and_29.txt` · lines 14
- BH-D115 · `BH-D115_symptom_measure_review_2026-01-30.txt` · lines 10–12

## DEV-54 · causal inference limits

Can the documents establish whether psychotherapy or medication caused the PHQ-9 improvement, or which treatment was more effective?

**Difficulty:** hard · **Answerability:** not_established

**Ground truth**

No. The records show symptom improvement over time alongside psychotherapy and medication management, but do not isolate causal effects or compare treatments. There is no documented treatment-effect comparison that attributes the 18-to-10 decline to one modality. The notes support a descriptive account of concurrent care, reported changes and continuing difficulties; they do not establish comparative efficacy.

**Required facts for grading**

- Temporal association and concurrent care do not establish causation or comparative efficacy.
- May report decline and partial improvement without treatment attribution.

**Failure modes:** post hoc causality, comparative efficacy invented.

**Evidence**

- BH-D002 · `intake_and_individual_jan05.txt` · lines 15
- BH-D013 · `symptom_measure_review_jan16.txt` · lines 11–13
- BH-D010 · `medication_review_jan13.txt` · lines 11–17
- BH-D114 · `BH-D114_medication_management_2026-01-30.txt` · lines 8–12
- BH-D115 · `BH-D115_symptom_measure_review_2026-01-30.txt` · lines 5–12

## DEV-55 · entity resolution

Identify the documented clinicians for January 9 family therapy, January 19 therapy, January 26 individual therapy, and January 30 medication management. Do multiple clinicians imply additional patient sessions?

**Difficulty:** medium · **Answerability:** determinate

**Ground truth**

January 9 HG-E104: Mara Voss, LCSW, with Leena Park, LPC, one family session. January 19: Leah Chen, LCSW, facilitated group HG-E110; Mira Patel, LCSW, delivered separate individual HG-E111, so two distinct sessions. January 26 HG-E115: Mira Patel and Nora Ellis, both LCSWs, documented the same individual session. January 30 medication HG-E120: Elena Ortiz, PMHNP. Multiple clinician names alone do not establish multiple patient encounters.

**Required facts for grading**

- Map clinicians to dates and encounter IDs correctly.
- One Jan9 session, two Jan19 sessions, one Jan26 session.
- Jan30 medication prescriber is Elena Ortiz, distinct from Jan13 Elias Brenner.

**Failure modes:** clinician names merged, provider count as session count.

**Evidence**

- BH-D007 · `family_primary_jan09.txt` · lines 6–10
- BH-D008 · `family_cofacilitator_jan09.txt` · lines 6–8
- BH-D101 · `BH-D101_group_content_2026-01-19.txt` · lines 3–5
- BH-D105 · `BH-D105_individual_2026-01-19.txt` · lines 3–7
- BH-D110 · `BH-D110_individual_primary_record_2026-01-26.txt` · lines 3–7
- BH-D111 · `BH-D111_individual_second_record_2026-01-26.txt` · lines 4–10
- BH-D114 · `BH-D114_medication_management_2026-01-30.txt` · lines 3–6

## DEV-56 · entity resolution

Do the early-January and later-January records refer to the same patient despite changes in clinician names? Identify the chart identifiers supporting the match.

**Difficulty:** easy · **Answerability:** determinate

**Ground truth**

Yes. Both early and later records identify Rowan Mercer, date of birth 1991-04-12, MRN HG-M042, at Harbor Grove Behavioral Health. Different treating clinicians do not imply different patients. Casey Mercer is identified as Rowan’s partner, not the patient whose therapy participation is being counted.

**Required facts for grading**

- Rowan Mercer, DOB 1991-04-12, MRN HG-M042 match.
- Casey is partner; clinicians are separate entities.

**Failure modes:** patient split by provider, partner as patient.

**Evidence**

- BH-D002 · `intake_and_individual_jan05.txt` · lines 4–8
- BH-D012 · `partner_collateral_jan16.txt` · lines 5–8
- BH-D110 · `BH-D110_individual_primary_record_2026-01-26.txt` · lines 2–6
- BH-D113 · `BH-D113_family_therapy_2026-01-30.txt` · lines 4–9

## DEV-57 · missing data

What reasons are documented for Rowan’s partial group attendance on January 6 and late arrival on January 22? Can the same explanation be assigned to both dates?

**Difficulty:** medium · **Answerability:** partially_determinate

**Ground truth**

January 6: parking difficulty caused late arrival, and a previously arranged ride required early departure; the roster records 10:15–11:15. January 22: late arrival at 10:30 is documented, but no reason for the lateness is supplied. It would be unsupported to copy January 6’s parking or ride explanation to January 22, or attribute January 22 lateness to anxiety without evidence.

**Required facts for grading**

- Jan6 reasons: parking delay and prearranged ride.
- Jan22 late arrival established, reason not documented.

**Failure modes:** reason copied between dates, plausible cause hallucinated.

**Evidence**

- BH-D005 · `early_group_attendance_roster.txt` · lines 10–13
- BH-D107 · `BH-D107_group_activity_records_2026-01-22_and_29.txt` · lines 7–9
- BH-D108 · `BH-D108_final_attendance_and_cancellation_register.txt` · lines 9–14

## DEV-58 · temporal provenance

Give three examples in which a signature, receipt, or import date differs from the underlying service or assessment date. Explain the effect on date-based counts.

**Difficulty:** medium · **Answerability:** determinate

**Ground truth**

Leena Park’s family note signed January 10 documents the January 9 HG-E104 visit; it adds no January 10 service. BH-D104 received January 26 retransmits the January 19 HG-E110 roster; it adds no January 26 group. BH-D014 received January 26 imports the January 16 HG-Q116 score; it adds no January 26 questionnaire or therapy appointment. Use the underlying event date and shared identifiers, not processing timestamps, for event counts.

**Required facts for grading**

- Jan10 signature→Jan9 family visit; Jan26 roster receipt→Jan19 group; Jan26 measure import→Jan16 assessment.
- No new service/assessment dates created by processing.

**Failure modes:** processing date as event date, duplicate event counted.

**Evidence**

- BH-D008 · `family_cofacilitator_jan09.txt` · lines 6–11
- BH-D104 · `BH-D104_resent_roster_received_2026-01-26.txt` · lines 4–20
- BH-D014 · `imported_measure_summary_received_jan26.txt` · lines 6–19

## DEV-59 · source reconciliation

A reviewer resolves all discrepancies by selecting the latest received or latest signed document. Would that rule produce defensible answers for January 19 and January 26?

**Difficulty:** hard · **Answerability:** determinate

**Ground truth**

No. For January 19, the explicit correction in BH-D103 supersedes the departure field in the original; the later-received BH-D104 is merely a resend of the original without the correction. Use 11:15. For January 26, the later-signed BH-D111 is a conflicting final account of the same full encounter, not an explicit amendment to BH-D110. Signature recency alone does not resolve 40 versus 50 minutes. Provenance and the scope of an actual correction matter; a blanket latest-document rule would discard valid evidence.

**Required facts for grading**

- Jan19 has a resolved explicit correction; later original copy does not supersede it.
- Jan26 remains an unresolved full-duration conflict despite later signature.
- Do not apply recency as a universal precedence rule.

**Failure modes:** latest receipt wins, later signature automatically wins, conflict and correction conflated.

**Evidence**

- BH-D103 · `BH-D103_attendance_correction_2026-01-20.txt` · lines 7–16
- BH-D104 · `BH-D104_resent_roster_received_2026-01-26.txt` · lines 8–20
- BH-D110 · `BH-D110_individual_primary_record_2026-01-26.txt` · lines 7–16
- BH-D111 · `BH-D111_individual_second_record_2026-01-26.txt` · lines 7–17

## DEV-60 · time window scope

Can the final Monday–Sunday week be reported as a complete observed week through February 1? Explain the review-period boundary and the strongest supported weekly conclusion.

**Difficulty:** hard · **Answerability:** partially_determinate

**Ground truth**

The final calendar week is January 26–February 1, but the requested episode/review period ends January 30. The supplied in-scope therapy is on January 26, 29 and 30, giving 3 days and 145 or 155 minutes. Those services meet the day goal; the minute goal and combined status are unresolved because of January 26’s conflict. No supplied record establishes services or absence of services on January 31 or February 1. Label the last week as review-period coverage through January 30 rather than implying a complete observation of both outside-period days.

**Required facts for grading**

- Calendar week ends Feb1 but review ends Jan30.
- In-scope 3 days and 145 or 155 minutes; overall status unresolved.
- Do not infer outside-period services or assert those days are confirmed service-free.

**Failure modes:** wrong week boundary, out of scope absence inferred, unobserved care invented.

**Evidence**

- BH-D003 · `signed_treatment_plan_jan05.txt` · lines 6–12
- BH-D110 · `BH-D110_individual_primary_record_2026-01-26.txt` · lines 3–7
- BH-D111 · `BH-D111_individual_second_record_2026-01-26.txt` · lines 4–10
- BH-D107 · `BH-D107_group_activity_records_2026-01-22_and_29.txt` · lines 12–17
- BH-D108 · `BH-D108_final_attendance_and_cancellation_register.txt` · lines 12–20
- BH-D113 · `BH-D113_family_therapy_2026-01-30.txt` · lines 5–7

## DEV-61 · deduplication

Which record pairs or groups should be linked as documentation of the same underlying event rather than counted as separate events? Include both encounters and symptom measurements.

**Difficulty:** hard · **Answerability:** determinate

**Ground truth**

Link BH-D007/BH-D008 to January 9 family HG-E104; BH-D101/BH-D102/BH-D103/BH-D104 to January 19 group HG-E110 (content, original attendance, correction and resend); both January 21 calls in BH-D106 to HG-E112/HG-A112; BH-D110/BH-D111 to January 26 HG-E115/HG-A115; and BH-D013/BH-D014 to January 16 PHQ-9 form HG-Q116. Also link each group’s activity and roster entries by encounter/date rather than counting each source as a visit. The January 27 draft and charge in BH-D112 and no-show in BH-D108 concern HG-E116, an undelivered appointment. BH-D107 and BH-D108 each cover multiple events, so file-level deduplication alone also fails.

**Required facts for grading**

- Link cofacilitator, roster/correction/resend, reconnect and competing clinician records by event identifiers.
- Deduplicate Jan16 measurement and its Jan26 import.
- One file can contain multiple events; one event can have multiple files.
- Link Jan27 evidence without creating an attended encounter.

**Failure modes:** one file one event, duplicate note counted, file level deduplication only.

**Evidence**

- BH-D007 · `family_primary_jan09.txt` · lines 6–10
- BH-D008 · `family_cofacilitator_jan09.txt` · lines 6–11
- BH-D101 · `BH-D101_group_content_2026-01-19.txt` · lines 3–6
- BH-D102 · `BH-D102_original_attendance_2026-01-19.txt` · lines 4–10
- BH-D103 · `BH-D103_attendance_correction_2026-01-20.txt` · lines 5–11
- BH-D104 · `BH-D104_resent_roster_received_2026-01-26.txt` · lines 8–20
- BH-D106 · `BH-D106_telehealth_2026-01-21.txt` · lines 3–19
- BH-D110 · `BH-D110_individual_primary_record_2026-01-26.txt` · lines 3–7
- BH-D111 · `BH-D111_individual_second_record_2026-01-26.txt` · lines 4–10
- BH-D013 · `symptom_measure_review_jan16.txt` · lines 6–9
- BH-D014 · `imported_measure_summary_received_jan26.txt` · lines 12–19
- BH-D107 · `BH-D107_group_activity_records_2026-01-22_and_29.txt` · lines 7–17
- BH-D108 · `BH-D108_final_attendance_and_cancellation_register.txt` · lines 8–16
- BH-D112 · `BH-D112_draft_note_and_charge_extract_2026-01-27.txt` · lines 5–25

## DEV-62 · evidence sufficiency

Would the appointment-status export alone support an accurate therapy-minute total for January 5–16? Identify what additional evidence is necessary.

**Difficulty:** hard · **Answerability:** determinate

**Ground truth**

No. BH-D006 provides scheduled slots and broad statuses, not sufficient patient-specific treatment intervals or service eligibility. January 6 requires the actual arrival/departure roster and break note; January 12 requires its break note despite a completed status. January 9 requires recognizing cofacilitator notes as one patient-present session; January 16 requires the collateral note showing Rowan absent despite completed status. January 13 medication management is not therapy. Direct individual notes establish actual contact. Combining these sources yields 5 attended therapy encounters on 5 days and 260 patient therapy minutes for January 5–16.

**Required facts for grading**

- Export alone insufficient because scheduled time/completed status does not establish eligible actual therapy time.
- Need actual attendance, break and patient-presence/service evidence.
- Correct combined result 5 sessions, 5 days, 260 minutes.

**Failure modes:** status export as gold truth, completed status as patient attendance, scheduled duration as treatment.

**Evidence**

- BH-D006 · `early_appointment_status_export.txt` · lines 9–20
- BH-D002 · `intake_and_individual_jan05.txt` · lines 6–8
- BH-D004 · `group_facilitator_jan06.txt` · lines 12
- BH-D005 · `early_group_attendance_roster.txt` · lines 9–11
- BH-D007 · `family_primary_jan09.txt` · lines 6–9
- BH-D008 · `family_cofacilitator_jan09.txt` · lines 6–8
- BH-D009 · `group_facilitator_jan12.txt` · lines 12
- BH-D010 · `medication_review_jan13.txt` · lines 17
- BH-D011 · `individual_therapy_jan14.txt` · lines 6–8
- BH-D012 · `partner_collateral_jan16.txt` · lines 6–17

## DEV-63 · billing evidence limits

Does the January 27 charge extract establish that a payer paid for the session, that the charge was reversed, or which psychotherapy billing code was used?

**Difficulty:** medium · **Answerability:** not_established

**Ground truth**

It establishes only that charge CH-116 for HG-E116 was shown as posted, with description Group psychotherapy, quantity 1 and posting timestamp January 27 at 18:06 in the January 30 extract. No payer payment, denial, reversal, refund, claim adjudication or specific procedure code is supplied. Clinical attendance independently shows no patient treatment; do not infer financial settlement or a billing code from the generic description.

**Required facts for grading**

- Posted charge and quantity are documented; payment/reversal/code are not.
- No-show evidence answers delivery, not claim settlement.

**Failure modes:** posted as paid, reversal invented, billing code hallucinated.

**Evidence**

- BH-D112 · `BH-D112_draft_note_and_charge_extract_2026-01-27.txt` · lines 18–27
- BH-D108 · `BH-D108_final_attendance_and_cancellation_register.txt` · lines 10–16

## DEV-64 · missing data

What reasons are known for each January 8, 15, 27 and 28 undelivered appointment, and which reason remains undocumented?

**Difficulty:** medium · **Answerability:** partially_determinate

**Ground truth**

January 8: Rowan reported the morning got away after poor sleep; individual no-show. January 15: clinic staff illness with no covering facilitator; clinic-cancelled group. January 27: group no-show, but no patient explanation is documented; an outreach message was left without clinical discussion. January 28: Rowan cancelled for a personal scheduling conflict. Do not copy the earlier poor-sleep explanation to January 27 or attribute the clinic cancellation to Rowan.

**Required facts for grading**

- Correct reasons for Jan8, Jan15 and Jan28.
- Jan27 reason is not documented.
- Keep patient and clinic causes separate.

**Failure modes:** reason copied between dates, undocumented reason fabricated, clinic cancellation as patient behavior.

**Evidence**

- BH-D015 · `missed_visit_outreach_jan08.txt` · lines 9–17
- BH-D016 · `group_cancellation_notice_jan15.txt` · lines 9–15
- BH-D108 · `BH-D108_final_attendance_and_cancellation_register.txt` · lines 16–18

## DEV-65 · evidence gap resolution

What targeted clarification would settle the unresolved January 26 time and the resulting final-week goal status? Which already available administrative records would not resolve it?

**Difficulty:** hard · **Answerability:** partially_determinate

**Ground truth**

Obtain an explicit clinician clarification/corrected signed record for HG-E115/HG-A115, or a reliable contemporaneous patient arrival/contact record that adjudicates whether therapy began at 09:00 or 09:10. Both final notes claim to describe full patient contact and agree on a 09:50 end. A substantiated 40-minute contact yields 145 final-week minutes, below 150; 50 yields 155, above 150, with 3 days in either case. The later receipt of an unrelated January 19 roster, January 16 measurement import, January 27 charge, or a note’s signature order does not establish January 26’s actual start. This describes evidence needed; it does not claim clarification was obtained.

**Required facts for grading**

- Need adjudication of Jan26 full patient-contact start, not another duplicate.
- 40 minutes→145/not met; 50→155/met; day goal met either way.
- Do not claim unavailable clarification or unrelated administrative data resolve it.

**Failure modes:** missing evidence assumed obtained, irrelevant record as resolution, latest signature wins.

**Evidence**

- BH-D110 · `BH-D110_individual_primary_record_2026-01-26.txt` · lines 3–16
- BH-D111 · `BH-D111_individual_second_record_2026-01-26.txt` · lines 4–17
- BH-D003 · `signed_treatment_plan_jan05.txt` · lines 12
- BH-D107 · `BH-D107_group_activity_records_2026-01-22_and_29.txt` · lines 12–17
- BH-D108 · `BH-D108_final_attendance_and_cancellation_register.txt` · lines 12–20
- BH-D113 · `BH-D113_family_therapy_2026-01-30.txt` · lines 6–7
- BH-D104 · `BH-D104_resent_roster_received_2026-01-26.txt` · lines 8–20
- BH-D014 · `imported_measure_summary_received_jan26.txt` · lines 12–19
- BH-D112 · `BH-D112_draft_note_and_charge_extract_2026-01-27.txt` · lines 18–25

