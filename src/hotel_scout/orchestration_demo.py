"""CALL-E-011 orchestration demonstration."""

from __future__ import annotations

from .approval import CallApproval
from .models import HotelCandidate, HotelSearchRequest
from .orchestrator import (
    build_orchestration_plan,
    execute_orchestration,
    render_call_preview,
)


def main() -> None:
    request = HotelSearchRequest(
        location="Chennai",
        check_in="2026-09-20",
        check_out="2026-09-22",
        guests=2,
        rooms=1,
        budget_per_night=5000,
        currency="INR",
        required_facilities=["Wi-Fi", "Breakfast", "Parking"],
    )

    candidates = [
        HotelCandidate(name="Hotel A", location="Chennai", phone_number="+910000000001"),
        HotelCandidate(name="Hotel B", location="Chennai", phone_number="+910000000002"),
        HotelCandidate(name="Hotel C", location="Chennai", phone_number="+910000000003"),
    ]

    plan = build_orchestration_plan(request, candidates)
    print(render_call_preview(plan))
    print()
    print("DRY-RUN EXECUTION")
    print("=" * 48)

    result = execute_orchestration(
        plan,
        approval=CallApproval(
            approved=True,
            approved_by="local-demo-user",
            approval_note="Approved for dry-run demonstration only.",
        ),
        live_call=False,
    )
    print(result.report)


if __name__ == "__main__":
    main()
