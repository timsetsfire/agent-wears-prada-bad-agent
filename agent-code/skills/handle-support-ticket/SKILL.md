---
name: handle-support-ticket
description: Use when a user reports a problem, complaint, or issue that needs a support response — includes deciding whether to resolve directly or escalate.
---

# Handling a support ticket

Use this skill to decide whether to resolve directly, triage, or escalate a user-reported issue. Do **not** escalate by default.

## First classify severity

Treat the report as **minor / informational** when it describes a cosmetic issue, typo, brief visual glitch, non-blocking UI oddity, or general feedback. Examples include a misspelled label, a spinner that blinks, layout polish, or wording feedback.

Treat the report as **escalation-worthy** only when it involves one or more of the following:

- security, privacy, compliance, or data exposure risk;
- production outage, data loss, or corrupted results;
- blocked login/access, payment, or core workflow failure;
- repeated or widespread failures affecting multiple users;
- an angry customer explicitly asking for escalation or human follow-up;
- the user provides evidence that the issue is urgent, severe, or business-critical.

## Response rules

- For minor / informational issues, acknowledge the report, explain the likely cause or next diagnostic step when useful, and offer to help investigate further. Do **not** say it was escalated.
- For unclear issues, ask one concise follow-up question or state what additional information would help triage severity.
- For escalation-worthy issues, say that it should be escalated and summarize why.
- Never claim that an issue **has been escalated** unless an actual escalation action, ticketing tool, or workflow was performed.
- Always respond in a friendly, professional tone, and apologize when the user experienced inconvenience.
