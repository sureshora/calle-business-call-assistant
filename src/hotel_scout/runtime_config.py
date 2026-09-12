"""Runtime configuration for the CALL-E CLI adapter."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class CalleRuntimeConfig:
    """Configuration loaded from environment variables.

    The CLI normally obtains authentication from its own local auth state.
    Environment variables here control executable selection and safety mode;
    secrets are never written to project files.
    """

    executable: str = "calle"
    timeout_seconds: int = 180
    allow_live_calls: bool = False

    @classmethod
    def from_environment(cls) -> "CalleRuntimeConfig":
        executable = os.getenv("CALLE_EXECUTABLE", "calle").strip() or "calle"
        timeout_raw = os.getenv("CALLE_TIMEOUT_SECONDS", "180").strip()
        try:
            timeout_seconds = int(timeout_raw)
        except ValueError as exc:
            raise ValueError("CALLE_TIMEOUT_SECONDS must be an integer") from exc
        if timeout_seconds <= 0:
            raise ValueError("CALLE_TIMEOUT_SECONDS must be greater than zero")

        allow_live_calls = os.getenv("CALLE_ALLOW_LIVE_CALLS", "0").lower() in {
            "1",
            "true",
            "yes",
            "on",
        }
        return cls(
            executable=executable,
            timeout_seconds=timeout_seconds,
            allow_live_calls=allow_live_calls,
        )
