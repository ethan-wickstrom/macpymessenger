from __future__ import annotations

import json
from typing import TYPE_CHECKING

import macpymessenger.__main__ as cli
from macpymessenger import __version__, diagnostics
from macpymessenger.diagnostics import (
    CheckStatus,
    EnvironmentCheck,
    EnvironmentReport,
    diagnose_environment,
)

if TYPE_CHECKING:
    from pathlib import Path

    import pytest


def test_diagnostics_report_passes_automated_checks_without_claiming_readiness(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    messages_app = tmp_path / "Messages.app"
    messages_app.mkdir()
    osascript = tmp_path / "osascript"
    osascript.write_text("", encoding="utf-8")
    monkeypatch.setattr(diagnostics.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(diagnostics, "_OSASCRIPT_PATH", osascript)
    monkeypatch.setattr(diagnostics.os, "access", lambda _path, _mode: True)
    monkeypatch.setattr(diagnostics, "_MESSAGES_APP_PATHS", (messages_app,))
    monkeypatch.setattr(diagnostics, "_load_script_source", lambda: "on sendMessage()\nend")

    report = diagnose_environment()

    assert report.blocked is False
    assert not hasattr(report, "ready")
    assert [check.identifier for check in report.checks[:4]] == [
        "platform",
        "osascript",
        "messages-app",
        "send-script",
    ]
    assert all(check.status is CheckStatus.OK for check in report.checks[:4])
    assert all(check.status is CheckStatus.MANUAL for check in report.checks[4:])


def test_diagnostics_report_missing_local_requirements(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(diagnostics.platform, "system", lambda: "Linux")
    monkeypatch.setattr(diagnostics, "_OSASCRIPT_PATH", tmp_path / "missing-osascript")
    monkeypatch.setattr(diagnostics, "_MESSAGES_APP_PATHS", ())

    report = diagnose_environment()

    assert report.blocked is True
    failed = {check.identifier for check in report.checks if check.status is CheckStatus.FAIL}
    assert failed == {"platform", "osascript", "messages-app"}


def test_diagnostics_do_not_expose_the_installed_script_path() -> None:
    report = diagnose_environment()
    send_script = next(check for check in report.checks if check.identifier == "send-script")

    assert send_script.summary in {
        "Bundled AppleScript is readable.",
        "Bundled AppleScript could not be read.",
    }
    assert "/" not in send_script.summary
    assert send_script.next_step is None or "/" not in send_script.next_step


def test_doctor_json_is_stable_for_agents(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    report = EnvironmentReport(
        checks=(
            EnvironmentCheck(
                identifier="platform",
                status=CheckStatus.FAIL,
                summary="macOS is required; found Linux.",
                next_step="Run macpymessenger on a Mac.",
            ),
        )
    )
    monkeypatch.setattr(cli, "diagnose_environment", lambda: report)

    exit_code = cli.main(["doctor", "--json"])
    payload = json.loads(capsys.readouterr().out)

    assert exit_code == 1
    assert payload == {
        "tool": "macpymessenger-doctor",
        "version": __version__,
        "blocked": True,
        "checks": [
            {
                "identifier": "platform",
                "status": "fail",
                "summary": "macOS is required; found Linux.",
                "next_step": "Run macpymessenger on a Mac.",
            }
        ],
    }


def test_doctor_text_gives_the_next_action_without_claiming_readiness(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    report = EnvironmentReport(
        checks=(
            EnvironmentCheck(
                identifier="automation",
                status=CheckStatus.MANUAL,
                summary="Automation permission cannot be checked without sending an Apple event.",
                next_step="Check System Settings > Privacy & Security > Automation.",
            ),
        )
    )
    monkeypatch.setattr(cli, "diagnose_environment", lambda: report)

    exit_code = cli.main(["doctor"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "MANUAL automation: Automation permission cannot be checked" in output
    assert "Next: Check System Settings > Privacy & Security > Automation." in output
    assert "No detectable local blockers. Complete the MANUAL checks before sending." in output
    assert "Ready for a first send." not in output
