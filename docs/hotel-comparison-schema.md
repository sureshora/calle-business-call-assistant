# Hotel Comparison Schema

## Search request

```json
{
  "location": "Near Arunachaleswarar Temple, Tiruvannamalai",
  "check_in": "2026-09-13",
  "check_out": "2026-09-15",
  "guests": 2,
  "rooms": 1,
  "budget_per_night": 5000,
  "preferences": ["parking", "breakfast", "air conditioning"],
  "candidate_count": 3
}
```

## Hotel candidate

```json
{
  "hotel_id": "hotel-001",
  "name": "Example Hotel",
  "phone_number": "+911234567890",
  "address": "Tiruvannamalai",
  "distance_from_location": "1.2 km",
  "public_rating": 4.3,
  "review_count": 1250,
  "rating_source": "Google Maps",
  "rating_checked_at": "2026-09-12T09:00:00+05:30"
}
```

## Call result

```json
{
  "hotel_id": "hotel-001",
  "call_status": "confirmed",
  "availability": "available",
  "room_type": "Deluxe AC",
  "currency": "INR",
  "price_per_night": 3800,
  "total_price": 7600,
  "taxes_included": true,
  "breakfast": "included",
  "facilities": {
    "parking": "confirmed",
    "air_conditioning": "confirmed",
    "wifi": "unknown"
  },
  "cancellation_policy": "Free cancellation until 24 hours before check-in",
  "evidence": [],
  "confidence": "high"
}
```

## Ranking principles

1. Exclude unavailable hotels from the primary ranking.
2. Normalize prices to the same stay duration and tax basis.
3. Apply user preferences before generic scoring.
4. Penalize unknown information rather than treating it as confirmed.
5. Explain the score in plain language.
6. Recommend one hotel only when the evidence is sufficient; otherwise state that no reliable winner can be selected.

Suggested default weights:

- 40% price/value
- 30% availability and requirement match
- 20% public rating
- 10% facilities and policies

These weights are defaults and should be adjustable.