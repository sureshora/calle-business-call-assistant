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

**CALL-E-004 — Hotel Scout Dry-Run Workflow**

This milestone adds the first executable, no-call hotel comparison workflow. It validates a hotel search request, accepts up to three candidate hotels, generates a standardized questionnaire, renders an approval preview, and defines transparent ranking weights.

### Run the dry-run demo

From the repository root:

```bash
python -m src.hotel_scout.demo
```

The demo uses placeholder hotel names and phone numbers. It does not place calls, make reservations, or collect payments.

### CALL-E-004 safety behavior

```text
Live calls allowed: False
No call will be placed in this dry-run.
No booking or payment action is supported.
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
