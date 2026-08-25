from __future__ import annotations

import json
from pathlib import Path

import pytest

from macpymessenger import __version__
from macpymessenger import __main__ as cli
from macpymessenger import diagnostics
from macpymessenger.diagnostics import (
    CheckStatus,
    EnvironmentCheck,
    EnvironmentReport,
    diagnose_environment,
)


def test_diagnostics_report_a_ready_mac_without_running_applescript(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    messages_app = tmp_path / "Messages.app"
    messages_app.mkdir()
    monkeypatch.setattr(diagnostics.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(diagnostics.shutil, "which", lambda command: f"/usr/bin/{command}")
    monkeypatch.setattr(diagnostics, "_MESSAGES_APP_PATHS", (messages_app,))

    report = diagnose_environment()

    assert report.ready is True
    assert [check.identifier for check in report.checks[:4]] == [
        "platform",
        "osascript",
        "messages-app",
        "send-script",
    ]
    assert all(check.status is CheckStatus.PASS for check in report.checks[:4])
    assert all(check.status is CheckStatus.INFO for check in report.checks[4:])


def test_diagnostics_report_missing_local_requirements(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(diagnostics.platform, "system", lambda: "Linux")
    monkeypatch.setattr(diagnostics.shutil, "which", lambda _command: None)
    monkeypatch.setattr(diagnostics, "_MESSAGES_APP_PATHS", ())

    report = diagnose_environment()

    assert report.ready is False
    failed = {check.identifier for check in report.checks if check.status is CheckStatus.FAIL}
    assert failed == {"platform", "osascript", "messages-app"}


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
                fix="Run macpymessenger on a Mac.",
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
        "ready": False,
        "checks": [
            {
                "id": "platform",
                "status": "fail",
                "summary": "macOS is required; found Linux.",
                "fix": "Run macpymessenger on a Mac.",
            }
        ],
    }


def test_doctor_text_gives_the_next_action(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    report = EnvironmentReport(
        checks=(
            EnvironmentCheck(
                identifier="automation",
                status=CheckStatus.INFO,
                summary="Automation permission is granted per Python launcher.",
                fix="Check System Settings > Privacy & Security > Automation.",
            ),
        )
    )
    monkeypatch.setattr(cli, "diagnose_environment", lambda: report)

    exit_code = cli.main(["doctor"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "INFO automation: Automation permission is granted per Python launcher." in output
    assert "Next: Check System Settings > Privacy & Security > Automation." in output
