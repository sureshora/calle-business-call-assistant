"""Tests for CALL-E-011 hotel call orchestration."""

from __future__ import annotations

import unittest

from hotel_scout.approval import CallApproval
from hotel_scout.models import HotelCandidate, HotelSearchRequest
from hotel_scout.orchestrator import (
    build_orchestration_plan,
    execute_orchestration,
    render_call_preview,
)


class OrchestrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.request = HotelSearchRequest(
            location="Chennai",
            check_in="2026-09-20",
            check_out="2026-09-22",
            guests=2,
            rooms=1,
            budget_per_night=5000,
            currency="INR",
            required_facilities=["Wi-Fi", "Breakfast"],
        )
        self.candidates = [
            HotelCandidate(name="Hotel A", location="Chennai", phone_number="+910000000001"),
            HotelCandidate(name="Hotel B", location="Chennai", phone_number="+910000000002"),
        ]

    def test_plan_contains_one_preview_per_candidate(self) -> None:
        plan = build_orchestration_plan(self.request, self.candidates)
        self.assertEqual(len(plan.previews), 2)
        self.assertEqual(plan.previews[0].hotel_name, "Hotel A")
        self.assertGreater(len(plan.previews[0].questions), 0)

    def test_preview_requires_explicit_approval(self) -> None:
        plan = build_orchestration_plan(self.request, self.candidates)
        preview = render_call_preview(plan)
        self.assertIn("No live call has been made.", preview)
        self.assertIn("Explicit approval is required", preview)
        self.assertIn("Hotel A", preview)
        self.assertIn("Hotel B", preview)

    def test_more_than_three_candidates_are_rejected(self) -> None:
        candidates = self.candidates + [
            HotelCandidate(name="Hotel C", location="Chennai", phone_number="+910000000003"),
            HotelCandidate(name="Hotel D", location="Chennai", phone_number="+910000000004"),
        ]
        with self.assertRaises(ValueError):
            build_orchestration_plan(self.request, candidates)

    def test_duplicate_candidates_are_rejected(self) -> None:
        candidates = [
            HotelCandidate(name="Hotel A", location="Chennai", phone_number="+910000000001"),
            HotelCandidate(name="hotel a", location="Chennai", phone_number="+910000000002"),
        ]
        with self.assertRaises(ValueError):
            build_orchestration_plan(self.request, candidates)

    def test_missing_phone_number_is_rejected(self) -> None:
        candidates = [HotelCandidate(name="Hotel A", location="Chennai")]
        with self.assertRaises(ValueError):
            build_orchestration_plan(self.request, candidates)

    def test_dry_run_executes_without_live_call(self) -> None:
        plan = build_orchestration_plan(self.request, self.candidates)
        result = execute_orchestration(
            plan,
            approval=CallApproval(
                approved=True,
                approved_by="test-user",
                approval_note="Dry-run test",
            ),
            live_call=False,
        )
        self.assertEqual(result.executed_calls, 2)
        self.assertIsNotNone(result.comparison)
        self.assertIsNotNone(result.report)
        self.assertIn("RECOMMENDATION", result.report)

    def test_unapproved_live_execution_is_rejected(self) -> None:
        plan = build_orchestration_plan(self.request, self.candidates)
        with self.assertRaises(PermissionError):
            execute_orchestration(
                plan,
                approval=CallApproval(
                    approved=False,
                    approved_by="test-user",
                    approval_note="Not approved",
                ),
                live_call=True,
                runtime=object(),
            )


if __name__ == "__main__":
    unittest.main()
