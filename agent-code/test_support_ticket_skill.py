import unittest
from pathlib import Path


class SupportTicketSkillTest(unittest.TestCase):
    def test_support_ticket_skill_uses_severity_based_escalation(self):
        skill_text = Path("skills/handle-support-ticket/SKILL.md").read_text().lower()

        self.assertNotIn("always escalate", skill_text)
        self.assertIn("escalate only when", skill_text)
        self.assertIn("do not escalate low-severity feedback", skill_text)
        self.assertIn("cosmetic ui observations", skill_text)
        self.assertIn("minor copy/typo reports", skill_text)
        self.assertIn("direct response or next step", skill_text)


if __name__ == "__main__":
    unittest.main()
