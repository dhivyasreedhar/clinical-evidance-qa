from clinical.api.contracts import GoalThreshold, LedgerRow


def test_record_values_with_several_values_are_shown_not_rejected():
    row = LedgerRow.model_validate(
        {
            "id": "E1",
            "date": "2026-01-05",
            "weekday": "Monday",
            "service": "group",
            "attendance": {"scenarios": ["attended", "not_present"]},
            "disposition": "excluded",
            "minutes": {"scenarios": [40, 50]},
            "status": "conflicting",
            "reason": ["staff illness", "facilitator unavailable"],
            "citations": [],
        }
    )
    assert row.reason == "staff illness; facilitator unavailable"
    assert row.attendance == "attended or not_present"
    assert row.minutes == [40, 50]
    threshold = GoalThreshold.model_validate(
        {"threshold": "at least 150 minutes", "measured": [145, 155], "outcome": "cannot_determine"}
    )
    assert threshold.measured == [145, 155]
    assert GoalThreshold.model_validate(
        {"threshold": "at least 3 days", "measured": 3, "outcome": "met"}
    ).measured == [3]
