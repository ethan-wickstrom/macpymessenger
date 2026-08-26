"""Side-effect-free local prerequisite checks."""

from __future__ import annotations

import os
import platform
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from .exceptions import ScriptNotFoundError
from .transport import _load_script_source

_OSASCRIPT_PATH = Path("/usr/bin/osascript")
_MESSAGES_APP_PATHS = (
    Path("/System/Applications/Messages.app"),
    Path("/Applications/Messages.app"),
)


class CheckStatus(StrEnum):
    """Outcome of one environment check."""

    OK = "ok"
    FAIL = "fail"
    MANUAL = "manual"


@dataclass(frozen=True, slots=True)
class EnvironmentCheck:
    """One stable, machine-readable environment finding."""

    identifier: str
    status: CheckStatus
    summary: str
    next_step: str | None = None

    def to_dict(self) -> dict[str, str | None]:
        """Return the public JSON shape for this check."""
        return {
            "identifier": self.identifier,
            "status": self.status.value,
            "summary": self.summary,
            "next_step": self.next_step,
        }


@dataclass(frozen=True, slots=True)
class EnvironmentReport:
    """Automated blockers and manual checks for a first send."""

    checks: tuple[EnvironmentCheck, ...]

    @property
    def blocked(self) -> bool:
        """Whether an automated check found a definite local blocker."""
        return any(check.status is CheckStatus.FAIL for check in self.checks)

    def to_dict(self) -> dict[str, object]:
        """Return the stable JSON payload shared by scripts and agents."""
        return {
            "blocked": self.blocked,
            "checks": [check.to_dict() for check in self.checks],
        }


def diagnose_environment() -> EnvironmentReport:
    """Inspect local prerequisites without opening Messages or sending text."""
    checks: list[EnvironmentCheck] = []

    system = platform.system()
    if system == "Darwin":
        checks.append(
            EnvironmentCheck(
                identifier="platform",
                status=CheckStatus.OK,
                summary="macOS detected.",
            )
        )
    else:
        checks.append(
            EnvironmentCheck(
                identifier="platform",
                status=CheckStatus.FAIL,
                summary=f"macOS is required; found {system or 'an unknown platform'}.",
                next_step="Run macpymessenger on a Mac.",
            )
        )

    if _OSASCRIPT_PATH.is_file() and os.access(_OSASCRIPT_PATH, os.X_OK):
        checks.append(
            EnvironmentCheck(
                identifier="osascript",
                status=CheckStatus.OK,
                summary="The system osascript executable is available.",
            )
        )
    else:
        checks.append(
            EnvironmentCheck(
                identifier="osascript",
                status=CheckStatus.FAIL,
                summary="The system osascript executable is unavailable.",
                next_step="Restore /usr/bin/osascript by repairing or updating macOS.",
            )
        )

    if any(path.is_dir() for path in _MESSAGES_APP_PATHS):
        checks.append(
            EnvironmentCheck(
                identifier="messages-app",
                status=CheckStatus.OK,
                summary="The Messages app is installed.",
            )
        )
    else:
        checks.append(
            EnvironmentCheck(
                identifier="messages-app",
                status=CheckStatus.FAIL,
                summary="The Messages app was not found in a standard macOS location.",
                next_step="Confirm that Messages is installed on this Mac.",
            )
        )

    try:
        _load_script_source()
    except ScriptNotFoundError:
        checks.append(
            EnvironmentCheck(
                identifier="send-script",
                status=CheckStatus.FAIL,
                summary="Bundled AppleScript could not be read.",
                next_step="Reinstall macpymessenger from a complete wheel.",
            )
        )
    else:
        checks.append(
            EnvironmentCheck(
                identifier="send-script",
                status=CheckStatus.OK,
                summary="Bundled AppleScript is readable.",
            )
        )

    checks.extend(
        (
            EnvironmentCheck(
                identifier="automation",
                status=CheckStatus.MANUAL,
                summary=(
                    "Automation permission cannot be checked without sending an Apple event."
                ),
                next_step=(
                    "Run one send, then check System Settings > Privacy & Security > "
                    "Automation."
                ),
            ),
            EnvironmentCheck(
                identifier="messages-account",
                status=CheckStatus.MANUAL,
                summary="Messages account sign-in cannot be checked without controlling Messages.",
                next_step="Open Messages and confirm that you can send a message by hand.",
            ),
        )
    )

    return EnvironmentReport(checks=tuple(checks))
