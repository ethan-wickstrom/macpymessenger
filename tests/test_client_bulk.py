from __future__ import annotations

from macpymessenger import BulkSendResult, IMessageClient, SendRequest
from tests.support import StubTransport


class MutatingTransport:
    def __init__(self, source: list[str]) -> None:
        self.source = source
        self.requests: list[SendRequest] = []

    def send(self, request: SendRequest) -> None:
        self.requests.append(request)
        if len(self.requests) == 1:
            self.source[:] = ["replacement"]


def test_send_bulk_returns_named_immutable_outcomes() -> None:
    transport = StubTransport(["2", "3"])
    client = IMessageClient(transport=transport)

    result = client.send_bulk(["1", "2", "3", "4"], "Ping")

    assert result == BulkSendResult(sent=("1", "4"), failed=("2", "3"))
    assert result.sent == ("1", "4")
    assert result.failed == ("2", "3")


def test_send_bulk_result_keeps_tuple_unpacking_compatibility() -> None:
    client = IMessageClient(transport=StubTransport(["2"]))

    sent, failed = client.send_bulk(["1", "2"], "Ping")

    assert sent == ("1",)
    assert failed == ("2",)


def test_send_bulk_handles_an_empty_recipient_list() -> None:
    client = IMessageClient(transport=StubTransport())

    assert client.send_bulk([], "Ping") == BulkSendResult(sent=(), failed=())


def test_send_bulk_can_classify_every_recipient_as_failed() -> None:
    client = IMessageClient(transport=StubTransport(["1", "2"]))

    assert client.send_bulk(["1", "2"], "Ping") == BulkSendResult(
        sent=(),
        failed=("1", "2"),
    )


def test_send_bulk_snapshots_caller_input_before_the_first_send() -> None:
    recipients = ["first", "second"]
    transport = MutatingTransport(recipients)
    client = IMessageClient(transport=transport)

    result = client.send_bulk(recipients, "Ping")

    assert result == BulkSendResult(sent=("first", "second"), failed=())
    assert [request.recipient for request in transport.requests] == ["first", "second"]


def test_send_bulk_accepts_a_one_pass_iterable() -> None:
    client = IMessageClient(transport=StubTransport())
    recipients = (str(index) for index in range(3))

    result = client.send_bulk(recipients, "Ping")

    assert result == BulkSendResult(sent=("0", "1", "2"), failed=())
