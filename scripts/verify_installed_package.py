"""Verify the installed macpymessenger distribution without sending a message."""

from __future__ import annotations

import json
import shutil
import subprocess
from importlib.resources import files
from typing import Final

from macpymessenger import (
    AppleScriptTransport,
    BulkSendFailure,
    BulkSendResult,
    IMessageClient,
    InvalidSendTextError,
    MessageFailureReason,
    SendRequest,
    TemplateManager,
    __version__,
)

_INVALID_INPUT_EXIT_CODE: Final = 2
_JSON_SCHEMA_VERSION: Final = 1
_PRIVATE_RECIPIENT: Final = "private-recipient"
_PRIVATE_MESSAGE: Final = "private-message"
_CORE_SKILL_DESCRIPTION: Final = (
    "Use this skill when the user explicitly asks an agent to send an "
    "iMessage through the local macOS Messages app or inspect "
    "macpymessenger readiness."
)


def _require(message: str, *, condition: bool) -> None:
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
    _require("distribution metadata has no version", condition=__version__ != "0+unknown")
    _require("py.typed is missing", condition=package.joinpath("py.typed").is_file())
    _require(
        "bundled AppleScript is missing",
        condition=package.joinpath("osascript", "sendMessage.applescript").is_file(),
    )
    _require(
        "bundled core Agent Skill is missing",
        condition=package.joinpath("skills", "core", "SKILL.md").is_file(),
    )
    _require(
        "the default client does not own AppleScriptTransport",
        condition=isinstance(IMessageClient().transport, AppleScriptTransport),
    )
    _require(
        "SendRequest default delay changed",
        condition=SendRequest("+15555550123", "Hello").delay_seconds == 0,
    )
    try:
        SendRequest("", "Hello")
    except InvalidSendTextError as error:
        _require(
            "SendRequest empty-recipient error is not structured",
            condition=error.field == "recipient" and error.reason == "empty",
        )
    else:
        message = "SendRequest accepted an empty recipient"
        raise RuntimeError(message)

    empty_bulk = BulkSendResult(sent=(), failures=())
    _require("BulkSendResult sent shape changed", condition=empty_bulk.sent == ())
    _require("BulkSendResult failed projection changed", condition=empty_bulk.failed == ())
    _require("BulkSendResult success state changed", condition=empty_bulk.ok)
    _require(
        "BulkSendResult unpacking changed",
        condition=tuple(empty_bulk) == ((), ()),
    )
    failure = BulkSendFailure(recipient="private-recipient", reason="delivery")
    _require(
        "BulkSendFailure shape changed",
        condition=failure.recipient == "private-recipient" and failure.reason == "delivery",
    )
    _require(
        "TemplateManager default state changed",
        condition=TemplateManager().list_templates() == {},
    )
    _require(
        "MessageFailureReason is not public",
        condition=MessageFailureReason.__name__ == "MessageFailureReason",
    )
    _require(
        "IMessageClient.send_request is missing",
        condition=callable(IMessageClient.send_request),
    )


def _verify_version_and_help() -> None:
    version = _run_cli("--version")
    _require("--version failed", condition=version.returncode == 0)
    _require(
        "--version output does not match metadata",
        condition=version.stdout.strip() == __version__,
    )
    _require("--version wrote to standard error", condition=version.stderr == "")

    help_result = _run_cli("--help")
    _require("--help failed", condition=help_result.returncode == 0)
    _require(
        "top-level help does not route agents to the core skill",
        condition="macpymessenger skills get core" in help_result.stdout,
    )
    _require(
        "top-level help omits skill versioning",
        condition="version-matched" in help_result.stdout,
    )

    send_help = _run_cli("send", "--help")
    _require("send --help failed", condition=send_help.returncode == 0)
    _require(
        "send input is undocumented",
        condition="one JSON object from standard input" in send_help.stdout,
    )
    _require("send dry-run is undocumented", condition="--dry-run" in send_help.stdout)
    _require("send exit codes are undocumented", condition="Exit status:" in send_help.stdout)
    _require(
        "send success boundary is undocumented",
        condition="request validated or transport completed" in send_help.stdout,
    )


def _verify_envelope(payload: dict[str, object], *, command: str) -> None:
    _require(
        f"{command} schema version changed",
        condition=payload.get("schema_version") == _JSON_SCHEMA_VERSION,
    )
    _require(
        f"{command} tool identifier changed",
        condition=payload.get("tool") == "macpymessenger",
    )
    _require(
        f"{command} command identifier changed",
        condition=payload.get("command") == command,
    )
    _require(
        f"{command} version does not match metadata",
        condition=payload.get("version") == __version__,
    )
    _require(
        f"{command} ok field is not boolean",
        condition=isinstance(payload.get("ok"), bool),
    )


def _verify_doctor() -> None:
    result = _run_cli("doctor", "--json")
    _require(
        "doctor returned an unknown exit status",
        condition=result.returncode in {0, 1},
    )
    _require("doctor JSON wrote to standard error", condition=result.stderr == "")
    payload = json.loads(result.stdout)
    _verify_envelope(payload, command="doctor")
    data = payload.get("data")
    _require("doctor data is not an object", condition=isinstance(data, dict))
    blocked = data.get("blocked")
    _require("doctor blocked field is not boolean", condition=isinstance(blocked, bool))
    _require("doctor restored the unsound ready field", condition="ready" not in data)
    _require(
        "doctor ok disagrees with blocked",
        condition=payload["ok"] is (not blocked),
    )
    checks = data.get("checks")
    _require(
        "doctor returned no checks",
        condition=isinstance(checks, list) and bool(checks),
    )
    for check in checks:
        _require(
            "doctor check is not an object",
            condition=isinstance(check, dict),
        )
        _require(
            "doctor check shape changed",
            condition=set(check) == {"identifier", "status", "summary", "next_step"},
        )
        _require(
            "doctor status changed",
            condition=check["status"] in {"ok", "fail", "manual"},
        )


def _verify_skills() -> None:
    catalog_result = _run_cli("skills", "list", "--json")
    _require("skills list --json failed", condition=catalog_result.returncode == 0)
    _require("skill catalog wrote to standard error", condition=catalog_result.stderr == "")
    catalog = json.loads(catalog_result.stdout)
    _verify_envelope(catalog, command="skills.list")
    _require(
        "skill catalog changed",
        condition=catalog.get("data")
        == {
            "skills": [
                {
                    "name": "core",
                    "description": _CORE_SKILL_DESCRIPTION,
                }
            ]
        },
    )

    bare_catalog = _run_cli("skills")
    _require("bare skills command failed", condition=bare_catalog.returncode == 0)
    _require(
        "bare skills output is not composable",
        condition=bare_catalog.stdout.startswith("core\t"),
    )

    core = _run_cli("skills", "get", "core")
    _require("skills get core failed", condition=core.returncode == 0)
    _require("skills get core wrote to standard error", condition=core.stderr == "")
    _require(
        "core skill frontmatter changed",
        condition=core.stdout.startswith("---\nname: core\n"),
    )
    _require(
        "core skill omits the send command",
        condition="macpymessenger send --json" in core.stdout,
    )
    _require(
        "core skill omits safe validation",
        condition="macpymessenger send --dry-run --json" in core.stdout,
    )
    _require(
        "core skill recommends an excluded integration",
        condition="MCP" not in core.stdout,
    )


def _verify_invalid_send() -> None:
    request = json.dumps(
        {
            "recipient": _PRIVATE_RECIPIENT,
            "message": _PRIVATE_MESSAGE,
            "unexpected": True,
        }
    )
    result = _run_cli("send", "--json", input_text=request)
    _require(
        "invalid send input did not return exit status 2",
        condition=result.returncode == _INVALID_INPUT_EXIT_CODE,
    )
    _require("invalid send JSON wrote to standard error", condition=result.stderr == "")
    _require(
        "send output exposed the recipient",
        condition=_PRIVATE_RECIPIENT not in result.stdout,
    )
    _require(
        "send output exposed the message",
        condition=_PRIVATE_MESSAGE not in result.stdout,
    )
    payload = json.loads(result.stdout)
    _verify_envelope(payload, command="send")
    _require(
        "invalid send result shape changed",
        condition=payload.get("error")
        == {
            "code": "invalid_input",
            "retryable": False,
        },
    )


def _verify_send_dry_run() -> None:
    request = json.dumps(
        {
            "recipient": _PRIVATE_RECIPIENT,
            "message": _PRIVATE_MESSAGE,
            "delay_seconds": 0,
        }
    )
    result = _run_cli("send", "--dry-run", "--json", input_text=request)
    _require("send dry-run failed", condition=result.returncode == 0)
    _require("send dry-run wrote to standard error", condition=result.stderr == "")
    _require(
        "send dry-run output exposed the recipient",
        condition=_PRIVATE_RECIPIENT not in result.stdout,
    )
    _require(
        "send dry-run output exposed the message",
        condition=_PRIVATE_MESSAGE not in result.stdout,
    )
    payload = json.loads(result.stdout)
    _verify_envelope(payload, command="send")
    _require("send dry-run reported failure", condition=payload.get("ok") is True)
    _require(
        "send dry-run result shape changed",
        condition=payload.get("data") == {"outcome": "validated"},
    )


def main() -> None:
    _verify_package_data_and_api()
    _verify_version_and_help()
    _verify_doctor()
    _verify_skills()
    _verify_invalid_send()
    _verify_send_dry_run()


if __name__ == "__main__":
    main()
