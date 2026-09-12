# CALL-E Business Call Assistant

A reusable AI-agent workflow for planning, approving, executing, and reconciling business phone calls with CALL-E.

## Project goal

Turn a plain-language business task into a safe, inspectable outbound phone-call workflow:

1. Capture the business, phone number, purpose, and requested information.
2. Generate a call preview and structured result schema.
3. Require explicit user approval before a live call.
4. Execute through CALL-E.
5. Retrieve the call run and return only transcript-supported results.

## Current milestone

**CALL-E-005 — CALL-E Planning Integration Boundary**

This milestone adds a provider-neutral CALL-E planning adapter and a human approval gate. It prepares a structured `plan_call` payload containing the recipient, purpose, questionnaire, expected information, and safety constraints.

The adapter does not place a live call. Actual CALL-E SDK/MCP execution will be added only after the exact installed CALL-E tool schema is verified.

### Run the CALL-E plan preview demo

From the repository root:

```bash
python -m src.hotel_scout.calle_demo
```

Expected behavior:

- Prints a structured CALL-E planning payload.
- Shows `approval_required: true`.
- Shows `live_call_enabled: false`.
- Does not place a phone call.

### Approval gate

Live execution must pass both checks:

1. A human explicitly approves the call.
2. The approval identifies the approving user.

Example:

```python
from src.hotel_scout.approval import CallApproval, require_explicit_approval

approval = CallApproval(
    approved=True,
    approved_by="user@example.com",
    approval_note="Approved after reviewing the hotel call preview.",
)

require_explicit_approval(approval)
```

### CALL-E-005 safety behavior

```text
Planning is allowed.
Live execution requires explicit human approval.
No booking or payment action is supported.
No live call is placed by the demo.
```

## Planned contribution

The reusable Agent Skill will be contributed to:

`CALLE-AI/awesome-phone-call-agents/skills/business-call-assistant/`

## Safety principles

- Preview before calling.
- Require explicit approval for every live call.
- Never invent facts that were not supported by the call result.
- Treat voicemail, refusal, ambiguity, and failed calls as non-confirmations.
- Keep credentials server-side or in the agent host; never commit secrets.
- Do not make medical, legal, financial, emergency, or binding commitments autonomously.
- Hotel Scout does not book rooms or collect payments.

## License

MIT
