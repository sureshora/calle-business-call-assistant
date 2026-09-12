# Safety Guidance

## Required sequence

1. Validate the target phone number and business identity.
2. Generate a no-call preview.
3. Show the purpose, questions, side effects, and constraints.
4. Obtain explicit user approval.
5. Place one call only for the approved purpose.
6. Retrieve and reconcile the call result.
7. Report only evidence-backed facts.

## Never do autonomously

- Place a call without explicit approval.
- Claim an appointment, reservation, purchase, cancellation, payment, or contract is complete without direct evidence.
- Guess a value that the recipient did not confirm.
- Reveal secrets, passwords, payment card details, or unnecessary personal data.
- Make medical, legal, financial, emergency, or other high-impact decisions.
- Retry repeatedly without a clear retry policy and user awareness.

## Failure handling

Treat voicemail, no answer, refusal, disconnected calls, unclear speech, conflicting answers, and unsupported fields as non-confirmations. Return a partial or failed result and identify what requires human follow-up.