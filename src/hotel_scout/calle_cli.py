"""Local subprocess executor for the CALL-E CLI."""

from __future__ import annotations

import subprocess
from typing import Sequence

from .calle_runtime import CalleCommandResult
from .runtime_config import CalleRuntimeConfig


def execute_calle_cli(
    command: Sequence[str],
    timeout_seconds: int,
) -> CalleCommandResult:
    """Execute a previously constructed CALL-E command."""
    completed = subprocess.run(
        tuple(command),
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
        check=False,
    )
    return CalleCommandResult(
        command=tuple(command),
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )


def build_runtime(config: CalleRuntimeConfig | None = None):
    """Build a CALL-E runtime using the local CLI executor."""
    from .calle_runtime import CalleRuntime

    resolved = config or CalleRuntimeConfig.from_environment()
    return CalleRuntime(config=resolved, executor=execute_calle_cli)
