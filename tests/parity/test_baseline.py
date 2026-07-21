"""Parity baseline: executable record of the incumbent's observable behavior.

Captured against commit 327762d before the rebuild and verified to pass
there. This file is the contract for the rebuild and is never edited to
make it pass. Intentional divergences live in test_divergences.py.
"""

from __future__ import annotations

import logging
import re
import subprocess
from typing import TYPE_CHECKING

import pytest

import macpymessenger
from macpymessenger import (
    Configuration,
    IMessageClient,
    SubprocessCommandRunner,
    TemplateManager,
)
from macpymessenger.exceptions import (
    ConfigurationError,
    InvalidDelayTypeError,
    MacPyMessengerError,
    MessageSendError,
    NegativeDelayError,
    ScriptNotFoundError,
    TemplateAlreadyExistsError,
    TemplateError,
    TemplateNotFoundError,
    TemplateTypeError,
)
from tests.support import StubRunner

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path
    from string.templatelib import Template


@pytest.fixture
def script_path(tmp_path: Path) -> Path:
    script = tmp_path / "send.scpt"
    script.write_text("-- test script", encoding="utf-8")
    return script


@pytest.fixture
def client(script_path: Path) -> tuple[IMessageClient, StubRunner]:
    runner = StubRunner()
    return IMessageClient(Configuration(script_path), command_runner=runner), runner


class TestConfiguration:
    def test_default_resolves_bundled_script(self) -> None:
        configuration = Configuration()
        assert configuration.send_script_path.name == "sendMessage.scpt"
        assert configuration.send_script_path.exists()

    def test_accepts_path_and_str(self, script_path: Path) -> None:
        assert Configuration(script_path).send_script_path == script_path
        assert Configuration(str(script_path)).send_script_path == script_path

    def test_missing_script_raises(self, tmp_path: Path) -> None:
        missing = tmp_path / "absent.scpt"
        with pytest.raises(ScriptNotFoundError, match=f"Send script not found at path: {missing}"):
            Configuration(missing)

    def test_repr(self, script_path: Path) -> None:
        assert repr(Configuration(script_path)) == f"Configuration(send_script_path={script_path})"


class TestSend:
    def test_send_builds_osascript_argv_command(
        self, client: tuple[IMessageClient, StubRunner], script_path: Path
    ) -> None:
        instance, runner = client
        result = instance.send("+15551234567", "Hello, world!")
        assert result is None
        assert runner.commands == [
            ["osascript", str(script_path), "+15551234567", "Hello, world!", "0"]
        ]

    def test_delay_is_forwarded_as_string(self, client: tuple[IMessageClient, StubRunner]) -> None:
        instance, runner = client
        instance.send("+15551234567", "later", delay_seconds=30)
        assert runner.commands[0][4] == "30"

    @pytest.mark.parametrize("bad_delay", [True, False, "5", 1.5, None])
    def test_non_int_delay_raises_typed_error(
        self, client: tuple[IMessageClient, StubRunner], bad_delay: object
    ) -> None:
        instance, _ = client
        expected = re.escape("Delay must be provided as an integer number of seconds.")
        with pytest.raises(InvalidDelayTypeError, match=expected):
            instance.send("+15551234567", "hi", bad_delay)  # ty: ignore[invalid-argument-type]

    def test_negative_delay_raises_typed_error(
        self, client: tuple[IMessageClient, StubRunner]
    ) -> None:
        instance, _ = client
        with pytest.raises(NegativeDelayError, match=re.escape("Delay must be non-negative.")):
            instance.send("+15551234567", "hi", -1)

    def test_invalid_delay_sends_nothing(self, client: tuple[IMessageClient, StubRunner]) -> None:
        instance, runner = client
        with pytest.raises(MacPyMessengerError):
            instance.send("+15551234567", "hi", -1)
        assert runner.commands == []

    def test_called_process_error_maps_to_message_send_error(self, script_path: Path) -> None:
        runner = StubRunner(failing_recipient_handles=["+15550000000"])
        instance = IMessageClient(Configuration(script_path), command_runner=runner)
        with pytest.raises(
            MessageSendError, match=r"Failed to send message to \+15550000000"
        ) as excinfo:
            instance.send("+15550000000", "hi")
        assert isinstance(excinfo.value.__cause__, subprocess.CalledProcessError)

    def test_os_error_maps_to_message_send_error(self, script_path: Path) -> None:
        def runner(command: object) -> None:  # noqa: ARG001
            reason = "boom"
            raise OSError(reason)

        instance = IMessageClient(Configuration(script_path), command_runner=runner)
        with pytest.raises(
            MessageSendError, match=r"Failed to execute osascript for \+15551234567"
        ) as excinfo:
            instance.send("+15551234567", "hi")
        assert isinstance(excinfo.value.__cause__, OSError)


class TestLogging:
    def test_success_logs_info_event(
        self,
        client: tuple[IMessageClient, StubRunner],
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        instance, _ = client
        with caplog.at_level(logging.INFO):
            instance.send("+15551234567", "hi")
        assert "Message sent to +15551234567" in caplog.text

    def test_failure_logs_exception_event(
        self, script_path: Path, caplog: pytest.LogCaptureFixture
    ) -> None:
        runner = StubRunner(failing_recipient_handles=["+15550000000"])
        instance = IMessageClient(Configuration(script_path), command_runner=runner)
        with caplog.at_level(logging.ERROR), pytest.raises(MessageSendError):
            instance.send("+15550000000", "hi")
        assert "Failed to send message to +15550000000" in caplog.text

    def test_injected_logger_receives_events(
        self, script_path: Path, caplog: pytest.LogCaptureFixture
    ) -> None:
        logger = logging.getLogger("parity.custom")
        instance = IMessageClient(
            Configuration(script_path), command_runner=StubRunner(), logger=logger
        )
        with caplog.at_level(logging.INFO, logger="parity.custom"):
            instance.send("+15551234567", "hi")
        assert "Message sent to +15551234567" in caplog.text


class TestTemplates:
    def test_create_render_and_send_template(
        self, client: tuple[IMessageClient, StubRunner]
    ) -> None:
        instance, runner = client

        def greeting(name: str) -> Template:
            return t"Hello, {name}!"

        instance.create_template("greeting", greeting)
        instance.send_template("+15551234567", "greeting", {"name": "Ada"})
        assert runner.commands[0][3] == "Hello, Ada!"

    def test_render_applies_conversion_and_format_spec(self) -> None:
        manager = TemplateManager()
        manager.create_template("fmt", lambda name: t"[{name!r:>10}]")
        assert manager.render_template("fmt", {"name": "Ada"}) == "[     'Ada']"

    def test_render_without_context(self) -> None:
        manager = TemplateManager()
        manager.create_template("static", lambda: t"no interpolation")
        assert manager.render_template("static") == "no interpolation"

    def test_non_string_interpolation_raises(self) -> None:
        manager = TemplateManager()
        manager.create_template("bad", lambda count: t"{count}")
        expected = re.escape("Interpolation 'count' resolved to int; expected str")
        with pytest.raises(TemplateTypeError, match=expected):
            manager.render_template("bad", {"count": 3})

    def test_non_template_factory_return_raises(self) -> None:
        manager = TemplateManager()
        manager.create_template("plain", lambda: "just a string")  # ty: ignore[invalid-argument-type]
        expected = re.escape(
            "Template factories must return a string.templatelib.Template instance."
        )
        with pytest.raises(TemplateTypeError, match=expected):
            manager.render_template("plain")

    def test_duplicate_create_raises(self) -> None:
        manager = TemplateManager()
        manager.create_template("dup", lambda: t"one")
        with pytest.raises(
            TemplateAlreadyExistsError, match=re.escape("Template with ID 'dup' already exists.")
        ):
            manager.create_template("dup", lambda: t"two")

    @pytest.mark.parametrize("operation", ["update", "delete", "render"])
    def test_missing_identifier_raises(self, operation: str) -> None:
        manager = TemplateManager()
        operations: dict[str, Callable[[], object]] = {
            "update": lambda: manager.update_template("ghost", lambda: t"x"),
            "delete": lambda: manager.delete_template("ghost"),
            "render": lambda: manager.render_template("ghost"),
        }
        with pytest.raises(
            TemplateNotFoundError, match=re.escape("Template with ID 'ghost' does not exist.")
        ):
            operations[operation]()

    def test_update_replaces_and_delete_removes(
        self, client: tuple[IMessageClient, StubRunner]
    ) -> None:
        instance, runner = client
        instance.create_template("note", lambda: t"first")
        instance.update_template("note", lambda: t"second")
        instance.send_template("+15551234567", "note")
        assert runner.commands[0][3] == "second"
        instance.delete_template("note")
        with pytest.raises(TemplateNotFoundError):
            instance.send_template("+15551234567", "note")

    def test_list_templates_returns_copy(self) -> None:
        manager = TemplateManager()
        manager.create_template("a", lambda: t"a")
        listing = manager.list_templates()
        listing.clear()
        assert manager.render_template("a") == "a"


class TestBulk:
    def test_send_bulk_partitions_successes_and_failures(self, script_path: Path) -> None:
        runner = StubRunner(failing_recipient_handles=["+15550000000"])
        instance = IMessageClient(Configuration(script_path), command_runner=runner)
        successful, failed = instance.send_bulk(
            ["+15551111111", "+15550000000", "+15552222222"], "hi"
        )
        assert successful == ["+15551111111", "+15552222222"]
        assert failed == ["+15550000000"]


class TestSubprocessRunner:
    def test_runs_real_command(self) -> None:
        SubprocessCommandRunner()(["true"])

    def test_nonzero_exit_raises_called_process_error(self) -> None:
        with pytest.raises(subprocess.CalledProcessError):
            SubprocessCommandRunner()(["false"])


class TestExceptionHierarchy:
    def test_hierarchy(self) -> None:
        assert issubclass(InvalidDelayTypeError, MacPyMessengerError)
        assert issubclass(InvalidDelayTypeError, TypeError)
        assert issubclass(NegativeDelayError, MacPyMessengerError)
        assert issubclass(NegativeDelayError, ValueError)
        assert issubclass(MessageSendError, MacPyMessengerError)
        assert issubclass(ScriptNotFoundError, ConfigurationError)
        assert issubclass(ConfigurationError, MacPyMessengerError)
        for template_error in (
            TemplateTypeError,
            TemplateNotFoundError,
            TemplateAlreadyExistsError,
        ):
            assert issubclass(template_error, TemplateError)
        assert issubclass(TemplateError, MacPyMessengerError)


class TestPublicSurface:
    def test_surviving_root_exports(self) -> None:
        for name in (
            "CommandRunner",
            "Configuration",
            "IMessageClient",
            "SubprocessCommandRunner",
            "TemplateManager",
        ):
            assert hasattr(macpymessenger, name)
