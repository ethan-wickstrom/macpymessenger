"""Template management utilities leveraging Python 3.14 t-strings."""

from __future__ import annotations

from collections.abc import Callable, Mapping, MutableMapping
from dataclasses import dataclass
from string.templatelib import Interpolation, Template, convert

from .exceptions import TemplateAlreadyExistsError, TemplateNotFoundError, TemplateTypeError

TemplateCallable = Callable[..., Template]


@dataclass(frozen=True, slots=True)
class RenderedTemplate:
    """Represents a rendered template instance."""

    identifier: str
    content: str


def _process_template(template: Template) -> str:
    """Render a t-string Template object ensuring all interpolations are strings.

    Each interpolation must resolve to ``str``; its conversion (``!s``, ``!r``,
    ``!a``) and format spec (for example ``:>10``) are then applied.
    """

    parts: list[str] = []
    for item in template:
        match item:
            case str() as text:
                parts.append(text)
            case Interpolation(value, expression, conversion, format_spec):
                if not isinstance(value, str):
                    raise TemplateTypeError.non_string_interpolation(
                        expression, type(value).__name__
                    )
                parts.append(format(convert(value, conversion), format_spec))
            case _:
                raise TemplateTypeError.unexpected_element(type(item).__name__)
    return "".join(parts)


class TemplateManager:
    """Manages message templates using callables that return t-strings."""

    def __init__(self) -> None:
        self._templates: MutableMapping[str, TemplateCallable] = {}

    def create_template(self, identifier: str, factory: TemplateCallable) -> None:
        if identifier in self._templates:
            raise TemplateAlreadyExistsError.duplicate_identifier(identifier)
        self._templates[identifier] = factory

    def update_template(self, identifier: str, factory: TemplateCallable) -> None:
        if identifier not in self._templates:
            raise TemplateNotFoundError.missing_identifier(identifier)
        self._templates[identifier] = factory

    def delete_template(self, identifier: str) -> None:
        if identifier not in self._templates:
            raise TemplateNotFoundError.missing_identifier(identifier)
        del self._templates[identifier]

    def render_template(
        self,
        identifier: str,
        context: Mapping[str, object] | None = None,
    ) -> str:
        try:
            factory = self._templates[identifier]
        except KeyError as error:
            raise TemplateNotFoundError.missing_identifier(identifier) from error
        kwargs = dict(context) if context is not None else {}
        template = factory(**kwargs)
        if not isinstance(template, Template):
            raise TemplateTypeError.invalid_factory_return()
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
