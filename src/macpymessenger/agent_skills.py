"""Version-matched Agent Skills bundled with macpymessenger."""

from __future__ import annotations

import re
from dataclasses import dataclass
from importlib.resources import files
from typing import Final, Self

_SKILL_NAMES: Final = ("core",)
_MAX_SKILL_NAME_LENGTH: Final = 64
_MAX_SKILL_DESCRIPTION_LENGTH: Final = 1024
_SKILL_NAME_PATTERN: Final = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


class AgentSkillResourceError(RuntimeError):
    """Raised when an installed Agent Skill is missing or malformed."""

    @classmethod
    def unknown_skill(cls, name: str) -> Self:
        return cls(f"Unknown bundled Agent Skill: {name}")

    @classmethod
    def unavailable(cls, name: str) -> Self:
        return cls(f"Bundled Agent Skill is unavailable: {name}")

    @classmethod
    def invalid_name(cls, name: str) -> Self:
        return cls(f"Bundled Agent Skill has invalid name '{name}'")

    @classmethod
    def name_mismatch(cls, path_name: str, declared_name: str) -> Self:
        return cls(f"Bundled Agent Skill path '{path_name}' declares name '{declared_name}'")

    @classmethod
    def description_too_long(cls) -> Self:
        return cls(
            f"Bundled Agent Skill description exceeds {_MAX_SKILL_DESCRIPTION_LENGTH} characters"
        )

    @classmethod
    def missing_frontmatter(cls) -> Self:
        return cls("Bundled Agent Skill has no YAML frontmatter")

    @classmethod
    def unclosed_frontmatter(cls) -> Self:
        return cls("Bundled Agent Skill frontmatter is not closed")

    @classmethod
    def invalid_field(cls, key: str) -> Self:
        return cls(f"Bundled Agent Skill must declare one non-empty '{key}' field")


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
        raise AgentSkillResourceError.unknown_skill(name)

    resource = files("macpymessenger").joinpath("skills", name, "SKILL.md")
    try:
        content = resource.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise AgentSkillResourceError.unavailable(name) from error

    return _parse_skill(name, content)


def list_skills() -> tuple[AgentSkill, ...]:
    """Load the ordered catalog of bundled skills."""
    return tuple(load_skill(name) for name in _SKILL_NAMES)


def _parse_skill(path_name: str, content: str) -> AgentSkill:
    """Parse and validate one controlled bundled Agent Skill document."""
    declared_name = _frontmatter_value(content, "name")
    description = _frontmatter_value(content, "description")

    if (
        len(declared_name) > _MAX_SKILL_NAME_LENGTH
        or _SKILL_NAME_PATTERN.fullmatch(declared_name) is None
    ):
        raise AgentSkillResourceError.invalid_name(declared_name)
    if declared_name != path_name:
        raise AgentSkillResourceError.name_mismatch(path_name, declared_name)
    if len(description) > _MAX_SKILL_DESCRIPTION_LENGTH:
        raise AgentSkillResourceError.description_too_long()

    return AgentSkill(
        name=declared_name,
        description=description,
        content=content,
    )


def _frontmatter_value(content: str, key: str) -> str:
    """Read one required single-line scalar from controlled skill frontmatter."""
    lines = content.splitlines()
    if not lines or lines[0] != "---":
        raise AgentSkillResourceError.missing_frontmatter()

    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise AgentSkillResourceError.unclosed_frontmatter() from error

    prefix = f"{key}: "
    values = [line.removeprefix(prefix).strip() for line in lines[1:end] if line.startswith(prefix)]
    if len(values) != 1 or not values[0]:
        raise AgentSkillResourceError.invalid_field(key)
    return values[0]
