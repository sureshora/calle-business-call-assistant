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

**CALL-E-001 — Reusable Skill Foundation**

This milestone contains the workflow contract, safety boundaries, and examples. Live CALL-E execution will be added in the next milestone after CLI/MCP authentication is verified.

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

## License

MIT