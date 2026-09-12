"""Non-destructive CALL-E runtime verification demo."""

from __future__ import annotations

from .calle_cli import build_runtime


def main() -> None:
    runtime = build_runtime()
    print("CALL-E-006 — RUNTIME VERIFICATION")
    for label, method in (
        ("CLI help", runtime.help),
        ("Authentication status", runtime.auth_status),
        ("MCP tools", runtime.mcp_tools),
    ):
        print(f"\n--- {label} ---")
        try:
            result = method()
        except FileNotFoundError:
            print("CALL-E CLI was not found. Install it before running this demo.")
            continue
        print(f"returncode={result.returncode}")
        if result.stdout:
            print(result.stdout.rstrip())
        if result.stderr:
            print(result.stderr.rstrip())
    print("\nNo live call was placed.")


if __name__ == "__main__":
    main()
