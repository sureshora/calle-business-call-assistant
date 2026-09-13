"""CALL-E-010 human-readable comparison report."""

from __future__ import annotations

from .comparison import HotelComparison
from .models import HotelCallResult


def _display(value: object) -> str:
    if value is None or value == "":
        return "Not available"
    return str(value)


def _money(value: float | None, currency: str) -> str:
    if value is None:
        return "Not available"
    return f"{value:,.2f} {currency}"


def _bool_display(value: bool | None) -> str:
    if value is True:
        return "Yes"
    if value is False:
        return "No"
    return "Not confirmed"


def render_hotel_comparison(
    comparison: HotelComparison,
) -> str:
    """Render a recommendation-ready hotel comparison report."""

    request = comparison.request
    lines: list[str] = [
        "CALL-E HOTEL SCOUT — COMPARISON REPORT",
        "=" * 48,
        "",
        "SEARCH REQUEST",
        f"Location: {request.location}",
        f"Check-in: {request.check_in}",
        f"Check-out: {request.check_out}",
        f"Guests: {request.guests}",
        f"Rooms: {request.rooms}",
        (
            f"Budget/night: {_money(request.budget_per_night, request.currency)}"
            if request.budget_per_night is not None
            else "Budget/night: Not specified"
        ),
        "",
        "HOTEL RESULTS",
        "-" * 48,
    ]

    for index, result in enumerate(comparison.results, start=1):
        lines.extend(
            [
                f"{index}. {result.hotel_name}",
                f"   Status: {_display(result.status)}",
                f"   Availability: {_display(result.availability)}",
                f"   Room type: {_display(result.room_type)}",
                (
                    "   Price/night: "
                    f"{_money(result.price_per_night, result.currency)}"
                ),
                (
                    "   Total price: "
                    f"{_money(result.total_price, result.currency)}"
                ),
                f"   Taxes included: {_bool_display(result.taxes_included)}",
                (
                    "   Breakfast included: "
                    f"{_bool_display(result.breakfast_included)}"
                ),
                (
                    "   Breakfast cost: "
                    f"{_money(result.breakfast_cost, result.currency)}"
                ),
                (
                    "   Facilities: "
                    f"{', '.join(result.requested_facilities) or 'Not confirmed'}"
                ),
                (
                    "   Cancellation policy: "
                    f"{_display(result.cancellation_policy)}"
                ),
                (
                    "   Additional charges: "
                    f"{_display(result.additional_charges)}"
                ),
                f"   Public rating: {_display(result.public_rating)}",
                f"   Review count: {_display(result.review_count)}",
                "",
            ]
        )

    lines.extend(
        [
            "RANKING",
            "-" * 48,
        ]
    )

    for index, ranking in enumerate(comparison.rankings, start=1):
        lines.extend(
            [
                f"{index}. {ranking.hotel_name}",
                f"   Total score: {ranking.total_score:.2f}/100",
                f"   {ranking.explanation}",
                "",
            ]
        )

    lines.extend(
        [
            "RECOMMENDATION",
            "-" * 48,
            (
                f"Recommended hotel: {comparison.recommended_hotel}"
                if comparison.recommended_hotel
                else "Recommended hotel: Not available"
            ),
            "",
            "RANKING WEIGHTS",
            f"Value: {comparison.ranking_weights['value']:.0%}",
            f"Availability: {comparison.ranking_weights['availability']:.0%}",
            f"Public rating: {comparison.ranking_weights['rating']:.0%}",
            f"Facilities: {comparison.ranking_weights['facilities']:.0%}",
            "",
            "SAFETY NOTES",
            "Only normalized results are included.",
            "Missing or ambiguous values are shown as not available.",
            "No booking or payment action is performed.",
        ]
    )

    return "\n".join(lines)


def render_compact_result(result: HotelCallResult) -> str:
    """Render one normalized result as a compact line."""

    return (
        f"{result.hotel_name}: "
        f"availability={_display(result.availability)}, "
        f"price/night={_money(result.price_per_night, result.currency)}, "
        f"rating={_display(result.public_rating)}, "
        f"status={_display(result.status)}"
    )