"""Template management utilities leveraging Python 3.14 t-strings."""

from __future__ import annotations

from collections.abc import Callable, Mapping, MutableMapping
from dataclasses import dataclass

from string.templatelib import Interpolation, Template

from .exceptions import TemplateAlreadyExistsError, TemplateNotFoundError, TemplateTypeError


TemplateCallable = Callable[..., Template]


@dataclass(frozen=True, slots=True)
class RenderedTemplate:
    """Represents a rendered template instance."""

    identifier: str
    content: str


def _process_template(template: Template) -> str:
    """Render a t-string Template object ensuring all interpolations are strings."""

    parts: list[str] = []
    for item in template:
        if isinstance(item, str):
            parts.append(item)
            continue
        if isinstance(item, Interpolation):
            value = item.value
            if not isinstance(value, str):
                raise TemplateTypeError(
                    f"Interpolation '{item.expression}' resolved to "
                    f"{type(value).__name__}; expected str"
                )
            parts.append(value)
            continue
        raise TemplateTypeError(f"Unexpected template element of type {type(item).__name__}")
    return "".join(parts)


class TemplateManager:
    """Manages message templates using callables that return t-strings."""

    def __init__(self) -> None:
        self._templates: MutableMapping[str, TemplateCallable] = {}

    def create_template(self, identifier: str, factory: TemplateCallable) -> None:
        if identifier in self._templates:
            raise TemplateAlreadyExistsError(f"Template with ID '{identifier}' already exists.")
        self._templates[identifier] = factory

    def update_template(self, identifier: str, factory: TemplateCallable) -> None:
        if identifier not in self._templates:
            raise TemplateNotFoundError(f"Template with ID '{identifier}' does not exist.")
        self._templates[identifier] = factory

    def delete_template(self, identifier: str) -> None:
        if identifier not in self._templates:
            raise TemplateNotFoundError(f"Template with ID '{identifier}' does not exist.")
        del self._templates[identifier]

    def render_template(
        self,
        identifier: str,
        context: Mapping[str, object] | None = None,
    ) -> str:
        try:
            factory = self._templates[identifier]
        except KeyError as error:
            raise TemplateNotFoundError(
                f"Template with ID '{identifier}' does not exist."
            ) from error
        kwargs = dict(context) if context is not None else {}
        template = factory(**kwargs)
        return _process_template(template)

    def compose_template(
        self,
        identifier: str,
        context: Mapping[str, object] | None = None,
    ) -> RenderedTemplate:
        return RenderedTemplate(
            identifier=identifier,
            content=self.render_template(identifier, context),
        )

    def list_templates(self) -> dict[str, TemplateCallable]:
        return dict(self._templates)
