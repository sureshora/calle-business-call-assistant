# Call Task Schema

The assistant uses a provider-neutral task contract so the workflow can be tested without placing a call and later mapped to CALL-E.

## Input

```json
{
  "business_name": "Example Hotel",
  "phone_number": "+911234567890",
  "purpose": "Find available rooms and rates",
  "requested_information": [
    "availability for 2 adults",
    "date and check-in time",
    "room type",
    "total rate and taxes"
  ],
  "constraints": [
    "Do not book",
    "Do not provide payment details",
    "Do not make commitments"
  ],
  "user_approved": false
}
```

## Preview output

```json
{
  "mode": "preview",
  "status": "awaiting_approval",
  "target": {
    "business_name": "Example Hotel",
    "phone_number": "+911234567890"
  },
  "purpose": "Find available rooms and rates",
  "questions": [
    "Are rooms available for 2 adults?",
    "What dates and check-in times are available?",
    "What room types and total rates are available?"
  ],
  "side_effects": [
    "An outbound phone call will be placed",
    "The recipient may hear an AI-generated voice",
    "The conversation may be recorded or transcribed by the provider"
  ],
  "requires_explicit_approval": true
}
```

## Result contract

```json
{
  "status": "confirmed | partial | unavailable | voicemail | refused | failed | ambiguous",
  "business_name": "Example Hotel",
  "facts": [
    {
      "field": "availability",
      "value": "Available",
      "evidence": "Transcript span supporting the value"
    }
  ],
  "follow_up_required": [],
  "confidence": "high | medium | low",
  "notes": []
}
```

A result is not considered confirmed unless the call evidence supports the exact field. Unknown values must remain unknown.