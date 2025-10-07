"""The public messaging client."""

from __future__ import annotations

import logging
import subprocess
from dataclasses import dataclass, field
from typing import List, Mapping, Optional, Protocol, Sequence, Tuple

from .configuration import Configuration
from .exceptions import MessageSendError
from .templates import RenderedTemplate, TemplateManager


class CommandRunner(Protocol):
    """Protocol describing callable command runners."""

    def __call__(self, command: Sequence[str]) -> None:  # pragma: no cover - Protocol definition
        """Execute the provided command."""


class SubprocessCommandRunner:
    """Command runner that delegates to :func:`subprocess.run`."""

    def __call__(self, command: Sequence[str]) -> None:
        if not isinstance(command, Sequence) or isinstance(command, (str, bytes)):
            raise TypeError("Command must be a sequence of strings.")
        for segment in command:
            if not isinstance(segment, str):
                raise TypeError("Command segments must be strings.")
        subprocess.run(tuple(command), check=True, text=True, shell=False)


@dataclass(slots=True)
class IMessageClient:
    """A client for sending messages via iMessage on macOS."""

    configuration: Configuration
    template_manager: TemplateManager = field(default_factory=TemplateManager)
    command_runner: CommandRunner = field(default_factory=SubprocessCommandRunner)
    logger: logging.Logger = field(default_factory=lambda: logging.getLogger(__name__))

    def __post_init__(self) -> None:
        if not any(isinstance(handler, logging.FileHandler) for handler in self.logger.handlers):
            file_handler = logging.FileHandler("macpymessenger.log")
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.INFO)

    def send(self, phone_number: str, message: str, delay_seconds: int = 0) -> None:
        if delay_seconds < 0:
            raise ValueError("Delay must be non-negative.")
        command: List[str] = [
            "osascript",
            str(self.configuration.send_script_path),
            phone_number,
            message,
            str(delay_seconds),
        ]
        try:
            self.command_runner(command)
            self.logger.info("Message sent to %s", phone_number)
        except subprocess.CalledProcessError as error:
            self.logger.error("Failed to send message to %s: %s", phone_number, error)
            raise MessageSendError(
                f"Failed to send message to {phone_number}"
            ) from error
        except OSError as error:
            self.logger.error("Execution error while sending to %s: %s", phone_number, error)
            raise MessageSendError(
                f"Failed to execute osascript for {phone_number}"
            ) from error

    def send_template(
        self,
        phone_number: str,
        template_id: str,
        context: Optional[Mapping[str, object]] = None,
        delay_seconds: int = 0,
    ) -> None:
        rendered_template: RenderedTemplate = self.template_manager.compose_template(
            template_id, context
        )
        return self.send(phone_number, rendered_template.content, delay_seconds)

    def create_template(
        self, template_id: str, content: str, parent_identifier: Optional[str] = None
    ) -> None:
        self.template_manager.create_template(template_id, content, parent_identifier)

    def update_template(self, template_id: str, new_content: str) -> None:
        self.template_manager.update_template(template_id, new_content)

    def delete_template(self, template_id: str) -> None:
        self.template_manager.delete_template(template_id)

    def send_bulk(self, phone_numbers: Sequence[str], message: str) -> Tuple[List[str], List[str]]:
        successful: List[str] = []
        failed: List[str] = []
        for number in phone_numbers:
            try:
                self.send(number, message)
                successful.append(number)
            except MessageSendError:
                failed.append(number)
        return successful, failed

    def get_chat_history(self, phone_number: str, limit: int = 10) -> List[Mapping[str, object]]:
        raise NotImplementedError("Chat history retrieval is not yet implemented.")

    def send_with_attachment(
        self, phone_number: str, message: str, attachment_path: str
    ) -> bool:
        raise NotImplementedError("Sending messages with attachments is not yet implemented.")
