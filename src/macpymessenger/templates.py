"""Template storage and rendering with Python 3.14 t-strings."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from string.templatelib import Interpolation, Template, convert

from .exceptions import TemplateAlreadyExistsError, TemplateNotFoundError, TemplateTypeError

TemplateCallable = Callable[..., Template]

__all__ = ["TemplateCallable", "TemplateManager"]


def _process_template(template: Template) -> str:
    """Render ``template`` with Python's conversion and format protocols."""
    parts: list[str] = []
    for item in template:
        match item:
            case str() as text:
                parts.append(text)
            case Interpolation(
                value=value,
                conversion=conversion,
                format_spec=format_spec,
            ):
                parts.append(format(convert(value, conversion), format_spec))
    return "".join(parts)


class TemplateManager:
    """Register and render callable t-string templates."""

    __slots__ = ("_templates",)

    def __init__(self) -> None:
        self._templates: dict[str, TemplateCallable] = {}

    def create_template(self, identifier: str, factory: TemplateCallable) -> None:
        """Register ``factory`` under a new identifier."""
        if identifier in self._templates:
            raise TemplateAlreadyExistsError.duplicate_identifier(identifier)
        self._templates[identifier] = factory

    def update_template(self, identifier: str, factory: TemplateCallable) -> None:
        """Replace an existing template factory."""
        if identifier not in self._templates:
            raise TemplateNotFoundError.missing_identifier(identifier)
        self._templates[identifier] = factory

    def delete_template(self, identifier: str) -> None:
        """Delete an existing template factory."""
        if identifier not in self._templates:
            raise TemplateNotFoundError.missing_identifier(identifier)
        del self._templates[identifier]

    def render_template(
        self,
        identifier: str,
        context: Mapping[str, object] | None = None,
    ) -> str:
        """Render a registered template with keyword values from ``context``."""
        try:
            factory = self._templates[identifier]
        except KeyError as error:
            raise TemplateNotFoundError.missing_identifier(identifier) from error

        kwargs = {} if context is None else dict(context)
        template = factory(**kwargs)
        if not isinstance(template, Template):
            raise TemplateTypeError.invalid_factory_return()
        return _process_template(template)

    def list_templates(self) -> dict[str, TemplateCallable]:
        """Return a shallow copy of the registered template mapping."""
        return dict(self._templates)
