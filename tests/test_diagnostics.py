from __future__ import annotations

import json
from typing import TYPE_CHECKING

import macpymessenger.__main__ as cli
from macpymessenger import Configuration, __version__, diagnostics
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
    monkeypatch.setattr(diagnostics.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(diagnostics.shutil, "which", lambda command: f"/usr/bin/{command}")
    monkeypatch.setattr(diagnostics, "_MESSAGES_APP_PATHS", (messages_app,))

    report = diagnose_environment()

    assert hasattr(report, "blocked")
    assert report.blocked is False
    assert not hasattr(report, "ready")
    assert [check.identifier for check in report.checks[:4]] == [
        "platform",
        "osascript",
        "messages-app",
        "send-script",
    ]
    assert all(check.status is CheckStatus.OK for check in report.checks[:4])
    assert all(check.status is CheckStatus.INFO for check in report.checks[4:])


def test_diagnostics_report_missing_local_requirements(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(diagnostics.platform, "system", lambda: "Linux")
    monkeypatch.setattr(diagnostics.shutil, "which", lambda _command: None)
    monkeypatch.setattr(diagnostics, "_MESSAGES_APP_PATHS", ())

    report = diagnose_environment()

    assert hasattr(report, "blocked")
    assert report.blocked is True
    failed = {check.identifier for check in report.checks if check.status is CheckStatus.FAIL}
    assert failed == {"platform", "osascript", "messages-app"}


def test_diagnostics_do_not_expose_the_installed_script_path() -> None:
    script_path = str(Configuration().send_script_path)
    report = diagnose_environment()
    send_script = next(check for check in report.checks if check.identifier == "send-script")

    assert script_path not in send_script.summary
    assert send_script.fix is None or script_path not in send_script.fix


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
        "blocked": True,
        "checks": [
            {
                "id": "platform",
                "status": "fail",
                "summary": "macOS is required; found Linux.",
                "fix": "Run macpymessenger on a Mac.",
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
    assert "No detectable local blockers. Complete the INFO checks before sending." in output
    assert "Ready for a first send." not in output
