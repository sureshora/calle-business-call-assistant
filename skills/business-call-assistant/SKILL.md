---
name: business-call-assistant
description: Plan and safely execute one approved CALL-E outbound business inquiry, then return only transcript-supported structured results.
---

# Business Call Assistant

Use this skill when a user wants an AI agent to contact a business by phone to collect specific information such as availability, rates, service windows, appointment options, delivery estimates, or other bounded operational facts.

## Core workflow

1. Collect the business name, exact phone number, purpose, requested fields, constraints, and desired timing.
2. Validate that the request is a bounded information-gathering task.
3. Produce a no-call preview containing the target, purpose, questions, expected result fields, side effects, and constraints.
4. Ask for explicit approval before any live call.
5. After approval, map the approved task to CALL-E `plan_call`.
6. Execute only the approved call through CALL-E `run_call`.
7. Retrieve the outcome using `get_call_run`.
8. Reconcile the call status and transcript before producing the final result.
9. Return only facts supported by the call. Mark unsupported, conflicting, or unclear values as unknown.

## Required inputs

- `business_name`
- `phone_number` in a valid international format when possible
- `purpose`
- `requested_information`
- `constraints`
- `user_approved`

See `references/call-task-schema.md` for the contract.

## Preview requirements

The preview must show:

- Who will be called and the phone number
- Why the call is being made
- The exact questions the agent intends to ask
- What information will be returned
- That the call may involve an AI voice and provider transcription
- Any limits, such as no booking, no payment, no purchase, and no commitments
- A clear request for explicit approval

## Live-call rules

- Never place a call without explicit user approval in the current workflow.
- Place one call for one approved purpose unless the user approves a defined retry.
- Do not disclose secrets, passwords, payment details, or unnecessary personal data.
- Do not make medical, legal, financial, emergency, or binding decisions.
- Do not claim that a booking, cancellation, purchase, payment, or contract is complete unless the call result explicitly supports it and the user authorized that action.

## Result rules

Use the result statuses defined in `references/call-task-schema.md`:

`confirmed`, `partial`, `unavailable`, `voicemail`, `refused`, `failed`, or `ambiguous`.

Every reported fact should have transcript evidence or be labeled unknown. Voicemail, no answer, refusal, disconnected calls, unclear speech, and conflicting answers are not confirmations.

## No-call mode

When CALL-E is not authenticated or the user has not approved a live call, remain in preview mode. Do not simulate a successful call as if it were real. A dry-run may show the planned questions and an illustrative result, but it must be clearly labeled as illustrative.