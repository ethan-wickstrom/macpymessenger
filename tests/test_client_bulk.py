from __future__ import annotations

from macpymessenger import Configuration, IMessageClient, TemplateManager
from tests.support import StubRunner


def test_send_bulk_classifies_recipient_handles(
    configuration: Configuration, template_manager: TemplateManager
) -> None:
    runner = StubRunner(["2", "3"])
    client_instance = IMessageClient(
        configuration=configuration,
        template_manager=template_manager,
        command_runner=runner,
    )
    success, failure = client_instance.send_bulk(["1", "2", "3", "4"], "Ping")
    assert success == ["1", "4"]
    assert failure == ["2", "3"]


def test_send_bulk_with_no_recipient_handles(
    configuration: Configuration, template_manager: TemplateManager
) -> None:
    runner = StubRunner()
    client_instance = IMessageClient(
        configuration=configuration,
        template_manager=template_manager,
        command_runner=runner,
    )
    success, failure = client_instance.send_bulk([], "Ping")
    assert success == []
    assert failure == []


def test_send_bulk_classifies_all_recipient_handles_as_failures(
    configuration: Configuration, template_manager: TemplateManager
) -> None:
    runner = StubRunner(["1", "2"])
    client_instance = IMessageClient(
        configuration=configuration,
        template_manager=template_manager,
        command_runner=runner,
    )
    success, failure = client_instance.send_bulk(["1", "2"], "Ping")
    assert success == []
    assert failure == ["1", "2"]
