from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict

from .models import HotelCallPreview


CALL_E_TOOL_NAME = "plan_call"


def build_calle_plan_payload(preview: HotelCallPreview) -> Dict[str, Any]:
    """Build a provider-neutral payload for CALL-E planning.

    This function prepares data only. It does not invoke a live call.
    The exact provider tool invocation is intentionally kept at the adapter
    boundary so SDK/MCP schema changes do not affect the domain workflow.
    """
    return {
        "tool": CALL_E_TOOL_NAME,
        "mode": "plan_only",
        "recipient": {
            "name": preview.hotel_name,
            "phone_number": preview.phone_number,
        },
        "purpose": preview.purpose,
        "questions": list(preview.questions),
        "expected_information": list(preview.expected_information),
        "constraints": [
            "Do not make a reservation.",
            "Do not collect payment information.",
            "Do not claim availability without hotel confirmation.",
            "Escalate ambiguous pricing or policy answers.",
        ],
        "approval_required": preview.approval_required,
        "live_call_enabled": preview.live_call_enabled,
    }


def serialize_calle_plan(preview: HotelCallPreview) -> Dict[str, Any]:
    """Return a JSON-serializable preview for logs or UI rendering."""
    return build_calle_plan_payload(preview)
