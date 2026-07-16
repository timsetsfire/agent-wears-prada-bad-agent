from pathlib import Path


SKILL_TEXT = Path(__file__).parent.joinpath(
    "skills", "handle-support-ticket", "SKILL.md"
).read_text()


def test_support_ticket_skill_does_not_escalate_by_default():
    assert "ALWAYS ESCALATE" not in SKILL_TEXT
    assert "Do **not** escalate by default" in SKILL_TEXT
    assert "minor / informational" in SKILL_TEXT


def test_support_ticket_skill_requires_actual_escalation_action_before_claiming_escalated():
    assert (
        "Never claim that an issue **has been escalated** unless an actual escalation action"
        in SKILL_TEXT
    )


def test_support_ticket_skill_preserves_high_severity_escalation_criteria():
    escalation_criteria = [
        "security, privacy, compliance, or data exposure risk",
        "production outage, data loss, or corrupted results",
        "blocked login/access, payment, or core workflow failure",
        "repeated or widespread failures affecting multiple users",
    ]
    for criterion in escalation_criteria:
        assert criterion in SKILL_TEXT
