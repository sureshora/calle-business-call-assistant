"""Provider-neutral CALL-E runtime boundary for CALL-E-006."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, Sequence

from .approval import CallApproval, require_explicit_approval
from .runtime_config import CalleRuntimeConfig


@dataclass(frozen=True)
class CalleCommandResult:
    command: tuple[str, ...]
    returncode: int
    stdout: str = ""
    stderr: str = ""

    @property
    def succeeded(self) -> bool:
        return self.returncode == 0


class CalleCommandExecutor(Protocol):
    def __call__(self, command: Sequence[str], timeout_seconds: int) -> CalleCommandResult:
        ...


class CalleRuntime:
    """Safe runtime boundary; execution is injected by the host application."""

    def __init__(
        self,
        config: CalleRuntimeConfig | None = None,
        executor: CalleCommandExecutor | None = None,
    ) -> None:
        self.config = config or CalleRuntimeConfig.from_environment()
        self.executor = executor

    def execute(
        self,
        arguments: Sequence[str],
        *,
        live_call: bool = False,
        approval: CallApproval | None = None,
    ) -> CalleCommandResult:
        if self.executor is None:
            raise RuntimeError("No CALL-E command executor has been configured.")
        if live_call:
            if not self.config.allow_live_calls:
                raise PermissionError("Live CALL-E calls are disabled by configuration.")
            if approval is None:
                raise PermissionError("Explicit approval is required for live calls.")
            require_explicit_approval(approval)
        command = (self.config.executable, *arguments)
        return self.executor(command, self.config.timeout_seconds)

    def help(self) -> CalleCommandResult:
        return self.execute(("--help",))

    def auth_status(self) -> CalleCommandResult:
        return self.execute(("auth", "status" ,))

    def mcp_tools(self) -> CalleCommandResult:
        return self.execute(("mcp", "tools"))

    def plan_call(self, *, to_phone: str, goal: str) -> CalleCommandResult:
        return self.execute(("call", "plan", "--to-phone", to_phone, "--goal", goal))

    def assert_live_call_permitted(self, approval: CallApproval) -> None:
        if not self.config.allow_live_calls:
            raise PermissionError("Live CALL-E calls are disabled by configuration.")
        require_explicit_approval(approval)
