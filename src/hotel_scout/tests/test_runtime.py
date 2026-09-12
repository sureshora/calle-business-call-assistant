from hotel_scout.approval import CallApproval
from hotel_scout.calle_runtime import CalleCommandResult, CalleRuntime
from hotel_scout.runtime_config import CalleRuntimeConfig


def fake_executor(command, timeout_seconds):
    return CalleCommandResult(tuple(command), 0, "ok", "")


def test_non_live_command_uses_executor():
    runtime = CalleRuntime(
        CalleRuntimeConfig(executable="calle", timeout_seconds=10),
        executor=fake_executor,
    )
    result = runtime.help()
    assert result.succeeded
    assert result.command == ("calle", "--help")


def test_live_call_requires_configuration():
    runtime = CalleRuntime(
        CalleRuntimeConfig(allow_live_calls=False),
        executor=fake_executor,
    )
    try:
        runtime.execute(("run_call",), live_call=True)
    except PermissionError as exc:
        assert "disabled" in str(exc)
    else:
        raise AssertionError("Live calls must be blocked by default")


def test_live_call_requires_explicit_approval():
    runtime = CalleRuntime(
        CalleRuntimeConfig(allow_live_calls=True),
        executor=fake_executor,
    )
    try:
        runtime.execute(("run_call",), live_call=True, approval=CallApproval())
    except PermissionError as exc:
        assert "approval" in str(exc).lower()
    else:
        raise AssertionError("Unapproved live calls must be blocked")
