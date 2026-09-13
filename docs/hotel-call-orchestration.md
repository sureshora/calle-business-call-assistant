# CALL-E-011 — Hotel Call Orchestration

## Purpose

CALL-E-011 connects hotel search, questionnaire generation, approval, CALL-E execution, result normalization, comparison, and reporting into one controlled workflow.

## Workflow

1. Validate the hotel search request.
2. Validate one to three hotel candidates.
3. Build one standardized CALL-E preview per candidate.
4. Render the proposed calls without contacting hotels.
5. Obtain explicit human approval.
6. Execute approved calls through the existing CALL-E runtime boundary.
7. Normalize the returned information.
8. Compare and rank the normalized results.
9. Render the recommendation report.

## Safety boundary

The orchestration layer:

- Requires explicit approval before live execution.
- Supports no more than three hotel candidates.
- Defaults to dry-run mode.
- Does not book rooms.
- Does not process payments.
- Does not request OTPs, passwords, or sensitive personal data.
- Does not accept unconfirmed charges.
- Preserves missing or ambiguous values as unavailable.

## Run the demonstration

From the repository root:

```powershell
python -m src.hotel_scout.orchestration_demo
```

## Run tests

```powershell
python -m unittest discover -s src/hotel_scout/tests -p "test_*.py" -v
```

## Live execution

Live execution is intentionally not performed by the demonstration or tests. It requires:

- A configured CALL-E runtime.
- Valid international phone numbers.
- A complete preview reviewed by the user.
- Explicit approval identifying the approving user.

The workflow performs information gathering only. It does not make reservations or payments.
