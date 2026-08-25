"""Local readiness checks for macpymessenger."""

from __future__ import annotations

import platform
import shutil
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from .configuration import Configuration
from .exceptions import ConfigurationError

_MESSAGES_APP_PATHS = (
    Path("/System/Applications/Messages.app"),
    Path("/Applications/Messages.app"),
)


class CheckStatus(StrEnum):
    """Outcome of one environment check."""

    PASS = "pass"
    FAIL = "fail"
    INFO = "info"


@dataclass(frozen=True, slots=True)
class EnvironmentCheck:
    """One stable, machine-readable environment finding."""

    identifier: str
    status: CheckStatus
    summary: str
    fix: str | None = None

    def to_dict(self) -> dict[str, str | None]:
        """Return the public JSON shape for this check."""
        return {
            "id": self.identifier,
            "status": self.status.value,
            "summary": self.summary,
            "fix": self.fix,
        }


@dataclass(frozen=True, slots=True)
class EnvironmentReport:
    """All local checks needed before the first send."""

    checks: tuple[EnvironmentCheck, ...]

    @property
    def ready(self) -> bool:
        """Whether every check that can be verified locally passed."""
        return all(check.status is not CheckStatus.FAIL for check in self.checks)

    def to_dict(self) -> dict[str, object]:
        """Return the stable JSON payload shared by scripts and agents."""
        return {
            "ready": self.ready,
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
                status=CheckStatus.PASS,
                summary="macOS detected.",
            )
        )
    else:
        checks.append(
            EnvironmentCheck(
                identifier="platform",
                status=CheckStatus.FAIL,
                summary=f"macOS is required; found {system or 'an unknown platform'}.",
                fix="Run macpymessenger on a Mac.",
            )
        )

    osascript_path = shutil.which("osascript")
    if osascript_path is not None:
        checks.append(
            EnvironmentCheck(
                identifier="osascript",
                status=CheckStatus.PASS,
                summary=f"osascript found at {osascript_path}.",
            )
        )
    else:
        checks.append(
            EnvironmentCheck(
                identifier="osascript",
                status=CheckStatus.FAIL,
                summary="osascript was not found on PATH.",
                fix="Use the system Python environment on macOS and restore /usr/bin to PATH.",
            )
        )

    messages_app = next((path for path in _MESSAGES_APP_PATHS if path.is_dir()), None)
    if messages_app is not None:
        checks.append(
            EnvironmentCheck(
                identifier="messages-app",
                status=CheckStatus.PASS,
                summary=f"Messages found at {messages_app}.",
            )
        )
    else:
        checks.append(
            EnvironmentCheck(
                identifier="messages-app",
                status=CheckStatus.FAIL,
                summary="The Messages app was not found in a standard macOS location.",
                fix="Confirm that Messages is installed on this Mac.",
            )
        )

    try:
        configuration = Configuration()
    except ConfigurationError as error:
        checks.append(
            EnvironmentCheck(
                identifier="send-script",
                status=CheckStatus.FAIL,
                summary=str(error),
                fix="Reinstall macpymessenger from a complete wheel.",
            )
        )
    else:
        checks.append(
            EnvironmentCheck(
                identifier="send-script",
                status=CheckStatus.PASS,
                summary=f"Bundled send script is readable at {configuration.send_script_path}.",
            )
        )

    checks.extend(
        (
            EnvironmentCheck(
                identifier="automation",
                status=CheckStatus.INFO,
                summary="Automation permission is granted per Python launcher.",
                fix="Run one send, then check System Settings > Privacy & Security > Automation.",
            ),
            EnvironmentCheck(
                identifier="messages-account",
                status=CheckStatus.INFO,
                summary="Account sign-in cannot be checked without controlling Messages.",
                fix="Open Messages and confirm that you can send a message by hand.",
            ),
        )
    )

    return EnvironmentReport(checks=tuple(checks))
