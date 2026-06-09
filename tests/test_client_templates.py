from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from macpymessenger.exceptions import TemplateNotFoundError

if TYPE_CHECKING:
    from macpymessenger import IMessageClient, TemplateManager
    from tests.support import StubRunner


def test_send_template_renders_content(
    client: tuple[IMessageClient, StubRunner], template_manager: TemplateManager
) -> None:
    instance, runner = client
    template_manager.create_template(
        "greeting",
        lambda name: t"Hello, {name}!",
    )
    instance.send_template("1234567890", "greeting", {"name": "Ada"})
    assert "Hello, Ada!" in runner.commands[-1]


def test_send_template_missing_template_raises(
    client: tuple[IMessageClient, StubRunner],
) -> None:
    instance, _ = client
    with pytest.raises(TemplateNotFoundError):
        instance.send_template("1234567890", "unknown")
