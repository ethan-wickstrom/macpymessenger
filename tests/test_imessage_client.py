import subprocess
from pathlib import Path
from typing import List, Sequence

import pytest

from macpymessenger import Configuration, IMessageClient, TemplateManager
from macpymessenger.exceptions import (
    DuplicateTemplateIdentifierError,
    MessageSendError,
    TemplateNotFoundError,
)


class StubRunner:
    def __init__(self, failing_phone_numbers: Sequence[str] | None = None) -> None:
        self.commands: List[List[str]] = []
        if failing_phone_numbers is None:
            self.failing_numbers = set()
        else:
            self.failing_numbers = set(failing_phone_numbers)

    def __call__(self, command: Sequence[str]) -> None:
        arguments = list(command)
        self.commands.append(arguments)
        phone_number = arguments[2]
        if phone_number in self.failing_numbers:
            raise subprocess.CalledProcessError(returncode=1, cmd=arguments)


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
def client(configuration: Configuration, template_manager: TemplateManager) -> tuple[IMessageClient, StubRunner]:
    runner = StubRunner()
    client_instance = IMessageClient(
        configuration=configuration,
        template_manager=template_manager,
        command_runner=runner,
    )
    return client_instance, runner


def test_send_message_success(client: tuple[IMessageClient, StubRunner]) -> None:
    instance, runner = client
    instance.send("1234567890", "Hello")
    assert runner.commands[0][2] == "1234567890"


def test_send_message_failure(client: tuple[IMessageClient, StubRunner]) -> None:
    instance, runner = client
    runner.failing_numbers.add("9876543210")
    with pytest.raises(MessageSendError):
        instance.send("9876543210", "Hello")


def test_send_message_rejects_negative_delay(client: tuple[IMessageClient, StubRunner]) -> None:
    instance, _ = client
    with pytest.raises(ValueError, match="Delay must be non-negative"):
        instance.send("1234567890", "Hello", delay_seconds=-1)


def test_send_template_renders_content(client: tuple[IMessageClient, StubRunner], template_manager: TemplateManager) -> None:
    instance, runner = client
    template_manager.create_template("greeting", "Hello, {{ name }}!")
    instance.send_template("1234567890", "greeting", {"name": "Ada"})
    assert "Hello, Ada!" in runner.commands[-1]


def test_send_template_missing_template_raises(
    client: tuple[IMessageClient, StubRunner],
) -> None:
    instance, _ = client
    with pytest.raises(TemplateNotFoundError):
        instance.send_template("1234567890", "unknown")

def test_update_and_delete_template(client: tuple[IMessageClient, StubRunner], template_manager: TemplateManager) -> None:
    instance, _ = client
    template_manager.create_template("greeting", "Hello")
    template_manager.update_template("greeting", "Hi")
    assert template_manager.render_template("greeting") == "Hi"
    template_manager.delete_template("greeting")
    with pytest.raises(TemplateNotFoundError):
        template_manager.render_template("greeting")

def test_update_nonexistent_template_raises(template_manager: TemplateManager) -> None:
    with pytest.raises(TemplateNotFoundError):
        template_manager.update_template("nonexistent", "Hi")


def test_delete_nonexistent_template_raises(template_manager: TemplateManager) -> None:
    with pytest.raises(TemplateNotFoundError):
        template_manager.delete_template("nonexistent")


def test_send_bulk_classifies_numbers(configuration: Configuration, template_manager: TemplateManager) -> None:
    runner = StubRunner(["2", "3"])
    client_instance = IMessageClient(
        configuration=configuration,
        template_manager=template_manager,
        command_runner=runner,
    )
    success, failure = client_instance.send_bulk(["1", "2", "3", "4"], "Ping")
    assert success == ["1", "4"]
    assert failure == ["2", "3"]


def test_send_bulk_with_no_numbers(
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


def test_load_directory_detects_duplicate_identifiers(tmp_path: Path) -> None:
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    (template_dir / "welcome.txt").write_text("Hello", encoding="utf-8")
    (template_dir / "welcome.j2").write_text("Hello again", encoding="utf-8")
    manager = TemplateManager()
    with pytest.raises(DuplicateTemplateIdentifierError):
        manager.load_directory(template_dir)
