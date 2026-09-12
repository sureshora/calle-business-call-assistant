"""CALL-E-007 controlled-call preparation and safety checks."""

from __future__ import annotations

import os
from dataclasses import dataclass

from .approval import CallApproval
from .calle_runtime import CalleRuntime


@dataclass(frozen=True)
class ControlledTestCall:
    phone_number: str
    test_phrase: str
    authorized_by: str

    @classmethod
    def from_environment(cls) -> "ControlledTestCall":
        phone_number = os.getenv("CALLE_TEST_PHONE_NUMBER", "").strip()
        authorized_by = os.getenv("CALLE_TEST_AUTHORIZED_BY", "").strip()
        if not phone_number:
            raise ValueError("CALLE_TEST_PHONE_NUMBER is required.")
        if not authorized_by:
            raise ValueError("CALLE_TEST_AUTHORIZED_BY is required.")
        return cls(
            phone_number=phone_number,
            test_phrase=(
                "This is a controlled CALL-E test for Hotel Scout. "
                "Please confirm that you can hear this message, then end the call."
            ),
            authorized_by=authorized_by,
        )


def build_controlled_test_approval(test_call: ControlledTestCall) -> CallApproval:
    return CallApproval(
        approved=False,
        approved_by=test_call.authorized_by,
        approval_note="Approval must be set to true only immediately before the test call.",
    )


def validate_controlled_test_call(
    runtime: CalleRuntime,
    test_call: ControlledTestCall,
    approval: CallApproval,
) -> None:
    if not test_call.phone_number.startswith("+"):
        raise ValueError("Use an international-format test number beginning with '+'.")
    runtime.assert_live_call_permitted(approval)
