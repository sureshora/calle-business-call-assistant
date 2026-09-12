"""CALL-E-008 hotel call execution adapter.

This module provides a safe boundary around CalleRuntime.
Dry-run mode is the default. Live calls require:
1. Runtime configuration allowing live calls.
2. A valid international phone number.
3. Explicit human approval.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .approval import CallApproval
from .calle_integration import build_calle_plan_payload
from .calle_runtime import CalleCommandResult, CalleRuntime
from .models import HotelCallPreview


@dataclass(frozen=True)
class HotelCallExecutionRequest:
    """Input required to execute or preview one hotel call."""

    preview: HotelCallPreview
    live_call: bool = False
    approval: Optional[CallApproval] = None


@dataclass(frozen=True)
class HotelCallExecutionResponse:
    """Result returned by the execution adapter."""

    mode: str
    hotel_name: str
    phone_number: Optional[str]
    command_result: Optional[CalleCommandResult]
    plan_payload: dict

    @property
    def succeeded(self) -> bool:
        """Return True only when a CALL-E command succeeded."""
        return (
            self.command_result is not None
            and self.command_result.succeeded
        )


def build_hotel_call_goal(preview: HotelCallPreview) -> str:
    """Convert the approved questionnaire into a CALL-E call goal."""

    questions = " ".join(
        f"Question {index}: {question}"
        for index, question in enumerate(preview.questions, start=1)
    )

    safety_constraints = (
        "Do not make a reservation. "
        "Do not collect payment information. "
        "Do not request OTPs, passwords, or sensitive personal data. "
        "Do not claim availability unless the hotel confirms it. "
        "Clearly identify uncertain or ambiguous answers."
    )

    return f"{preview.purpose} {questions} {safety_constraints}".strip()


def execute_hotel_call(
    runtime: CalleRuntime,
    request: HotelCallExecutionRequest,
) -> HotelCallExecutionResponse:
    """Preview or execute a hotel call through the CALL-E runtime.

    The default behavior is dry-run and does not contact anyone.
    """

    preview = request.preview
    payload = build_calle_plan_payload(preview)

    if not request.live_call:
        return HotelCallExecutionResponse(
            mode="dry_run",
            hotel_name=preview.hotel_name,
            phone_number=preview.phone_number,
            command_result=None,
            plan_payload=payload,
        )

    if not preview.phone_number:
        raise ValueError(
            "A phone number is required for a live hotel call."
        )

    if not preview.phone_number.startswith("+"):
        raise ValueError(
            "Use an international-format phone number beginning with '+'."
        )

    if request.approval is None:
        raise PermissionError(
            "Explicit approval is required for live hotel calls."
        )

    result = runtime.execute(
        (
            "call",
            "run",
            "--to-phone",
            preview.phone_number,
            "--goal",
            build_hotel_call_goal(preview),
        ),
        live_call=True,
        approval=request.approval,
    )

    return HotelCallExecutionResponse(
        mode="live",
        hotel_name=preview.hotel_name,
        phone_number=preview.phone_number,
        command_result=result,
        plan_payload=payload,
    )