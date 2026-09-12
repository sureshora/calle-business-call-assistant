from __future__ import annotations

from typing import List

from .models import HotelCandidate, HotelCallPreview, HotelScoutPlan, HotelSearchRequest
from .questionnaire import build_hotel_call_preview
from .ranking import DEFAULT_RANKING_WEIGHTS


def create_hotel_scout_plan(request: HotelSearchRequest, candidates: List[HotelCandidate]) -> HotelScoutPlan:
    errors = request.validate()
    if errors:
        raise ValueError("Invalid hotel search request:\n- " + "\n- ".join(errors))
    if not candidates:
        raise ValueError("At least one hotel candidate is required.")
    if len(candidates) > 3:
        raise ValueError("The dry-run workflow supports a maximum of three hotel candidates at this stage.")

    previews = [build_hotel_call_preview(request, candidate) for candidate in candidates]
    return HotelScoutPlan(
        request=request,
        candidates=candidates,
        call_previews=previews,
        ranking_weights=dict(DEFAULT_RANKING_WEIGHTS),
        live_calls_allowed=False,
    )


def render_plan(plan: HotelScoutPlan) -> str:
    request = plan.request
    lines = [
        "CALL-E HOTEL SCOUT — DRY-RUN PLAN",
        "=" * 42,
        "",
        "SEARCH REQUEST",
        f"Location: {request.location}",
        f"Check-in: {request.check_in}",
        f"Check-out: {request.check_out}",
        f"Guests: {request.guests}",
        f"Rooms: {request.rooms}",
        f"Budget/night: {request.budget_per_night or 'Not specified'} {request.currency}",
        f"Required facilities: {', '.join(request.required_facilities) or 'None'}",
        f"Preferences: {', '.join(request.preferences) or 'None'}",
        "",
        "CANDIDATE HOTELS",
    ]

    for index, candidate in enumerate(plan.candidates, start=1):
        lines.extend([
            f"{index}. {candidate.name}",
            f"   Location: {candidate.location}",
            f"   Phone: {candidate.phone_number or 'Not available'}",
            f"   Website: {candidate.website or 'Not available'}",
            f"   Public rating: {candidate.public_rating or 'Not available'}",
            "",
        ])

    lines.extend(["CALL PREVIEWS", "-" * 42])
    for index, preview in enumerate(plan.call_previews, start=1):
        lines.extend([
            f"{index}. {preview.hotel_name}",
            f"   Purpose: {preview.purpose}",
            f"   Approval required: {preview.approval_required}",
            f"   Live call enabled: {preview.live_call_enabled}",
            "   Questions:",
        ])
        for question_number, question in enumerate(preview.questions, start=1):
            lines.append(f"      {question_number}. {question}")
        lines.append("")

    lines.extend([
        "RANKING WEIGHTS",
        f"Value: {plan.ranking_weights['value']:.0%}",
        f"Availability: {plan.ranking_weights['availability']:.0%}",
        f"Public rating: {plan.ranking_weights['rating']:.0%}",
        f"Facilities: {plan.ranking_weights['facilities']:.0%}",
        "",
        "SAFETY STATUS",
        f"Live calls allowed: {plan.live_calls_allowed}",
        "No call will be placed in this dry-run.",
        "No booking or payment action is supported.",
    ])
    return "\n".join(lines)
