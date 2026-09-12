from __future__ import annotations

import json

from .calle_integration import build_calle_plan_payload
from .models import HotelCallPreview


def main() -> None:
    preview = HotelCallPreview(
        hotel_name="Example Chennai Hotel",
        phone_number="+91XXXXXXXXXX",
        purpose=(
            "Verify live accommodation availability and pricing for "
            "the requested dates. Do not make a reservation or collect payment."
        ),
        questions=[
            "Do you have availability for the requested dates and number of guests?",
            "What is the total price including taxes and mandatory fees?",
            "Is breakfast included?",
            "What is the cancellation policy?",
        ],
        expected_information=[
            "Availability",
            "Room category",
            "Total price",
            "Breakfast",
            "Cancellation policy",
        ],
    )

    payload = build_calle_plan_payload(preview)
    print("CALL-E-005 — CALL PLAN PREVIEW")
    print(json.dumps(payload, indent=2))
    print("\nNo live call was placed.")


if __name__ == "__main__":
    main()
