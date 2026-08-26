from __future__ import annotations

import pytest

from macpymessenger import IMessageClient, TemplateManager
from tests.support import StubTransport


@pytest.fixture
def template_manager() -> TemplateManager:
    return TemplateManager()


@pytest.fixture
def client(
    template_manager: TemplateManager,
) -> tuple[IMessageClient, StubTransport]:
    transport = StubTransport()
    client_instance = IMessageClient(
        template_manager=template_manager,
        transport=transport,
    )
    return client_instance, transport
