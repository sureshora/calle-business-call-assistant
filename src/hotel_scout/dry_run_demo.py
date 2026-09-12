from __future__ import annotations

import json

from .calle_execution import (
    HotelCallExecutionRequest,
    execute_hotel_call,
)
from .calle_runtime import CalleRuntime
from .models import HotelCallPreview


def main() -> None:
    preview = HotelCallPreview(
        hotel_name="Example Chennai Hotel",
        phone_number="+919999999999",
        purpose=(
            "Verify accommodation availability and pricing. "
            "Do not make a reservation."
        ),
        questions=[
            "Do you have availability for the requested dates?",
            "What is the total price including taxes?",
            "Is breakfast included?",
            "What is the cancellation policy?",
        ],
        expected_information=[
            "Availability",
            "Total price",
            "Breakfast",
            "Cancellation policy",
        ],
    )

    runtime = CalleRuntime()

    response = execute_hotel_call(
        runtime,
        HotelCallExecutionRequest(
            preview=preview,
            live_call=False,
        ),
    )

    print("Mode:", response.mode)
    print("Hotel:", response.hotel_name)
    print("Phone:", response.phone_number)
    print("CALL-E payload:")
    print(json.dumps(response.plan_payload, indent=2))


if __name__ == "__main__":
    main()