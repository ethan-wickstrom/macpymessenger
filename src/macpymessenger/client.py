"""The public messaging client."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING, overload

from .commands import CommandRunner, SubprocessCommandRunner
from .delivery import MessageDelivery
from .exceptions import (
    ConfigurationError,
    MessageSendError,
)
from .templates import TemplateManager

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping, Sequence
    from string.templatelib import Template

    from .configuration import Configuration
else:
    Template = import_module("string.templatelib").Template
    Configuration = import_module("macpymessenger.configuration").Configuration


@dataclass(frozen=True, slots=True)
class FileLoggingConfiguration:
    """File logging destination for client operational events."""

    path: str | Path | None = None


__all__ = [
    "CommandRunner",
    "FileLoggingConfiguration",
    "IMessageClient",
    "SubprocessCommandRunner",
]


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
        Logger instance used for emitting operational events. When omitted a module-scoped
        logger is created and defaulted to ``INFO`` only if no handlers are configured.
    file_logging:
        Optional file logging destination. When provided, a :class:`logging.FileHandler` is
        attached if one is not already configured. When the path is omitted, the handler writes
        to ``macpymessenger.log`` in the current working directory.
    """

    __slots__ = (
        "_delivery",
        "_logger",
        "command_runner",
        "configuration",
        "file_logging",
        "template_manager",
    )

    def __init__(
        self,
        configuration: Configuration,
        template_manager: TemplateManager | None = None,
        command_runner: CommandRunner | None = None,
        logger: logging.Logger | None = None,
        file_logging: FileLoggingConfiguration | None = None,
    ) -> None:
        self.configuration = configuration
        self.template_manager = (
            template_manager if template_manager is not None else TemplateManager()
        )
        self.command_runner = (
            command_runner if command_runner is not None else SubprocessCommandRunner()
        )
        self.file_logging = file_logging

        if logger is None:
            created_default_logger = True
            logger_instance = logging.getLogger(__name__)
        else:
            created_default_logger = False
            logger_instance = logger

        if (
            created_default_logger
            and not logger_instance.handlers
            and logger_instance.level == logging.NOTSET
        ):
            logger_instance.setLevel(logging.INFO)

        has_file_handler = any(
            isinstance(handler, logging.FileHandler) for handler in logger_instance.handlers
        )
        if self.file_logging is not None and not has_file_handler:
            log_file_path_obj = (
                Path(self.file_logging.path)
                if self.file_logging.path is not None
                else Path.cwd() / "macpymessenger.log"
            )
            try:
                file_handler = logging.FileHandler(log_file_path_obj, encoding="utf-8")
            except OSError as error:
                error_message = error.strerror or str(error)
                raise ConfigurationError.file_logging_unavailable(
                    log_file_path_obj, error_message
                ) from error
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)
            logger_instance.addHandler(file_handler)

        self._logger = logger_instance
        self._delivery = MessageDelivery(
            configuration=self.configuration,
            command_runner=self.command_runner,
            logger=self._logger,
        )

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    @overload
    def send(self, phone_number: str, message: str, delay_seconds: int = 0) -> None: ...

    @overload
    def send(self, phone_number: str, message: str, delay_seconds: object = 0) -> None: ...

    def send(self, phone_number: str, message: str, delay_seconds: object = 0) -> None:
        self._delivery.deliver(phone_number, message, delay_seconds)

    def send_template(
        self,
        phone_number: str,
        template_id: str,
        context: Mapping[str, object] | None = None,
        delay_seconds: int = 0,
    ) -> None:
        rendered_template = self.template_manager.compose_template(template_id, context)
        return self.send(phone_number, rendered_template.content, delay_seconds)

    def create_template(
        self,
        template_id: str,
        factory: Callable[..., Template],
    ) -> None:
        self.template_manager.create_template(template_id, factory)

    def update_template(self, template_id: str, factory: Callable[..., Template]) -> None:
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

        message = "Experimental: Chat history retrieval is not yet implemented."
        raise NotImplementedError(message)

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

        message = "Experimental: Sending messages with attachments is not yet implemented."
        raise NotImplementedError(message)
