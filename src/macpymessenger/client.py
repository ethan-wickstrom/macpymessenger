"""The public messaging client."""

from __future__ import annotations

import logging
import subprocess
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from string.templatelib import Template

from typing import Protocol

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
    """A client for sending messages via iMessage on macOS.

    Parameters
    ----------
    configuration:
        Resolved configuration specifying the AppleScript entry point.
    template_manager:
        Template storage and rendering backend used for templated messages.
    command_runner:
        Callable responsible for executing the generated AppleScript command.
    logger:
        Logger instance used for emitting operational events.
    enable_file_logging:
        When ``True`` a ``macpymessenger.log`` :class:`logging.FileHandler` is attached during
        initialization if one is not already configured. The default ``False`` value respects the
        handlers supplied on ``logger`` and prevents creating files implicitly.
    """

    configuration: Configuration
    template_manager: TemplateManager = field(default_factory=TemplateManager)
    command_runner: CommandRunner = field(default_factory=SubprocessCommandRunner)
    logger: logging.Logger = field(default_factory=lambda: logging.getLogger(__name__))
    enable_file_logging: bool = False

    def __post_init__(self) -> None:
        has_file_handler = any(
            isinstance(handler, logging.FileHandler) for handler in self.logger.handlers
        )
        if self.enable_file_logging and not has_file_handler:
            file_handler = logging.FileHandler("macpymessenger.log")
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.INFO)

    def send(self, phone_number: str, message: str, delay_seconds: int = 0) -> None:
        if delay_seconds < 0:
            raise ValueError("Delay must be non-negative.")
        command: list[str] = [
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
            raise MessageSendError(f"Failed to send message to {phone_number}") from error
        except OSError as error:
            self.logger.error("Execution error while sending to %s: %s", phone_number, error)
            raise MessageSendError(f"Failed to execute osascript for {phone_number}") from error

    def send_template(
        self,
        phone_number: str,
        template_id: str,
        context: Mapping[str, str] | None = None,
        delay_seconds: int = 0,
    ) -> None:
        rendered_template: RenderedTemplate = self.template_manager.compose_template(
            template_id, context
        )
        return self.send(phone_number, rendered_template.content, delay_seconds)

    def create_template(
        self,
        template_id: str,
        factory: Callable[..., "Template"],
    ) -> None:
        self.template_manager.create_template(template_id, factory)

    def update_template(self, template_id: str, factory: Callable[..., "Template"]) -> None:
        self.template_manager.update_template(template_id, factory)

    def delete_template(self, template_id: str) -> None:
        self.template_manager.delete_template(template_id)

    def send_bulk(self, phone_numbers: Sequence[str], message: str) -> tuple[list[str], list[str]]:
        successful: list[str] = []
        failed: list[str] = []
        for number in phone_numbers:
            try:
                self.send(number, message)
                successful.append(number)
            except MessageSendError:
                failed.append(number)
        return successful, failed

    def get_chat_history(self, phone_number: str, limit: int = 10) -> list[Mapping[str, object]]:
        """Experimental: Chat history retrieval is not yet implemented.

        Parameters
        ----------
        phone_number:
            The E.164-formatted phone number or iMessage handle whose history would be fetched.
        limit:
            Maximum number of messages to return once the feature ships. Values must be
            positive and are expected to cap the page size. The default of ``10`` is a
            placeholder until the implementation is available.

        Returns
        -------
        List[Mapping[str, object]]
            This method will eventually return structured message payloads ordered from most
            recent to oldest. The exact schema is intentionally unspecified while the feature
            is experimental.

        Raises
        ------
        NotImplementedError
            Always raised. The message includes the ``"Experimental"`` prefix to signal that
            the public API exists but is not yet functional.

        Notes
        -----
        Expected availability: TBD. Tracking work is scoped for a future minor release.
        Until then, callers must not rely on this method.
        """

        raise NotImplementedError("Experimental: Chat history retrieval is not yet implemented.")

    def send_with_attachment(self, phone_number: str, message: str, attachment_path: str) -> bool:
        """Experimental: Sending messages with attachments is not yet implemented.

        Parameters
        ----------
        phone_number:
            Intended recipient handle in E.164 or email format.
        message:
            Text body that would accompany the attachment when support lands.
        attachment_path:
            Absolute path to a file on disk. Future implementations will validate MIME type,
            existence, and maximum payload size before sending.

        Returns
        -------
        bool
            Planned to indicate whether the attachment send succeeded. The concrete semantics
            will be finalised alongside the implementation.

        Raises
        ------
        NotImplementedError
            Always raised with an ``"Experimental"`` prefixed message, ensuring callers are
            aware that attachment delivery is not currently supported.

        Notes
        -----
        Expected availability: TBD. The method is defined to stabilise the public API surface
        but must not be invoked in production workflows yet.
        """

        raise NotImplementedError(
            "Experimental: Sending messages with attachments is not yet implemented."
        )
