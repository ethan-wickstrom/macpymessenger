"""The public messaging client."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from .commands import CommandRunner, SubprocessCommandRunner
from .delivery import MessageDelivery
from .exceptions import MessageSendError
from .templates import TemplateManager

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from .configuration import Configuration
    from .templates import TemplateCallable

__all__ = ["IMessageClient"]


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
        Logger that receives operational events. Defaults to this module's
        logger. The library never attaches handlers or sets levels; route and
        format events with standard :mod:`logging` configuration.
    """

    __slots__ = ("_delivery", "_logger", "command_runner", "configuration", "template_manager")

    def __init__(
        self,
        configuration: Configuration,
        template_manager: TemplateManager | None = None,
        command_runner: CommandRunner | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        self.configuration = configuration
        self.template_manager = (
            template_manager if template_manager is not None else TemplateManager()
        )
        self.command_runner = (
            command_runner if command_runner is not None else SubprocessCommandRunner()
        )
        self._logger = logger if logger is not None else logging.getLogger(__name__)
        self._delivery = MessageDelivery(
            configuration=self.configuration,
            command_runner=self.command_runner,
            logger=self._logger,
        )

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    def send(self, phone_number: str, message: str, delay_seconds: int = 0) -> None:
        self._delivery.deliver(phone_number, message, delay_seconds)

    def send_template(
        self,
        phone_number: str,
        template_id: str,
        context: Mapping[str, object] | None = None,
        delay_seconds: int = 0,
    ) -> None:
        message_body = self.template_manager.render_template(template_id, context)
        self.send(phone_number, message_body, delay_seconds)

    def create_template(self, template_id: str, factory: TemplateCallable) -> None:
        self.template_manager.create_template(template_id, factory)

    def update_template(self, template_id: str, factory: TemplateCallable) -> None:
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
