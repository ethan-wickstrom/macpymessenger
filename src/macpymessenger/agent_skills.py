"""Version-matched Agent Skills bundled with macpymessenger."""

from __future__ import annotations

from dataclasses import dataclass
from importlib.resources import files
from typing import Final

_SKILL_NAMES: Final = ("core",)


class AgentSkillResourceError(RuntimeError):
    """Raised when an installed Agent Skill is missing or malformed."""


@dataclass(frozen=True, slots=True)
class AgentSkill:
    """One bundled Agent Skill and the metadata needed for discovery."""

    name: str
    description: str
    content: str

    def to_dict(self) -> dict[str, str]:
        """Return the stable catalog shape for this skill."""
        return {
            "name": self.name,
            "description": self.description,
        }


def skill_names() -> tuple[str, ...]:
    """Return the ordered names of all bundled skills."""
    return _SKILL_NAMES


def load_skill(name: str) -> AgentSkill:
    """Load one bundled skill and verify its required frontmatter."""
    if name not in _SKILL_NAMES:
        raise AgentSkillResourceError(f"Unknown bundled Agent Skill: {name}")

    resource = files("macpymessenger").joinpath("skills", name, "SKILL.md")
    try:
        content = resource.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise AgentSkillResourceError(f"Bundled Agent Skill is unavailable: {name}") from error

    declared_name = _frontmatter_value(content, "name")
    description = _frontmatter_value(content, "description")
    if declared_name != name:
        raise AgentSkillResourceError(
            f"Bundled Agent Skill path '{name}' declares name '{declared_name}'"
        )
    return AgentSkill(name=name, description=description, content=content)


def list_skills() -> tuple[AgentSkill, ...]:
    """Load the ordered catalog of bundled skills."""
    return tuple(load_skill(name) for name in _SKILL_NAMES)


def _frontmatter_value(content: str, key: str) -> str:
    """Read one required single-line scalar from controlled skill frontmatter."""
    lines = content.splitlines()
    if not lines or lines[0] != "---":
        raise AgentSkillResourceError("Bundled Agent Skill has no YAML frontmatter")

    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise AgentSkillResourceError("Bundled Agent Skill frontmatter is not closed") from error

    prefix = f"{key}: "
    values = [line.removeprefix(prefix).strip() for line in lines[1:end] if line.startswith(prefix)]
    if len(values) != 1 or not values[0]:
        raise AgentSkillResourceError(
            f"Bundled Agent Skill must declare one non-empty '{key}' field"
        )
    return values[0]
