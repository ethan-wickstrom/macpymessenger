"""Verify the installed macpymessenger distribution without sending a message."""

from __future__ import annotations

import json
import shutil
import subprocess
from importlib.resources import files
from typing import Final

from macpymessenger import (
    AppleScriptTransport,
    BulkSendResult,
    IMessageClient,
    MessageFailureReason,
    SendRequest,
    TemplateManager,
    __version__,
)

_PRIVATE_RECIPIENT: Final = "private-recipient"
_PRIVATE_MESSAGE: Final = "private-message"
_CORE_SKILL_DESCRIPTION: Final = (
    "Use this skill when the user explicitly asks an agent to send an "
    "iMessage through the local macOS Messages app or inspect "
    "macpymessenger readiness."
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _command_path() -> str:
    command = shutil.which("macpymessenger")
    if command is None:
        message = "the installed console script is missing"
        raise RuntimeError(message)
    return command


def _run_cli(
    *arguments: str,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(  # noqa: S603
        (_command_path(), *arguments),
        input=input_text,
        capture_output=True,
        check=False,
        text=True,
    )


def _verify_package_data_and_api() -> None:
    package = files("macpymessenger")
    _require(__version__ != "0+unknown", "distribution metadata has no version")
    _require(package.joinpath("py.typed").is_file(), "py.typed is missing")
    _require(
        package.joinpath("osascript", "sendMessage.applescript").is_file(),
        "bundled AppleScript is missing",
    )
    _require(
        package.joinpath("skills", "core", "SKILL.md").is_file(),
        "bundled core Agent Skill is missing",
    )
    _require(
        isinstance(IMessageClient().transport, AppleScriptTransport),
        "the default client does not own AppleScriptTransport",
    )
    _require(
        SendRequest("+15555550123", "Hello").delay_seconds == 0,
        "SendRequest default delay changed",
    )
    _require(BulkSendResult((), ()).sent == (), "BulkSendResult shape changed")
    _require(TemplateManager().list_templates() == {}, "TemplateManager default state changed")
    _require(
        MessageFailureReason.__name__ == "MessageFailureReason",
        "MessageFailureReason is not public",
    )


def _verify_version_and_help() -> None:
    version = _run_cli("--version")
    _require(version.returncode == 0, "--version failed")
    _require(version.stdout.strip() == __version__, "--version output does not match metadata")
    _require(version.stderr == "", "--version wrote to standard error")

    help_result = _run_cli("--help")
    _require(help_result.returncode == 0, "--help failed")
    _require(
        "macpymessenger skills get core" in help_result.stdout,
        "top-level help does not route agents to the core skill",
    )
    _require(
        "version-matched" in help_result.stdout,
        "top-level help omits skill versioning",
    )

    send_help = _run_cli("send", "--help")
    _require(send_help.returncode == 0, "send --help failed")
    _require(
        "one JSON object from standard input" in send_help.stdout,
        "send input is undocumented",
    )
    _require("Exit status:" in send_help.stdout, "send exit codes are undocumented")


def _verify_doctor() -> None:
    result = _run_cli("doctor", "--json")
    _require(result.returncode in {0, 1}, "doctor returned an unknown exit status")
    _require(result.stderr == "", "doctor JSON wrote to standard error")
    payload = json.loads(result.stdout)
    _require(payload["tool"] == "macpymessenger-doctor", "doctor tool identifier changed")
    _require(isinstance(payload["blocked"], bool), "doctor blocked field is not boolean")
    _require("ready" not in payload, "doctor restored the unsound ready field")
    checks = payload["checks"]
    _require(isinstance(checks, list) and bool(checks), "doctor returned no checks")
    for check in checks:
        _require(
            set(check) == {"identifier", "status", "summary", "next_step"},
            "doctor check shape changed",
        )
        _require(check["status"] in {"ok", "fail", "manual"}, "doctor status changed")


def _verify_skills() -> None:
    catalog_result = _run_cli("skills", "list", "--json")
    _require(catalog_result.returncode == 0, "skills list --json failed")
    _require(catalog_result.stderr == "", "skill catalog wrote to standard error")
    catalog = json.loads(catalog_result.stdout)
    _require(catalog["tool"] == "macpymessenger-skills", "skill tool identifier changed")
    _require(
        catalog["skills"] == [{"name": "core", "description": _CORE_SKILL_DESCRIPTION}],
        "skill catalog changed",
    )

    bare_catalog = _run_cli("skills")
    _require(bare_catalog.returncode == 0, "bare skills command failed")
    _require(bare_catalog.stdout.startswith("core\t"), "bare skills output is not composable")

    core = _run_cli("skills", "get", "core")
    _require(core.returncode == 0, "skills get core failed")
    _require(core.stderr == "", "skills get core wrote to standard error")
    _require(core.stdout.startswith("---\nname: core\n"), "core skill frontmatter changed")
    _require("macpymessenger send --json" in core.stdout, "core skill omits the send command")
    _require("MCP" not in core.stdout, "core skill recommends an excluded integration")


def _verify_invalid_send() -> None:
    request = json.dumps(
        {
            "recipient": _PRIVATE_RECIPIENT,
            "message": _PRIVATE_MESSAGE,
            "unexpected": True,
        }
    )
    result = _run_cli("send", "--json", input_text=request)
    _require(result.returncode == 2, "invalid send input did not return exit status 2")
    _require(result.stderr == "", "invalid send JSON wrote to standard error")
    _require(_PRIVATE_RECIPIENT not in result.stdout, "send output exposed the recipient")
    _require(_PRIVATE_MESSAGE not in result.stdout, "send output exposed the message")
    payload = json.loads(result.stdout)
    _require(
        payload == {
            "tool": "macpymessenger-send",
            "version": __version__,
            "ok": False,
            "error": {"code": "invalid_input"},
        },
        "invalid send result shape changed",
    )


def main() -> None:
    _verify_package_data_and_api()
    _verify_version_and_help()
    _verify_doctor()
    _verify_skills()
    _verify_invalid_send()


if __name__ == "__main__":
    main()
