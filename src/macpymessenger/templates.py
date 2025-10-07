"""Template management utilities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Mapping, MutableMapping, Optional

from jinja2 import DictLoader, Environment, TemplateError as JinjaTemplateError, TemplateNotFound

from .exceptions import TemplateAlreadyExistsError, TemplateError, TemplateNotFoundError


@dataclass(frozen=True, slots=True)
class TemplateDefinition:
    """Represents a stored template definition."""

    identifier: str
    content: str
    parent_identifier: Optional[str] = None


@dataclass(frozen=True, slots=True)
class RenderedTemplate:
    """Represents a rendered template instance."""

    identifier: str
    content: str


class TemplateManager:
    """Manages message templates backed by Jinja2."""

    def __init__(self, template_dir: Optional[Path | str] = None) -> None:
        self._definitions: Dict[str, TemplateDefinition] = {}
        self._mapping: MutableMapping[str, str] = {}
        self._loader = DictLoader(self._mapping)
        self._environment = Environment(loader=self._loader, autoescape=True)
        if template_dir is not None:
            self.load_directory(Path(template_dir))

    def load_directory(self, directory: Path) -> None:
        directory_path = directory
        if not directory_path.exists():
            raise TemplateNotFoundError(f"Template directory not found: {directory_path}")
        for entry in directory_path.iterdir():
            if entry.is_file():
                suffix = entry.suffix
                if suffix == ".txt" or suffix == ".j2":
                    content = entry.read_text(encoding="utf-8")
                    identifier = entry.stem
                    if identifier not in self._definitions:
                        self.create_template(identifier, content)

    def create_template(
        self,
        identifier: str,
        content: str,
        parent_identifier: Optional[str] = None,
    ) -> TemplateDefinition:
        if identifier in self._definitions:
            raise TemplateAlreadyExistsError(f"Template with ID '{identifier}' already exists.")
        definition = TemplateDefinition(identifier, content, parent_identifier)
        self._definitions[identifier] = definition
        self._mapping[identifier] = content
        return definition

    def get_template(self, identifier: str) -> TemplateDefinition:
        try:
            return self._definitions[identifier]
        except KeyError as error:
            raise TemplateNotFoundError(f"Template with ID '{identifier}' does not exist.") from error

    def update_template(self, identifier: str, new_content: str) -> TemplateDefinition:
        if identifier not in self._definitions:
            raise TemplateNotFoundError(f"Template with ID '{identifier}' does not exist.")
        definition = TemplateDefinition(identifier, new_content, self._definitions[identifier].parent_identifier)
        self._definitions[identifier] = definition
        self._mapping[identifier] = new_content
        return definition

    def delete_template(self, identifier: str) -> None:
        if identifier not in self._definitions:
            raise TemplateNotFoundError(f"Template with ID '{identifier}' does not exist.")
        del self._definitions[identifier]
        if identifier in self._mapping:
            del self._mapping[identifier]

    def render_template(self, identifier: str, context: Optional[Mapping[str, object]] = None) -> str:
        try:
            template = self._environment.get_template(identifier)
        except TemplateNotFound as error:
            raise TemplateNotFoundError(f"Template with ID '{identifier}' does not exist.") from error
        context_mapping = dict(context) if context is not None else {}
        try:
            return template.render(**context_mapping)
        except JinjaTemplateError as error:
            raise TemplateError(f"Error rendering template '{identifier}': {error}") from error

    def compose_template(
        self,
        identifier: str,
        context: Optional[Mapping[str, object]] = None,
    ) -> RenderedTemplate:
        rendered_content = self.render_template(identifier, context)
        return RenderedTemplate(identifier=identifier, content=rendered_content)

    def include_template(self, identifier: str, context: Optional[Mapping[str, object]] = None) -> str:
        return self.render_template(identifier, context)

    def list_templates(self) -> Dict[str, TemplateDefinition]:
        return dict(self._definitions)
