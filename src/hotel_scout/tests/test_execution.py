import unittest

from src.hotel_scout.approval import CallApproval
from src.hotel_scout.calle_execution import (
    HotelCallExecutionRequest,
    build_hotel_call_goal,
    execute_hotel_call,
)
from src.hotel_scout.calle_runtime import (
    CalleCommandResult,
    CalleRuntime,
)
from src.hotel_scout.models import HotelCallPreview
from src.hotel_scout.runtime_config import CalleRuntimeConfig


class FakeExecutor:
    def __init__(self) -> None:
        self.commands = []

    def __call__(self, command, timeout_seconds):
        self.commands.append((tuple(command), timeout_seconds))
        return CalleCommandResult(
            command=tuple(command),
            returncode=0,
            stdout="CALL-E test result",
            stderr="",
        )


def make_preview() -> HotelCallPreview:
    return HotelCallPreview(
        hotel_name="Test Hotel",
        phone_number="+919999999999",
        purpose="Verify availability and pricing. Do not make a reservation.",
        questions=[
            "Do you have availability?",
            "What is the total price including taxes?",
        ],
        expected_information=[
            "Availability",
            "Total price",
        ],
    )


class HotelCallExecutionTests(unittest.TestCase):
    def test_goal_contains_questions_and_safety_constraints(self):
        goal = build_hotel_call_goal(make_preview())

        self.assertIn("Do you have availability?", goal)
        self.assertIn("Do not make a reservation.", goal)
        self.assertIn("Do not request OTPs", goal)

    def test_default_mode_is_dry_run(self):
        executor = FakeExecutor()
        runtime = CalleRuntime(
            config=CalleRuntimeConfig(
                executable="calle",
                timeout_seconds=30,
                allow_live_calls=False,
            ),
            executor=executor,
        )

        response = execute_hotel_call(
            runtime,
            HotelCallExecutionRequest(preview=make_preview()),
        )

        self.assertEqual(response.mode, "dry_run")
        self.assertIsNone(response.command_result)
        self.assertEqual(executor.commands, [])

    def test_live_call_requires_configuration_and_approval(self):
        executor = FakeExecutor()
        runtime = CalleRuntime(
            config=CalleRuntimeConfig(
                executable="calle",
                timeout_seconds=30,
                allow_live_calls=False,
            ),
            executor=executor,
        )

        approval = CallApproval(
            approved=True,
            approved_by="Test User",
        )

        with self.assertRaises(PermissionError):
            execute_hotel_call(
                runtime,
                HotelCallExecutionRequest(
                    preview=make_preview(),
                    live_call=True,
                    approval=approval,
                ),
            )

    def test_approved_live_call_uses_runtime_boundary(self):
        executor = FakeExecutor()
        runtime = CalleRuntime(
            config=CalleRuntimeConfig(
                executable="calle",
                timeout_seconds=30,
                allow_live_calls=True,
            ),
            executor=executor,
        )

        approval = CallApproval(
            approved=True,
            approved_by="Test User",
        )

        response = execute_hotel_call(
            runtime,
            HotelCallExecutionRequest(
                preview=make_preview(),
                live_call=True,
                approval=approval,
            ),
        )

        self.assertEqual(response.mode, "live")
        self.assertTrue(response.succeeded)
        self.assertEqual(len(executor.commands), 1)

        command, timeout_seconds = executor.commands[0]

        self.assertEqual(command[0], "calle")
        self.assertIn("call", command)
        self.assertIn("run", command)
        self.assertEqual(timeout_seconds, 30)


if __name__ == "__main__":
    unittest.main()