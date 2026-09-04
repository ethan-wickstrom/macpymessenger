from __future__ import annotations

import subprocess

from macpymessenger import (
    BulkSendFailure,
    BulkSendResult,
    IMessageClient,
    SendRequest,
)
from tests.support import StubTransport


class MutatingTransport:
    def __init__(self, source: list[str]) -> None:
        self.source = source
        self.requests: list[SendRequest] = []

    def send(self, request: SendRequest) -> None:
        self.requests.append(request)
        if len(self.requests) == 1:
            self.source[:] = ["replacement"]


class MixedFailureTransport:
    def __init__(self) -> None:
        self.requests: list[SendRequest] = []

    def send(self, request: SendRequest) -> None:
        self.requests.append(request)
        if request.recipient == "delivery":
            raise subprocess.CalledProcessError(
                returncode=1,
                cmd=["/usr/bin/osascript", "-"],
            )
        if request.recipient == "transport":
            message = "transport unavailable"
            raise OSError(message)


def test_send_bulk_returns_named_immutable_outcomes() -> None:
    transport = StubTransport(["2", "3"])
    client = IMessageClient(transport=transport)

    result = client.send_bulk(["1", "2", "3", "4"], "Ping")

    assert result == BulkSendResult(
        sent=("1", "4"),
        failures=(
            BulkSendFailure(recipient="2", reason="delivery"),
            BulkSendFailure(recipient="3", reason="delivery"),
        ),
    )
    assert result.sent == ("1", "4")
    assert result.failed == ("2", "3")
    assert result.ok is False


def test_send_bulk_preserves_each_failure_reason_in_input_order() -> None:
    client = IMessageClient(transport=MixedFailureTransport())

    result = client.send_bulk(["delivery", "sent", "transport"], "Ping")

    assert result.failures == (
        BulkSendFailure(recipient="delivery", reason="delivery"),
        BulkSendFailure(recipient="transport", reason="transport"),
    )
    assert result.failed == ("delivery", "transport")


def test_send_bulk_result_keeps_tuple_unpacking_compatibility() -> None:
    client = IMessageClient(transport=StubTransport(["2"]))

    sent, failed = client.send_bulk(["1", "2"], "Ping")

    assert sent == ("1",)
    assert failed == ("2",)


def test_send_bulk_handles_an_empty_recipient_list() -> None:
    client = IMessageClient(transport=StubTransport())

    result = client.send_bulk([], "Ping")

    assert result == BulkSendResult(sent=(), failures=())
    assert result.failed == ()
    assert result.ok is True


def test_send_bulk_can_classify_every_recipient_as_failed() -> None:
    client = IMessageClient(transport=StubTransport(["1", "2"]))

    assert client.send_bulk(["1", "2"], "Ping") == BulkSendResult(
        sent=(),
        failures=(
            BulkSendFailure(recipient="1", reason="delivery"),
            BulkSendFailure(recipient="2", reason="delivery"),
        ),
    )


def test_send_bulk_snapshots_caller_input_before_the_first_send() -> None:
    recipients = ["first", "second"]
    transport = MutatingTransport(recipients)
    client = IMessageClient(transport=transport)

    result = client.send_bulk(recipients, "Ping")

    assert result == BulkSendResult(sent=("first", "second"), failures=())
    assert [request.recipient for request in transport.requests] == ["first", "second"]


def test_send_bulk_accepts_a_one_pass_iterable() -> None:
    client = IMessageClient(transport=StubTransport())
    recipients = (str(index) for index in range(3))

    result = client.send_bulk(recipients, "Ping")

    assert result == BulkSendResult(sent=("0", "1", "2"), failures=())
