from __future__ import annotations

from typing import Dict, List

from .models import HotelCallResult, RankedHotel


DEFAULT_RANKING_WEIGHTS: Dict[str, float] = {
    "value": 0.40,
    "availability": 0.30,
    "rating": 0.20,
    "facilities": 0.10,
}


def normalize_price_score(price: float | None, lowest_price: float | None) -> float:
    if price is None or lowest_price is None or price <= 0 or lowest_price <= 0:
        return 0.0
    return round(min((lowest_price / price) * 100, 100.0), 2)


def availability_score(status: str | None) -> float:
    if not status:
        return 0.0
    normalized = status.lower()
    if "available" in normalized or "confirmed" in normalized:
        return 100.0
    if "limited" in normalized or "wait" in normalized:
        return 50.0
    if "unavailable" in normalized or "not available" in normalized:
        return 0.0
    return 25.0


def rating_score(rating: float | None) -> float:
    if rating is None:
        return 0.0
    return round(max(0.0, min(rating / 5.0 * 100.0, 100.0)), 2)


def facilities_score(result: HotelCallResult, required_facilities: List[str]) -> float:
    if not required_facilities:
        return 100.0
    confirmed = {item.strip().lower() for item in result.requested_facilities}
    requested = {item.strip().lower() for item in required_facilities}
    return round(len(confirmed.intersection(requested)) / len(requested) * 100, 2)


def rank_hotels(
    results: List[HotelCallResult],
    required_facilities: List[str] | None = None,
    weights: Dict[str, float] | None = None,
) -> List[RankedHotel]:
    required_facilities = required_facilities or []
    weights = weights or DEFAULT_RANKING_WEIGHTS
    prices = [r.price_per_night for r in results if r.price_per_night and r.price_per_night > 0]
    lowest_price = min(prices) if prices else None
    ranked: List[RankedHotel] = []

    for result in results:
        value = normalize_price_score(result.price_per_night, lowest_price)
        availability = availability_score(result.availability)
        rating = rating_score(result.public_rating)
        facilities = facilities_score(result, required_facilities)
        total = (
            value * weights["value"]
            + availability * weights["availability"]
            + rating * weights["rating"]
            + facilities * weights["facilities"]
        )
        ranked.append(RankedHotel(
            hotel_name=result.hotel_name,
            total_score=round(total, 2),
            value_score=value,
            availability_score=availability,
            rating_score=rating,
            facilities_score=facilities,
            explanation=(
                f"Value={value:.2f}, availability={availability:.2f}, "
                f"rating={rating:.2f}, facilities={facilities:.2f}. "
                f"Weighted score={total:.2f}."
            ),
        ))

    return sorted(ranked, key=lambda item: item.total_score, reverse=True)
