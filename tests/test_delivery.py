"""Focused tests for the delivery module."""

from __future__ import annotations

import logging
import subprocess
from typing import TYPE_CHECKING

import pytest

from macpymessenger import Configuration
from macpymessenger.delivery import MessageDelivery
from macpymessenger.exceptions import (
    InvalidDelayTypeError,
    MessageSendError,
    NegativeDelayError,
)
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
def delivery_logger() -> logging.Logger:
    return logging.getLogger("test.delivery")


@pytest.fixture
def delivery(
    configuration: Configuration,
    delivery_logger: logging.Logger,
) -> tuple[MessageDelivery, StubRunner]:
    runner = StubRunner()
    instance = MessageDelivery(
        configuration=configuration,
        command_runner=runner,
        logger=delivery_logger,
    )
    return instance, runner


# ---------------------------------------------------------------------------
# Delay validation
# ---------------------------------------------------------------------------


class TestValidateDelay:
    def test_accepts_zero(self) -> None:
        assert MessageDelivery._validate_delay(0) == 0

    def test_accepts_positive_int(self) -> None:
        delay = 30
        assert MessageDelivery._validate_delay(delay) == delay

    def test_rejects_bool(self) -> None:
        with pytest.raises(InvalidDelayTypeError):
            MessageDelivery._validate_delay(True)  # noqa: FBT003

    def test_rejects_float(self) -> None:
        with pytest.raises(InvalidDelayTypeError):
            MessageDelivery._validate_delay(1.5)

    def test_rejects_string(self) -> None:
        with pytest.raises(InvalidDelayTypeError):
            MessageDelivery._validate_delay("5")

    def test_rejects_none(self) -> None:
        with pytest.raises(InvalidDelayTypeError):
            MessageDelivery._validate_delay(None)

    def test_rejects_negative(self) -> None:
        with pytest.raises(NegativeDelayError):
            MessageDelivery._validate_delay(-1)


# ---------------------------------------------------------------------------
# Send command construction
# ---------------------------------------------------------------------------


class TestBuildCommand:
    def test_command_structure(
        self,
        delivery: tuple[MessageDelivery, StubRunner],
        script_path: Path,
    ) -> None:
        instance, _ = delivery
        command = instance._build_command("+10000000000", "Hello", 0)
        assert command[0] == "osascript"
        assert command[1] == str(script_path)
        assert command[2] == "+10000000000"
        assert command[3] == "Hello"
        assert command[4] == "0"

    def test_delay_value_serialized(
        self,
        delivery: tuple[MessageDelivery, StubRunner],
    ) -> None:
        instance, _ = delivery
        command = instance._build_command("+10000000000", "Hello", 60)
        assert command[4] == "60"

    def test_returns_list_of_strings(
        self,
        delivery: tuple[MessageDelivery, StubRunner],
    ) -> None:
        instance, _ = delivery
        command = instance._build_command("+10000000000", "Hello", 0)
        assert all(isinstance(segment, str) for segment in command)


# ---------------------------------------------------------------------------
# Command execution and failure mapping
# ---------------------------------------------------------------------------


class TestExecute:
    def test_success_calls_runner(
        self,
        delivery: tuple[MessageDelivery, StubRunner],
    ) -> None:
        instance, runner = delivery
        instance._execute("+10000000000", ["osascript", "send.scpt", "+10000000000", "hi", "0"])
        assert len(runner.commands) == 1

    def test_called_process_error_maps_to_delivery_failed(
        self,
        delivery: tuple[MessageDelivery, StubRunner],
    ) -> None:
        instance, runner = delivery
        runner.failing_recipient_handles.add("+19999999999")
        with pytest.raises(MessageSendError, match="Failed to send message to \\+19999999999"):
            instance._execute(
                "+19999999999",
                ["osascript", "send.scpt", "+19999999999", "hi", "0"],
            )

    def test_oserror_maps_to_command_failed(
        self,
        delivery: tuple[MessageDelivery, StubRunner],
        delivery_logger: logging.Logger,
    ) -> None:
        def raising_runner(command: object) -> None:  # noqa: ARG001
            msg = "exec failed"
            raise OSError(msg)

        instance = MessageDelivery(
            configuration=delivery[0]._configuration,
            command_runner=raising_runner,
            logger=delivery_logger,
        )
        with pytest.raises(MessageSendError, match="Failed to execute osascript"):
            instance._execute("+10000000000", ["osascript"])

    def test_success_logs_info(
        self,
        delivery: tuple[MessageDelivery, StubRunner],
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        instance, _ = delivery
        with caplog.at_level(logging.INFO, logger="test.delivery"):
            instance._execute(
                "+10000000000",
                ["osascript", "send.scpt", "+10000000000", "hi", "0"],
            )
        assert any("+10000000000" in record.message for record in caplog.records)

    def test_failure_logs_exception(
        self,
        delivery: tuple[MessageDelivery, StubRunner],
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        instance, runner = delivery
        runner.failing_recipient_handles.add("+19999999999")
        with (
            caplog.at_level(logging.ERROR, logger="test.delivery"),
            pytest.raises(MessageSendError),
        ):
                instance._execute(
                    "+19999999999",
                    ["osascript", "send.scpt", "+19999999999", "hi", "0"],
                )
        assert any("+19999999999" in record.message for record in caplog.records)


# ---------------------------------------------------------------------------
# deliver (full integration path through the delivery object)
# ---------------------------------------------------------------------------


class TestDeliver:
    def test_success_passes_correct_args_to_runner(
        self,
        delivery: tuple[MessageDelivery, StubRunner],
    ) -> None:
        instance, runner = delivery
        instance.deliver("+10000000000", "Hello")
        assert runner.commands[0][2] == "+10000000000"
        assert runner.commands[0][3] == "Hello"
        assert runner.commands[0][4] == "0"

    def test_delay_forwarded_to_command(
        self,
        delivery: tuple[MessageDelivery, StubRunner],
    ) -> None:
        instance, runner = delivery
        instance.deliver("+10000000000", "Hello", delay_seconds=5)
        assert runner.commands[0][4] == "5"

    def test_rejects_negative_delay(
        self,
        delivery: tuple[MessageDelivery, StubRunner],
    ) -> None:
        instance, _ = delivery
        with pytest.raises(NegativeDelayError):
            instance.deliver("+10000000000", "Hello", delay_seconds=-1)

    def test_rejects_bool_delay(
        self,
        delivery: tuple[MessageDelivery, StubRunner],
    ) -> None:
        instance, _ = delivery
        with pytest.raises(InvalidDelayTypeError):
            instance.deliver("+10000000000", "Hello", delay_seconds=True)

    def test_failing_recipient_raises_message_send_error(
        self,
        delivery: tuple[MessageDelivery, StubRunner],
    ) -> None:
        instance, runner = delivery
        runner.failing_recipient_handles.add("+19999999999")
        with pytest.raises(MessageSendError):
            instance.deliver("+19999999999", "Hello")

    def test_subprocess_called_process_error_is_chained(
        self,
        delivery: tuple[MessageDelivery, StubRunner],
    ) -> None:
        instance, runner = delivery
        runner.failing_recipient_handles.add("+19999999999")
        with pytest.raises(MessageSendError) as exc_info:
            instance.deliver("+19999999999", "Hello")
        assert isinstance(exc_info.value.__cause__, subprocess.CalledProcessError)
