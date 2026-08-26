from __future__ import annotations

from typing import TYPE_CHECKING, cast

import pytest

from macpymessenger.exceptions import TemplateNotFoundError, TemplateTypeError

if TYPE_CHECKING:
    from collections.abc import Callable
    from string.templatelib import Template

    from macpymessenger import TemplateManager


class FalseyContext(dict[str, object]):
    def __bool__(self) -> bool:
        return False


def test_template_formats_non_string_values(template_manager: TemplateManager) -> None:
    template_manager.create_template("count", lambda count: t"Count: {count}")

    assert template_manager.render_template("count", context={"count": 123}) == "Count: 123"


def test_template_applies_conversion(template_manager: TemplateManager) -> None:
    template_manager.create_template("greeting", lambda name: t"Hello, {name!r}!")

    assert (
        template_manager.render_template("greeting", context={"name": "Ada"})
        == "Hello, 'Ada'!"
    )


def test_template_applies_conversion_to_non_string_values(
    template_manager: TemplateManager,
) -> None:
    template_manager.create_template("count", lambda count: t"Count: {count!s}")

    assert template_manager.render_template("count", context={"count": 123}) == "Count: 123"


def test_template_applies_string_format_spec(template_manager: TemplateManager) -> None:
    template_manager.create_template("greeting", lambda name: t"[{name:>5}]")

    assert template_manager.render_template("greeting", context={"name": "Ada"}) == "[  Ada]"


def test_template_applies_numeric_format_spec(template_manager: TemplateManager) -> None:
    template_manager.create_template("total", lambda total: t"Total: {total:.2f}")

    assert template_manager.render_template("total", context={"total": 3.5}) == "Total: 3.50"


def test_template_preserves_a_falsey_mapping_context(template_manager: TemplateManager) -> None:
    template_manager.create_template("greeting", lambda name: t"Hello, {name}!")

    assert (
        template_manager.render_template(
            "greeting",
            context=FalseyContext(name="Ada"),
        )
        == "Hello, Ada!"
    )


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
