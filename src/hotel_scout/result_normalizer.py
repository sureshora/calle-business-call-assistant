"""CALL-E-009 normalization of hotel call responses."""

from __future__ import annotations

import re
from typing import Any, Mapping

from .models import HotelCallResult


def _text(value: Any) -> str:
    """Convert a value to trimmed text."""
    return "" if value is None else str(value).strip()


def _optional_bool(value: Any) -> bool | None:
    """Normalize common yes/no-style values."""

    if isinstance(value, bool):
        return value

    text = _text(value).lower()

    if text in {
        "yes",
        "true",
        "included",
        "available",
        "confirmed",
    }:
        return True

    if text in {
        "no",
        "false",
        "not included",
        "unavailable",
        "none",
        "not confirmed",
    }:
        return False

    return None


def _optional_float(value: Any) -> float | None:
    """Extract a numeric value without inventing missing data."""

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)

    text = _text(value).replace(",", "")
    match = re.search(r"\d+(?:\.\d+)?", text)

    return float(match.group()) if match else None


def _optional_int(value: Any) -> int | None:
    """Normalize an integer value such as a review count."""

    if isinstance(value, bool):
        return None

    if isinstance(value, int):
        return value

    text = _text(value).replace(",", "")

    if text.isdigit():
        return int(text)

    return None


def _facility_list(value: Any) -> list[str]:
    """Normalize facilities supplied as text or a list."""

    if value is None:
        return []

    if isinstance(value, str):
        return [
            item.strip()
            for item in value.split(",")
            if item.strip()
        ]

    if isinstance(value, (list, tuple, set)):
        return [
            str(item).strip()
            for item in value
            if str(item).strip()
        ]

    return [str(value).strip()]


def _evidence_list(value: Any) -> list[str]:
    """Normalize evidence entries."""

    if value is None:
        return []

    if isinstance(value, str):
        return [value.strip()] if value.strip() else []

    if isinstance(value, (list, tuple, set)):
        return [
            str(item).strip()
            for item in value
            if str(item).strip()
        ]

    return [str(value).strip()]


def normalize_hotel_call_result(
    hotel_name: str,
    raw: Mapping[str, Any],
    *,
    evidence: list[str] | None = None,
) -> HotelCallResult:
    """Normalize a structured or partially structured CALL-E response.

    Missing or ambiguous values remain None. The function does not invent
    availability, prices, ratings, policies, or facilities.
    """

    status = (
        _text(raw.get("status") or raw.get("call_status"))
        or "completed"
    )

    availability = _text(raw.get("availability")) or None

    room_type = (
        _text(raw.get("room_type") or raw.get("room_category"))
        or None
    )

    currency = _text(raw.get("currency")) or "INR"

    cancellation_policy = (
        _text(
            raw.get("cancellation_policy")
            or raw.get("cancellation")
        )
        or None
    )

    additional_charges = (
        _text(
            raw.get("additional_charges")
            or raw.get("extra_charges")
        )
        or None
    )

    facilities = _facility_list(
        raw.get("requested_facilities")
        or raw.get("facilities")
    )

    normalized_evidence = (
        list(evidence)
        if evidence is not None
        else _evidence_list(raw.get("evidence"))
    )

    return HotelCallResult(
        hotel_name=hotel_name,
        availability=availability,
        room_type=room_type,
        price_per_night=_optional_float(
            raw.get("price_per_night")
            or raw.get("nightly_price")
        ),
        total_price=_optional_float(raw.get("total_price")),
        currency=currency,
        taxes_included=_optional_bool(raw.get("taxes_included")),
        breakfast_included=_optional_bool(
            raw.get("breakfast_included")
        ),
        breakfast_cost=_optional_float(raw.get("breakfast_cost")),
        requested_facilities=facilities,
        cancellation_policy=cancellation_policy,
        additional_charges=additional_charges,
        public_rating=_optional_float(
            raw.get("public_rating") or raw.get("rating")
        ),
        review_count=_optional_int(raw.get("review_count")),
        evidence=normalized_evidence,
        status=status,
    )