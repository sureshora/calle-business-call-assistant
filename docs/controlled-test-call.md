# CALL-E-007 — Controlled Test Call

## Purpose

CALL-E-007 prepares a single controlled test call before Hotel Scout is allowed to contact real hotels.

## Requirements

- The destination number must belong to the project owner or a person who has explicitly authorized the test.
- Use international phone-number format, such as `+91...`.
- Do not use a hotel, customer, emergency service, or unknown recipient.
- The test message must not request a booking, payment, password, OTP, or sensitive information.
- The caller must identify the call as a controlled technical test.

## Environment configuration

```bash
export CALLE_TEST_PHONE_NUMBER="+91XXXXXXXXXX"
export CALLE_TEST_AUTHORIZED_BY="Suresh"
export CALLE_ALLOW_LIVE_CALLS="0"
```

Live calls remain disabled until the user explicitly changes the setting after reviewing the call plan.

## Approval sequence

1. Display the exact destination number and test message.
2. Confirm that the number is controlled and authorized.
3. Confirm that the user wants the call placed now.
4. Set `CALLE_ALLOW_LIVE_CALLS=1` only for the approved test session.
5. Create an approval object with `approved=True` and a non-empty `approved_by` value.
6. Execute only the controlled test call.
7. Immediately disable live calls again.
8. Record the call identifier, status, transcript availability, and any errors without storing secrets.

No live call is performed by the repository milestone itself.
