from __future__ import annotations

from macpymessenger import BulkSendResult, IMessageClient, TemplateManager
from tests.support import StubTransport


def test_send_bulk_returns_named_immutable_outcomes(
    template_manager: TemplateManager,
) -> None:
    transport = StubTransport(["2", "3"])
    client = IMessageClient(
        template_manager=template_manager,
        transport=transport,
    )

    result = client.send_bulk(["1", "2", "3", "4"], "Ping")

    assert result == BulkSendResult(sent=("1", "4"), failed=("2", "3"))
    assert result.sent == ("1", "4")
    assert result.failed == ("2", "3")


def test_send_bulk_result_keeps_tuple_unpacking_compatibility(
    template_manager: TemplateManager,
) -> None:
    transport = StubTransport(["2"])
    client = IMessageClient(
        template_manager=template_manager,
        transport=transport,
    )

    sent, failed = client.send_bulk(["1", "2"], "Ping")

    assert sent == ("1",)
    assert failed == ("2",)


def test_send_bulk_handles_an_empty_recipient_list(
    template_manager: TemplateManager,
) -> None:
    client = IMessageClient(
        template_manager=template_manager,
        transport=StubTransport(),
    )

    assert client.send_bulk([], "Ping") == BulkSendResult(sent=(), failed=())


def test_send_bulk_can_classify_every_recipient_as_failed(
    template_manager: TemplateManager,
) -> None:
    client = IMessageClient(
        template_manager=template_manager,
        transport=StubTransport(["1", "2"]),
    )

    assert client.send_bulk(["1", "2"], "Ping") == BulkSendResult(
        sent=(),
        failed=("1", "2"),
    )
