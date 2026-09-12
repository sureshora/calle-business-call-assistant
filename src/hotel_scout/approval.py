from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CallApproval:
    approved: bool = False
    approved_by: str | None = None
    approval_note: str | None = None


def require_explicit_approval(approval: CallApproval) -> None:
    """Raise unless a human explicitly approved the live call."""
    if not approval.approved:
        raise PermissionError(
            "Live CALL-E execution requires explicit human approval."
        )

    if not approval.approved_by or not approval.approved_by.strip():
        raise PermissionError(
            "Approval must identify the approving user."
        )


def live_execution_allowed(approval: CallApproval) -> bool:
    """Return whether the approval object passes the safety gate."""
    try:
        require_explicit_approval(approval)
    except PermissionError:
        return False
    return True
