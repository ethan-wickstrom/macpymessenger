"""Command-line entry point for macpymessenger."""

from __future__ import annotations

import argparse
import json
import sys
from typing import TYPE_CHECKING, Final

from . import __version__
from .agent_skills import AgentSkillResourceError, list_skills, load_skill, skill_names
from .client import IMessageClient
from .diagnostics import EnvironmentReport, diagnose_environment
from .exceptions import (
    InvalidDelayTypeError,
    MacPyMessengerError,
    MessageSendError,
    NegativeDelayError,
)
from .transport import SendRequest

if TYPE_CHECKING:
    from collections.abc import Sequence

_SUCCESS: Final = 0
_SEND_FAILED: Final = 1
_INVALID_INPUT: Final = 2
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
        description="Send iMessages from Python on macOS.",
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
    skill_commands = skills.add_subparsers(dest="skill_command", required=True)
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


def _doctor_json_payload(report: EnvironmentReport) -> dict[str, object]:
    payload = report.to_dict()
    return {
        "tool": "macpymessenger-doctor",
        "version": __version__,
        **payload,
    }


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


def _read_send_request() -> SendRequest:
    try:
        payload: object = json.load(sys.stdin)
    except json.JSONDecodeError, OSError, RecursionError, UnicodeError:
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

    recipient = fields["recipient"]
    message = fields["message"]
    delay_seconds = fields.get("delay_seconds", 0)
    if not isinstance(recipient, str) or not isinstance(message, str):
        raise _InvalidSendInputError

    try:
        return SendRequest(
            recipient=recipient,
            message=message,
            delay_seconds=delay_seconds,
        )
    except InvalidDelayTypeError, NegativeDelayError:
        raise _InvalidSendInputError from None


def _send_result_payload(
    *,
    ok: bool,
    reason: str | None = None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "tool": "macpymessenger-send",
        "version": __version__,
        "ok": ok,
    }
    if reason is not None:
        payload["error"] = {
            "code": f"{reason}_failed",
            "reason": reason,
        }
    return payload


def _run_send(*, json_output: bool) -> int:
    try:
        request = _read_send_request()
    except _InvalidSendInputError:
        if json_output:
            _write_json(
                {
                    "tool": "macpymessenger-send",
                    "version": __version__,
                    "ok": False,
                    "error": {"code": "invalid_input"},
                }
            )
        else:
            sys.stderr.write("Invalid input. Pass one send request as JSON on standard input.\n")
        return _INVALID_INPUT

    try:
        client = IMessageClient()
        client.send(
            request.recipient,
            request.message,
            delay_seconds=request.delay_seconds,
        )
    except MessageSendError as error:
        reason = error.reason
    except MacPyMessengerError:
        reason = "transport"
    else:
        if json_output:
            _write_json(_send_result_payload(ok=True))
        else:
            sys.stdout.write("Message sent.\n")
        return _SUCCESS

    if json_output:
        _write_json(_send_result_payload(ok=False, reason=reason))
    else:
        sys.stderr.write(f"Message was not sent: {reason}_failed.\n")
    return _SEND_FAILED


def _run_skills_list(*, json_output: bool) -> int:
    try:
        skills = list_skills()
    except AgentSkillResourceError:
        if json_output:
            _write_json(
                {
                    "tool": "macpymessenger-skills",
                    "version": __version__,
                    "error": {"code": "skill_unavailable"},
                }
            )
        else:
            sys.stderr.write("Bundled Agent Skill content is unavailable.\n")
        return _SEND_FAILED

    if json_output:
        _write_json(
            {
                "tool": "macpymessenger-skills",
                "version": __version__,
                "skills": [skill.to_dict() for skill in skills],
            }
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
        return _run_send(json_output=arguments.json_output)

    if arguments.command == "skills":
        if arguments.skill_command == "list":
            return _run_skills_list(json_output=arguments.json_output)
        return _run_skills_get(arguments.name)

    parser.print_help()
    return _SUCCESS


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
