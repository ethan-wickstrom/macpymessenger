from __future__ import annotations

from typing import TYPE_CHECKING, cast

import pytest

from macpymessenger.exceptions import TemplateNotFoundError, TemplateTypeError

if TYPE_CHECKING:
    from collections.abc import Callable
    from string.templatelib import Template

    from macpymessenger import TemplateManager


def test_template_non_string_value_raises(template_manager: TemplateManager) -> None:
    template_manager.create_template("greeting", lambda name: t"Hello, {name}!")
    context: dict[str, object] = {"name": 123}
    with pytest.raises(
        TemplateTypeError, match=r"Interpolation 'name' resolved to int; expected str"
    ):
        template_manager.render_template("greeting", context=context)


def test_template_applies_conversion(template_manager: TemplateManager) -> None:
    template_manager.create_template("greeting", lambda name: t"Hello, {name!r}!")
    assert template_manager.render_template("greeting", context={"name": "Ada"}) == "Hello, 'Ada'!"


def test_template_applies_format_spec(template_manager: TemplateManager) -> None:
    template_manager.create_template("greeting", lambda name: t"[{name:>5}]")
    assert template_manager.render_template("greeting", context={"name": "Ada"}) == "[  Ada]"


def test_template_conversion_does_not_bypass_type_check(
    template_manager: TemplateManager,
) -> None:
    template_manager.create_template("count", lambda count: t"Count: {count!s}")
    context: dict[str, object] = {"count": 123}
    with pytest.raises(
        TemplateTypeError, match=r"Interpolation 'count' resolved to int; expected str"
    ):
        template_manager.render_template("count", context=context)


def test_template_factory_must_return_t_string(template_manager: TemplateManager) -> None:
    bad_factory = cast("Callable[..., Template]", lambda name: f"Hello, {name}!")
    template_manager.create_template("greeting", bad_factory)
    with pytest.raises(TemplateTypeError, match=r"must return a string\.templatelib\.Template"):
        template_manager.render_template("greeting", context={"name": "Ada"})


def test_update_and_delete_template(
    template_manager: TemplateManager,
) -> None:
    template_manager.create_template("greeting", lambda: t"Hello")
    template_manager.update_template("greeting", lambda: t"Hi")
    assert template_manager.render_template("greeting") == "Hi"
    template_manager.delete_template("greeting")
    with pytest.raises(TemplateNotFoundError):
        template_manager.render_template("greeting")


def test_update_nonexistent_template_raises(template_manager: TemplateManager) -> None:
    with pytest.raises(TemplateNotFoundError):
        template_manager.update_template("nonexistent", lambda: t"Hi")


def test_delete_nonexistent_template_raises(template_manager: TemplateManager) -> None:
    with pytest.raises(TemplateNotFoundError):
        template_manager.delete_template("nonexistent")
