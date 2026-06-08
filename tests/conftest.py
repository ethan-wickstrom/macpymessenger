from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from macpymessenger import Configuration, IMessageClient, TemplateManager
from tests.support import StubRunner

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture
def script_path(tmp_path: Path) -> Path:
    script = tmp_path / "send.scpt"
    script.write_text("-- test script", encoding="utf-8")
    return script


@pytest.fixture
def configuration(script_path: Path) -> Configuration:
    return Configuration(script_path)


@pytest.fixture
def template_manager() -> TemplateManager:
    return TemplateManager()


@pytest.fixture
def client(
    configuration: Configuration, template_manager: TemplateManager
) -> tuple[IMessageClient, StubRunner]:
    runner = StubRunner()
    client_instance = IMessageClient(
        configuration=configuration,
        template_manager=template_manager,
        command_runner=runner,
    )
    return client_instance, runner
