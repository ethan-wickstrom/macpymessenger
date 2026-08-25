from __future__ import annotations

from macpymessenger import BulkSendResult, Configuration, IMessageClient, TemplateManager
from tests.support import StubRunner


def test_send_bulk_returns_named_immutable_outcomes(
    configuration: Configuration, template_manager: TemplateManager
) -> None:
    runner = StubRunner(["2", "3"])
    client = IMessageClient(
        configuration=configuration,
        template_manager=template_manager,
        command_runner=runner,
    )

    result = client.send_bulk(["1", "2", "3", "4"], "Ping")

    assert result == BulkSendResult(sent=("1", "4"), failed=("2", "3"))
    assert result.sent == ("1", "4")
    assert result.failed == ("2", "3")


def test_send_bulk_result_keeps_tuple_unpacking_compatibility(
    configuration: Configuration, template_manager: TemplateManager
) -> None:
    runner = StubRunner(["2"])
    client = IMessageClient(
        configuration=configuration,
        template_manager=template_manager,
        command_runner=runner,
    )

    sent, failed = client.send_bulk(["1", "2"], "Ping")

    assert sent == ("1",)
    assert failed == ("2",)


def test_send_bulk_handles_an_empty_recipient_list(
    configuration: Configuration, template_manager: TemplateManager
) -> None:
    client = IMessageClient(
        configuration=configuration,
        template_manager=template_manager,
        command_runner=StubRunner(),
    )

    assert client.send_bulk([], "Ping") == BulkSendResult(sent=(), failed=())


def test_send_bulk_can_classify_every_recipient_as_failed(
    configuration: Configuration, template_manager: TemplateManager
) -> None:
    client = IMessageClient(
        configuration=configuration,
        template_manager=template_manager,
        command_runner=StubRunner(["1", "2"]),
    )

    assert client.send_bulk(["1", "2"], "Ping") == BulkSendResult(
        sent=(),
        failed=("1", "2"),
    )
