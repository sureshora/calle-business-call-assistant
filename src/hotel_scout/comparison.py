"""CALL-E-010 hotel result comparison pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from .models import HotelCallResult, HotelSearchRequest, RankedHotel
from .ranking import DEFAULT_RANKING_WEIGHTS, rank_hotels


@dataclass(frozen=True)
class HotelComparison:
    """Recommendation-ready comparison result."""

    request: HotelSearchRequest
    results: list[HotelCallResult]
    rankings: list[RankedHotel]
    ranking_weights: dict[str, float]

    @property
    def recommended_hotel(self) -> str | None:
        """Return the highest-ranked hotel, if any."""
        return self.rankings[0].hotel_name if self.rankings else None

    @property
    def complete_results(self) -> list[HotelCallResult]:
        """Return results that completed successfully."""
        return [
            result
            for result in self.results
            if result.status.lower() in {"completed", "success", "confirmed"}
        ]


def _validate_result_name(result: HotelCallResult) -> None:
    if not result.hotel_name.strip():
        raise ValueError("Every hotel result must contain a hotel name.")


def _validate_currency(
    request: HotelSearchRequest,
    results: Iterable[HotelCallResult],
) -> None:
    currencies = {
        result.currency.upper().strip()
        for result in results
        if result.currency and result.currency.strip()
    }

    if len(currencies) > 1:
        raise ValueError(
            "All hotel results must use the same currency before ranking."
        )

    if currencies and request.currency.upper() not in currencies:
        raise ValueError(
            "Hotel result currency does not match the search request currency."
        )


def compare_hotel_results(
    request: HotelSearchRequest,
    results: list[HotelCallResult],
    *,
    weights: Mapping[str, float] | None = None,
) -> HotelComparison:
    """Validate, rank, and package normalized hotel results."""

    errors = request.validate()
    if errors:
        raise ValueError(
            "Invalid hotel search request:\n- " + "\n- ".join(errors)
        )

    if not results:
        raise ValueError("At least one normalized hotel result is required.")

    if len(results) > 3:
        raise ValueError(
            "The comparison pipeline supports a maximum of three hotels."
        )

    names: set[str] = set()

    for result in results:
        _validate_result_name(result)

        normalized_name = result.hotel_name.strip().casefold()
        if normalized_name in names:
            raise ValueError(
                f"Duplicate hotel result detected: {result.hotel_name}"
            )

        names.add(normalized_name)

    _validate_currency(request, results)

    selected_weights = dict(weights or DEFAULT_RANKING_WEIGHTS)

    required_weight_keys = {
        "value",
        "availability",
        "rating",
        "facilities",
    }

    if set(selected_weights) != required_weight_keys:
        raise ValueError(
            "Ranking weights must contain exactly: "
            "value, availability, rating, facilities."
        )

    if any(weight < 0 for weight in selected_weights.values()):
        raise ValueError("Ranking weights cannot be negative.")

    if round(sum(selected_weights.values()), 6) != 1.0:
        raise ValueError("Ranking weights must sum to 1.0.")

    rankings = rank_hotels(
        results,
        required_facilities=request.required_facilities,
        weights=selected_weights,
    )

    return HotelComparison(
        request=request,
        results=list(results),
        rankings=rankings,
        ranking_weights=selected_weights,
    )