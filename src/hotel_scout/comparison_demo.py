"""CALL-E-010 comparison pipeline demonstration."""

from __future__ import annotations

from .comparison import compare_hotel_results
from .models import HotelCallResult, HotelSearchRequest
from .report import render_hotel_comparison


def build_demo_request() -> HotelSearchRequest:
    return HotelSearchRequest(
        location="Chennai",
        check_in="2026-09-20",
        check_out="2026-09-22",
        guests=2,
        rooms=1,
        budget_per_night=5000,
        currency="INR",
        required_facilities=["Wi-Fi", "Breakfast", "Parking"],
        preferences=["quiet room", "near city centre"],
    )


def build_demo_results() -> list[HotelCallResult]:
    return [
        HotelCallResult(
            hotel_name="Hotel A",
            availability="Available",
            room_type="Deluxe Room",
            price_per_night=4200,
            total_price=8400,
            currency="INR",
            taxes_included=True,
            breakfast_included=True,
            breakfast_cost=0,
            requested_facilities=["Wi-Fi", "Breakfast", "Parking"],
            cancellation_policy="Free cancellation until 24 hours before check-in",
            additional_charges="None confirmed",
            public_rating=4.2,
            review_count=850,
            evidence=["Illustrative normalized result"],
            status="completed",
        ),
        HotelCallResult(
            hotel_name="Hotel B",
            availability="Limited availability",
            room_type="Executive Room",
            price_per_night=3800,
            total_price=7600,
            currency="INR",
            taxes_included=False,
            breakfast_included=False,
            breakfast_cost=450,
            requested_facilities=["Wi-Fi", "Parking"],
            cancellation_policy="Cancellation fee may apply",
            additional_charges="Taxes not included",
            public_rating=4.5,
            review_count=1200,
            evidence=["Illustrative normalized result"],
            status="completed",
        ),
        HotelCallResult(
            hotel_name="Hotel C",
            availability="Available",
            room_type="Superior Room",
            price_per_night=4700,
            total_price=9400,
            currency="INR",
            taxes_included=True,
            breakfast_included=True,
            breakfast_cost=0,
            requested_facilities=["Wi-Fi", "Breakfast"],
            cancellation_policy="Free cancellation until 48 hours before check-in",
            additional_charges="Parking charge may apply",
            public_rating=4.0,
            review_count=640,
            evidence=["Illustrative normalized result"],
            status="completed",
        ),
    ]


def main() -> None:
    request = build_demo_request()
    results = build_demo_results()

    comparison = compare_hotel_results(request, results)

    print(render_hotel_comparison(comparison))


if __name__ == "__main__":
    main()