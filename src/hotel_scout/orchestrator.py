"""CALL-E-011 end-to-end hotel call orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping, Sequence

from .approval import CallApproval, require_explicit_approval
from .calle_execution import (
    HotelCallExecutionRequest,
    execute_hotel_call,
)
from .comparison import HotelComparison, compare_hotel_results
from .models import HotelCallPreview, HotelCallResult, HotelCandidate, HotelSearchRequest
from .questionnaire import build_hotel_call_preview
from .report import render_hotel_comparison
from .result_normalizer import normalize_hotel_call_result


@dataclass(frozen=True)
class HotelOrchestrationPlan:
    """Validated candidates and previews prepared before execution."""

    request: HotelSearchRequest
    candidates: list[HotelCandidate]
    previews: list[HotelCallPreview]

    @property
    def candidate_names(self) -> list[str]:
        return [candidate.name for candidate in self.candidates]


@dataclass(frozen=True)
class HotelOrchestrationResult:
    """Result of executing and comparing the hotel call plan."""

    plan: HotelOrchestrationPlan
    approval: CallApproval
    results: list[HotelCallResult]
    comparison: HotelComparison
    report: str
    executed_calls: int

    @property
    def recommended_hotel(self) -> str | None:
        return self.comparison.recommended_hotel


def _validate_candidates(candidates: Sequence[HotelCandidate]) -> None:
    if not candidates:
        raise ValueError("At least one hotel candidate is required.")
    if len(candidates) > 3:
        raise ValueError("A maximum of three hotel candidates is supported.")

    names: set[str] = set()
    for candidate in candidates:
        if not candidate.name.strip():
            raise ValueError("Every hotel candidate must have a name.")
        if not candidate.phone_number or not candidate.phone_number.strip():
            raise ValueError(f"Phone number is required for {candidate.name}.")
        normalized = candidate.name.strip().casefold()
        if normalized in names:
            raise ValueError(f"Duplicate hotel candidate detected: {candidate.name}")
        names.add(normalized)


def build_orchestration_plan(
    request: HotelSearchRequest,
    candidates: Sequence[HotelCandidate],
) -> HotelOrchestrationPlan:
    """Validate input and prepare one CALL-E preview per candidate."""
    errors = request.validate()
    if errors:
        raise ValueError("Invalid hotel search request:\n- " + "\n- ".join(errors))

    _validate_candidates(candidates)
    candidate_list = list(candidates)
    previews = [
        build_hotel_call_preview(request, candidate)
        for candidate in candidate_list
    ]

    return HotelOrchestrationPlan(
        request=request,
        candidates=candidate_list,
        previews=previews,
    )


def render_call_preview(plan: HotelOrchestrationPlan) -> str:
    """Render all proposed calls without contacting any hotel."""
    lines = [
        "CALL-E HOTEL SCOUT — CALL PREVIEW",
        "=" * 48,
        "",
        "No live call has been made.",
        "Explicit approval is required before execution.",
        "",
        f"Location: {plan.request.location}",
        f"Dates: {plan.request.check_in} to {plan.request.check_out}",
        f"Guests: {plan.request.guests}",
        f"Rooms: {plan.request.rooms}",
        "",
        "PROPOSED CALLS",
        "-" * 48,
    ]

    for index, preview in enumerate(plan.previews, start=1):
        lines.extend([
            f"{index}. {preview.hotel_name}",
            f"   Phone: {preview.phone_number or 'Not available'}",
            f"   Purpose: {preview.purpose}",
            "   Questions:",
        ])
        lines.extend(f"   - {question}" for question in preview.questions)
        lines.append("   Safety: No reservation, payment, OTP, password, or sensitive data collection.")
        lines.append("")

    lines.extend([
        "APPROVAL REQUIRED",
        "-" * 48,
        "Approve only after checking the listed hotels, phone numbers, questions, and safety limits.",
    ])
    return "\n".join(lines)


def _dry_run_raw_result(preview: HotelCallPreview) -> dict[str, Any]:
    return {
        "status": "dry_run",
        "availability": None,
        "evidence": ["Dry-run only; no hotel was contacted."],
    }


def execute_orchestration(
    plan: HotelOrchestrationPlan,
    *,
    approval: CallApproval,
    runtime: Any | None = None,
    live_call: bool = False,
    raw_result_provider: Callable[[HotelCallPreview], Mapping[str, Any]] | None = None,
) -> HotelOrchestrationResult:
    """Execute the approved plan, normalize responses, and rank hotels.

    Dry-run is the default. A live execution requires a configured runtime and
    explicit approval. ``raw_result_provider`` is useful for deterministic tests
    and demonstrations that simulate structured CALL-E responses.
    """
    if live_call:
        require_explicit_approval(approval)
        if runtime is None:
            raise ValueError("A CALL-E runtime is required for live execution.")

    normalized_results: list[HotelCallResult] = []

    for preview in plan.previews:
        if raw_result_provider is not None:
            raw = raw_result_provider(preview)
        elif live_call:
            response = execute_hotel_call(
                runtime,
                HotelCallExecutionRequest(
                    preview=preview,
                    live_call=True,
                    approval=approval,
                ),
            )
            raw = {
                "status": "completed" if response.succeeded else "failed",
                "evidence": ["CALL-E execution response received."],
            }
        else:
            raw = _dry_run_raw_result(preview)

        normalized_results.append(
            normalize_hotel_call_result(
                preview.hotel_name,
                raw,
                evidence=list(raw.get("evidence", [])),
            )
        )

    comparison = compare_hotel_results(plan.request, normalized_results)
    report = render_hotel_comparison(comparison)

    return HotelOrchestrationResult(
        plan=plan,
        approval=approval,
        results=normalized_results,
        comparison=comparison,
        report=report,
        executed_calls=len(normalized_results),
    )
