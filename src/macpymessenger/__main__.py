"""Command-line entry point for macpymessenger."""

from __future__ import annotations

import argparse
import json
import sys
from typing import TYPE_CHECKING, Final, cast

from . import __version__
from .agent_skills import AgentSkillResourceError, list_skills, load_skill, skill_names
from .client import IMessageClient
from .diagnostics import EnvironmentReport, diagnose_environment
from .exceptions import (
    InvalidDelayTypeError,
    InvalidSendTextError,
    MessageFailureReason,
    MessageSendError,
    NegativeDelayError,
    ScriptNotFoundError,
)
from .transport import SendRequest

if TYPE_CHECKING:
    from collections.abc import Sequence

_SUCCESS: Final = 0
_SEND_FAILED: Final = 1
_INVALID_INPUT: Final = 2
_JSON_SCHEMA_VERSION: Final = 1
_TOOL_NAME: Final = "macpymessenger"
_SEND_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "delay_seconds",
        "message",
        "recipient",
    }
)
_REQUIRED_SEND_FIELDS: Final[frozenset[str]] = frozenset({"message", "recipient"})


class _InvalidSendInputError(ValueError):
    """Raised when standard input does not contain one valid send request."""


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="macpymessenger",
        description=(
            "Send iMessages from Python on macOS.\n\n"
            "Start here for AI agents:\n"
            "  macpymessenger skills get core\n\n"
            "This loads version-matched instructions from the installed package."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=__version__)
    subparsers = parser.add_subparsers(dest="command")

    doctor = subparsers.add_parser(
        "doctor",
        help="Check local requirements without sending a message.",
    )
    doctor.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Write stable machine-readable output.",
    )

    send = subparsers.add_parser(
        "send",
        help="Read one private send request as JSON from standard input.",
        description="Read one JSON object from standard input and send one message.",
        epilog=(
            "Input JSON:\n"
            '  {"recipient":"<recipient>","message":"<message>","delay_seconds":0}\n\n'
            "Fields:\n"
            '  "recipient"      required non-empty string\n'
            '  "message"        required non-empty string\n'
            '  "delay_seconds"  optional non-negative integer; default 0\n\n'
            "No other fields or duplicate keys are accepted.\n\n"
            "Exit status:\n"
            "  0  request validated or transport completed\n"
            "  1  send or transport failure\n"
            "  2  invalid input"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    send.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate input without creating a client or sending a message.",
    )
    send.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Write stable machine-readable output.",
    )

    skills = subparsers.add_parser(
        "skills",
        help="Read Agent Skills bundled with the installed package.",
    )
    skills.set_defaults(json_output=False)
    skill_commands = skills.add_subparsers(dest="skill_command")
    skill_list = skill_commands.add_parser("list", help="List bundled Agent Skills.")
    skill_list.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Write stable machine-readable output.",
    )
    skill_get = skill_commands.add_parser("get", help="Write one Agent Skill to standard output.")
    skill_get.add_argument("name", choices=skill_names())

    return parser


def _json_envelope(
    command: str,
    *,
    ok: bool,
    data: dict[str, object] | None = None,
    error: dict[str, object] | None = None,
) -> dict[str, object]:
    """Build the shared versioned JSON result shape."""
    payload: dict[str, object] = {
        "schema_version": _JSON_SCHEMA_VERSION,
        "tool": _TOOL_NAME,
        "command": command,
        "version": __version__,
        "ok": ok,
    }
    if data is not None:
        payload["data"] = data
    if error is not None:
        payload["error"] = error
    return payload


def _doctor_json_payload(report: EnvironmentReport) -> dict[str, object]:
    return _json_envelope(
        "doctor",
        ok=not report.blocked,
        data=report.to_dict(),
    )


def _write_json(payload: dict[str, object]) -> None:
    json.dump(payload, sys.stdout, separators=(",", ":"), sort_keys=True)
    sys.stdout.write("\n")


def _write_doctor_text(report: EnvironmentReport) -> None:
    sys.stdout.write(f"macpymessenger {__version__}\n\n")
    for check in report.checks:
        sys.stdout.write(f"{check.status.value.upper()} {check.identifier}: {check.summary}\n")
        if check.next_step is not None:
            sys.stdout.write(f"  Next: {check.next_step}\n")
    summary = (
        "Local requirements are missing."
        if report.blocked
        else "No detectable local blockers. Complete the MANUAL checks before sending."
    )
    sys.stdout.write(f"\n{summary}\n")


def _unique_json_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    """Build one JSON object while rejecting duplicate keys."""
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise _InvalidSendInputError
        result[key] = value
    return result


def _read_send_request() -> SendRequest:
    try:
        payload: object = json.load(sys.stdin, object_pairs_hook=_unique_json_object)
    except (json.JSONDecodeError, OSError, RecursionError, UnicodeError):
        raise _InvalidSendInputError from None

    if not isinstance(payload, dict):
        raise _InvalidSendInputError

    fields: dict[str, object] = {}
    for key, value in payload.items():
        if not isinstance(key, str):
            raise _InvalidSendInputError
        fields[key] = value

    field_names = fields.keys()
    if not _REQUIRED_SEND_FIELDS.issubset(field_names) or not field_names <= _SEND_FIELDS:
        raise _InvalidSendInputError

    try:
        return SendRequest(
            recipient=cast("str", fields["recipient"]),
            message=cast("str", fields["message"]),
            delay_seconds=cast("int", fields.get("delay_seconds", 0)),
        )
    except (InvalidDelayTypeError, InvalidSendTextError, NegativeDelayError):
        raise _InvalidSendInputError from None


def _send_success_payload(outcome: str) -> dict[str, object]:
    return _json_envelope(
        "send",
        ok=True,
        data={"outcome": outcome},
    )


def _send_error_payload(
    code: str,
    *,
    reason: MessageFailureReason | None = None,
) -> dict[str, object]:
    error: dict[str, object] = {
        "code": code,
        "retryable": False,
    }
    if reason is not None:
        error["reason"] = reason
    return _json_envelope("send", ok=False, error=error)


def _write_send_input_error(*, json_output: bool) -> int:
    if json_output:
        _write_json(_send_error_payload("invalid_input"))
    else:
        sys.stderr.write("Invalid input. Pass one send request as JSON on standard input.\n")
    return _INVALID_INPUT


def _write_send_success(*, json_output: bool, outcome: str) -> int:
    if json_output:
        _write_json(_send_success_payload(outcome))
    elif outcome == "validated":
        sys.stdout.write("Request is valid. No message was sent.\n")
    else:
        sys.stdout.write("Send request completed. Delivery is not confirmed.\n")
    return _SUCCESS


def _write_send_failure(
    *,
    json_output: bool,
    reason: MessageFailureReason,
) -> int:
    if json_output:
        _write_json(_send_error_payload(f"{reason}_failed", reason=reason))
    else:
        sys.stderr.write(
            f"The send failed or could not be confirmed: {reason}_failed. "
            "Do not retry automatically.\n"
        )
    return _SEND_FAILED


def _run_send(*, json_output: bool, dry_run: bool) -> int:
    try:
        request = _read_send_request()
    except _InvalidSendInputError:
        return _write_send_input_error(json_output=json_output)

    if dry_run:
        return _write_send_success(json_output=json_output, outcome="validated")

    try:
        client = IMessageClient()
        client.send_request(request)
    except MessageSendError as error:
        reason = error.reason
    except ScriptNotFoundError:
        reason = "transport"
    else:
        return _write_send_success(
            json_output=json_output,
            outcome="transport_completed",
        )

    return _write_send_failure(json_output=json_output, reason=reason)


def _run_skills_list(*, json_output: bool) -> int:
    try:
        skills = list_skills()
    except AgentSkillResourceError:
        if json_output:
            _write_json(
                _json_envelope(
                    "skills.list",
                    ok=False,
                    error={"code": "skill_unavailable", "retryable": False},
                )
            )
        else:
            sys.stderr.write("Bundled Agent Skill content is unavailable.\n")
        return _SEND_FAILED

    if json_output:
        _write_json(
            _json_envelope(
                "skills.list",
                ok=True,
                data={"skills": [skill.to_dict() for skill in skills]},
            )
        )
    else:
        for skill in skills:
            sys.stdout.write(f"{skill.name}\t{skill.description}\n")
    return _SUCCESS


def _run_skills_get(name: str) -> int:
    try:
        skill = load_skill(name)
    except AgentSkillResourceError:
        sys.stderr.write("Bundled Agent Skill content is unavailable.\n")
        return _SEND_FAILED

    sys.stdout.write(skill.content)
    if not skill.content.endswith("\n"):
        sys.stdout.write("\n")
    return _SUCCESS


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command line and return a process exit code."""
    parser = _build_parser()
    arguments = parser.parse_args(argv)

    if arguments.command == "doctor":
        report = diagnose_environment()
        if arguments.json_output:
            _write_json(_doctor_json_payload(report))
        else:
            _write_doctor_text(report)
        return _SEND_FAILED if report.blocked else _SUCCESS

    if arguments.command == "send":
        return _run_send(
            json_output=arguments.json_output,
            dry_run=arguments.dry_run,
        )

    if arguments.command == "skills":
        if arguments.skill_command in {None, "list"}:
            return _run_skills_list(json_output=arguments.json_output)
        return _run_skills_get(arguments.name)

    parser.print_help()
    return _SUCCESS


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
