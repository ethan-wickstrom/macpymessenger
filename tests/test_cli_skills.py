from __future__ import annotations

import json
import re
from importlib.resources import files
from pathlib import Path

import pytest

import macpymessenger.__main__ as cli
from macpymessenger import __version__, agent_skills
from macpymessenger.agent_skills import AgentSkillResourceError, load_skill

MAX_SKILL_NAME_LENGTH = 64
MAX_SKILL_DESCRIPTION_LENGTH = 1024


def _skill_content(name: str, description: str) -> str:
    return f"---\nname: {name}\ndescription: {description}\n---\n\n# Test skill\n"


def test_skills_list_json_exposes_a_small_versioned_catalog(
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code = cli.main(["skills", "list", "--json"])
    payload = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert payload == {
        "schema_version": 1,
        "tool": "macpymessenger",
        "command": "skills.list",
        "version": __version__,
        "ok": True,
        "data": {
            "skills": [
                {
                    "name": "core",
                    "description": (
                        "Use this skill when the user explicitly asks an agent to send an "
                        "iMessage through the local macOS Messages app or inspect "
                        "macpymessenger readiness."
                    ),
                }
            ]
        },
    }


def test_bare_skills_lists_the_catalog(
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code = cli.main(["skills"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert output.startswith("core\t")
    assert "Use this skill when the user explicitly asks" in output


def test_top_level_help_routes_agents_to_the_installed_core_skill(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["--help"])

    output = capsys.readouterr().out
    assert exc_info.value.code == 0
    assert "Start here for AI agents:" in output
    assert "macpymessenger skills get core" in output
    assert "version-matched" in output


def test_skills_get_core_returns_installed_version_matched_instructions(
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code = cli.main(["skills", "get", "core"])
    content = capsys.readouterr().out

    assert exit_code == 0
    assert content.startswith("---\nname: core\n")
    assert "macpymessenger doctor --json" in content
    assert "macpymessenger send --json" in content
    assert "explicitly asks" in content
    assert "process arguments, environment variables, and temporary files" in content
    assert "shell history" not in content
    assert "MCP" not in content


def test_core_skill_is_bundled_in_the_installed_package() -> None:
    resource = files("macpymessenger").joinpath("skills", "core", "SKILL.md")

    assert resource.is_file()


def test_core_skill_metadata_meets_agent_skills_constraints() -> None:
    skill = load_skill("core")

    assert len(skill.name) <= MAX_SKILL_NAME_LENGTH
    assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill.name)
    assert len(skill.description) <= MAX_SKILL_DESCRIPTION_LENGTH


@pytest.mark.parametrize(
    "name",
    [
        "Core",
        "-core",
        "core-",
        "core--send",
        "a" * 65,
    ],
)
def test_skill_parser_rejects_invalid_names(name: str) -> None:
    with pytest.raises(AgentSkillResourceError, match="invalid name"):
        agent_skills._parse_skill("core", _skill_content(name, "Use this skill for tests."))


def test_skill_parser_rejects_a_description_over_the_spec_limit() -> None:
    with pytest.raises(AgentSkillResourceError, match="description exceeds"):
        agent_skills._parse_skill("core", _skill_content("core", "a" * 1025))


def test_skill_parser_rejects_a_directory_name_mismatch() -> None:
    with pytest.raises(AgentSkillResourceError, match="declares name"):
        agent_skills._parse_skill(
            "core",
            _skill_content("other-skill", "Use this skill for tests."),
        )


def test_repository_skill_stub_defers_to_installed_cli_content() -> None:
    content = Path(".agents/skills/macpymessenger/SKILL.md").read_text(encoding="utf-8")

    assert content.startswith("---\nname: macpymessenger\n")
    assert "macpymessenger skills get core" in content
    assert "discovery stub" in content
