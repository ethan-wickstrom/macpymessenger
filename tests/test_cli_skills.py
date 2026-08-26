from __future__ import annotations

import json
from importlib.resources import files
from pathlib import Path
from typing import TYPE_CHECKING

import macpymessenger.__main__ as cli
from macpymessenger import __version__

if TYPE_CHECKING:
    import pytest


def test_skills_list_json_exposes_a_small_versioned_catalog(
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code = cli.main(["skills", "list", "--json"])
    payload = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert payload["tool"] == "macpymessenger-skills"
    assert payload["version"] == __version__
    assert payload["skills"] == [
        {
            "name": "core",
            "description": (
                "Send text through the local macOS Messages app with the "
                "macpymessenger CLI. Use only when the user explicitly asks an "
                "agent to send an iMessage or check macpymessenger readiness."
            ),
        }
    ]


def test_skills_get_core_returns_installed_version_matched_instructions(
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code = cli.main(["skills", "get", "core"])
    content = capsys.readouterr().out

    assert exit_code == 0
    assert content.startswith("---\nname: core\n")
    assert "macpymessenger doctor --json" in content
    assert "macpymessenger send --json" in content
    assert "explicitly asked" in content
    assert "MCP" not in content


def test_core_skill_is_bundled_in_the_installed_package() -> None:
    resource = files("macpymessenger").joinpath("skills", "core", "SKILL.md")

    assert resource.is_file()


def test_repository_skill_stub_defers_to_installed_cli_content() -> None:
    content = Path(".agents/skills/macpymessenger/SKILL.md").read_text(encoding="utf-8")

    assert content.startswith("---\nname: macpymessenger\n")
    assert "macpymessenger skills get core" in content
    assert "discovery stub" in content
