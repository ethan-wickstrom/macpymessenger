"""Command-line entry point for macpymessenger diagnostics."""

from __future__ import annotations

import argparse
import json
import sys
from typing import TYPE_CHECKING

from . import __version__
from .diagnostics import EnvironmentReport, diagnose_environment

if TYPE_CHECKING:
    from collections.abc import Sequence


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="macpymessenger",
        description="Send iMessages from Python on macOS.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
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
    return parser


def _json_payload(report: EnvironmentReport) -> dict[str, object]:
    payload = report.to_dict()
    return {
        "tool": "macpymessenger-doctor",
        "version": __version__,
        **payload,
    }


def _write_text(report: EnvironmentReport) -> None:
    sys.stdout.write(f"macpymessenger {__version__}\n\n")
    for check in report.checks:
        sys.stdout.write(f"{check.status.value.upper()} {check.identifier}: {check.summary}\n")
        if check.next_step is not None:
            sys.stdout.write(f"  Next: {check.next_step}\n")

    if report.blocked:
        summary = "Local blockers must be fixed before sending."
    else:
        summary = "No detectable local blockers. Complete the MANUAL checks before sending."
    sys.stdout.write(f"\n{summary}\n")


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command line and return a process exit code."""
    parser = _build_parser()
    arguments = parser.parse_args(argv)

    if arguments.command != "doctor":
        parser.print_help()
        return 0

    report = diagnose_environment()
    if arguments.json_output:
        json.dump(_json_payload(report), sys.stdout, sort_keys=True)
        sys.stdout.write("\n")
    else:
        _write_text(report)
    return 1 if report.blocked else 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
