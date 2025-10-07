"""Template management utilities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Final, Mapping, MutableMapping, Optional, Set, cast

from jinja2 import DictLoader, Environment, TemplateError as JinjaTemplateError, TemplateNotFound, select_autoescape

from .exceptions import (
    DuplicateTemplateIdentifierError,
    TemplateAlreadyExistsError,
    TemplateError,
    TemplateNotFoundError,
)


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
        self._environment = Environment(
            loader=self._loader,
            autoescape=select_autoescape(enabled_extensions=("html", "xml", "j2", "txt")),
        )
        if template_dir is not None:
            self.load_directory(Path(template_dir))

    def load_directory(self, directory: Path) -> None:
        directory_path = directory
        if not directory_path.exists():
            raise TemplateNotFoundError(f"Template directory not found: {directory_path}")
        loaded_identifiers: Set[str] = set()
        for entry in directory_path.iterdir():
            if entry.is_file():
                suffix = entry.suffix.lower()
                if suffix in {".txt", ".j2"}:
                    identifier = entry.stem
                    if identifier in loaded_identifiers or identifier in self._definitions:
                        raise DuplicateTemplateIdentifierError(
                            f"Duplicate template identifier found: '{identifier}' in '{entry}'"
                        )
                    content = entry.read_text(encoding="utf-8")
                    self.create_template(identifier, content)
                    loaded_identifiers.add(identifier)

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
        self._invalidate_template_cache()
        return definition

    def get_template(self, identifier: str) -> TemplateDefinition:
        try:
            return self._definitions[identifier]
        except KeyError as error:
            raise TemplateNotFoundError(f"Template with ID '{identifier}' does not exist.") from error

    _UNSET: Final[object] = object()

    def update_template(
        self,
        identifier: str,
        new_content: str,
        parent_identifier: Optional[str] | object = _UNSET,
    ) -> TemplateDefinition:
        """Update an existing template's content and optionally its parent."""
        if identifier not in self._definitions:
            raise TemplateNotFoundError(f"Template with ID '{identifier}' does not exist.")
        old_definition = self._definitions[identifier]
        if parent_identifier is self._UNSET:
            new_parent = old_definition.parent_identifier
        else:
            new_parent = cast(Optional[str], parent_identifier)
        definition = TemplateDefinition(identifier, new_content, new_parent)
        self._definitions[identifier] = definition
        self._mapping[identifier] = new_content
        self._invalidate_template_cache()
        return definition

    def delete_template(self, identifier: str) -> None:
        if identifier not in self._definitions:
            raise TemplateNotFoundError(f"Template with ID '{identifier}' does not exist.")
        del self._definitions[identifier]
        if identifier in self._mapping:
            del self._mapping[identifier]
        self._invalidate_template_cache()

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
        """Return the rendered content for use in include-like contexts."""
        return self.render_template(identifier, context)

    def list_templates(self) -> Dict[str, TemplateDefinition]:
        return dict(self._definitions)

    def _invalidate_template_cache(self) -> None:
        cache = self._environment.cache
        if cache is not None:
            cache.clear()
