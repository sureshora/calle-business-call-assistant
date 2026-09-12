import unittest

from src.hotel_scout.approval import CallApproval
from src.hotel_scout.calle_runtime import (
    CalleCommandResult,
    CalleRuntime,
)
from src.hotel_scout.runtime_config import CalleRuntimeConfig


class FakeExecutor:
    def __init__(self) -> None:
        self.commands = []

    def __call__(self, command, timeout_seconds):
        self.commands.append((tuple(command), timeout_seconds))
        return CalleCommandResult(
            command=tuple(command),
            returncode=0,
            stdout="ok",
            stderr="",
        )


class RuntimeTests(unittest.TestCase):
    def test_help_uses_configured_executable(self):
        executor = FakeExecutor()

        runtime = CalleRuntime(
            config=CalleRuntimeConfig(
                executable="calle-test",
                timeout_seconds=20,
                allow_live_calls=False,
            ),
            executor=executor,
        )

        result = runtime.help()

        self.assertTrue(result.succeeded)
        self.assertEqual(
            executor.commands[0],
            (("calle-test", "--help"), 20),
        )

    def test_auth_status_uses_runtime_boundary(self):
        executor = FakeExecutor()

        runtime = CalleRuntime(
            config=CalleRuntimeConfig(
                executable="calle-test",
                timeout_seconds=20,
                allow_live_calls=False,
            ),
            executor=executor,
        )

        result = runtime.auth_status()

        self.assertTrue(result.succeeded)
        self.assertEqual(
            executor.commands[0],
            (("calle-test", "auth", "status"), 20),
        )

    def test_mcp_tools_uses_runtime_boundary(self):
        executor = FakeExecutor()

        runtime = CalleRuntime(
            config=CalleRuntimeConfig(
                executable="calle-test",
                timeout_seconds=20,
                allow_live_calls=False,
            ),
            executor=executor,
        )

        result = runtime.mcp_tools()

        self.assertTrue(result.succeeded)
        self.assertEqual(
            executor.commands[0],
            (("calle-test", "mcp", "tools"), 20),
        )

    def test_live_call_requires_configuration(self):
        executor = FakeExecutor()

        runtime = CalleRuntime(
            config=CalleRuntimeConfig(
                executable="calle-test",
                timeout_seconds=20,
                allow_live_calls=False,
            ),
            executor=executor,
        )

        approval = CallApproval(
            approved=True,
            approved_by="Test User",
        )

        with self.assertRaises(PermissionError):
            runtime.execute(
                (
                    "call",
                    "run",
                    "--to-phone",
                    "+919999999999",
                    "--goal",
                    "Controlled test only",
                ),
                live_call=True,
                approval=approval,
            )

        self.assertEqual(executor.commands, [])

    def test_live_call_requires_explicit_approval(self):
        executor = FakeExecutor()

        runtime = CalleRuntime(
            config=CalleRuntimeConfig(
                executable="calle-test",
                timeout_seconds=20,
                allow_live_calls=True,
            ),
            executor=executor,
        )

        with self.assertRaises(PermissionError):
            runtime.execute(
                (
                    "call",
                    "run",
                    "--to-phone",
                    "+919999999999",
                    "--goal",
                    "Controlled test only",
                ),
                live_call=True,
                approval=None,
            )

        self.assertEqual(executor.commands, [])

    def test_approved_live_call_is_forwarded(self):
        executor = FakeExecutor()

        runtime = CalleRuntime(
            config=CalleRuntimeConfig(
                executable="calle-test",
                timeout_seconds=20,
                allow_live_calls=True,
            ),
            executor=executor,
        )

        approval = CallApproval(
            approved=True,
            approved_by="Test User",
        )

        result = runtime.execute(
            (
                "call",
                "run",
                "--to-phone",
                "+919999999999",
                "--goal",
                "Controlled test only",
            ),
            live_call=True,
            approval=approval,
        )

        self.assertTrue(result.succeeded)
        self.assertEqual(
            executor.commands[0],
            (
                (
                    "calle-test",
                    "call",
                    "run",
                    "--to-phone",
                    "+919999999999",
                    "--goal",
                    "Controlled test only",
                ),
                20,
            ),
        )


if __name__ == "__main__":
    unittest.main()