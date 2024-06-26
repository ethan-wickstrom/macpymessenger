import subprocess
import logging
from typing import List, Tuple

from .src import TemplateManager, Configuration, exceptions

logger = logging.getLogger(__name__)

class IMessageClient:
    """A client for sending iMessages on macOS."""

    def __init__(self, configuration: Configuration):
        """
        Initialize the IMessageClient.

        Args:
            configuration (Configuration): The configuration object for the client.
        """
        self.configuration = configuration
        self.template_manager = TemplateManager()
        self._setup_logging()

    def _setup_logging(self):
        """Set up logging for the IMessageClient."""
        logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler('macpymessenger.log')
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    def send(self, phone_number: str, message: str, delay: int = 0) -> bool:
        """
        Send an iMessage to the specified phone number.

        Args:
            phone_number (str): The phone number of the recipient.
            message (str): The message content.
            delay (int, optional): The delay before the message is sent, in seconds. Defaults to 0.

        Returns:
            bool: True if the message was sent successfully, False otherwise.

        Raises:
            MessageSendError: If an error occurs while sending the message.
        """
        try:
            subprocess.run(
                [
                    "osascript",
                    self.configuration.send_script_path,
                    phone_number,
                    message,
                    str(delay)
                ],
                check=True,
            )
            logger.info(f"Message sent to {phone_number}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to send message to {phone_number}. Error: {str(e)}")
            raise exceptions.MessageSendError(f"Failed to send message to {phone_number}") from e

    def send_template(self, phone_number: str, template_id: str, context: dict = None) -> bool:
        """
        Send a message using a template.

        Args:
            phone_number (str): The phone number of the recipient.
            template_id (str): The ID of the template to use.
            context (dict, optional): The context data for rendering the template. Defaults to None.

        Returns:
            bool: True if the message was sent successfully, False otherwise.
        """
        context = context or {}
        composed_template = self.template_manager.compose_template(template_id, **context)
        return self.send(phone_number, composed_template.render())

    def create_template(self, template_id: str, content: str, parent: str = None) -> None:
        """
        Create a new message template.

        Args:
            template_id (str): The ID of the template.
            content (str): The content of the template.
            parent (str, optional): The ID of the parent template. Defaults to None.
        """
        self.template_manager.create_template(template_id, content, parent)

    def update_template(self, template_id: str, new_content: str) -> None:
        """
        Update an existing message template.

        Args:
            template_id (str): The ID of the template.
            new_content (str): The new content of the template.
        """
        self.template_manager.update_template(template_id, new_content)

    def delete_template(self, template_id: str) -> None:
        """
        Delete an existing message template.

        Args:
            template_id (str): The ID of the template.
        """
        self.template_manager.delete_template(template_id)

    def send_bulk(self, phone_numbers: List[str], message: str) -> Tuple[List[str], List[str]]:
        """
        Send a message to multiple recipients.

        Args:
            phone_numbers (List[str]): A list of phone numbers.
            message (str): The message content.

        Returns:
            Tuple[List[str], List[str]]: A tuple containing the phone numbers to which the message
            was successfully sent, and the phone numbers to which the message failed to send.
        """
        successful_sends = []
        failed_sends = []

        for phone_number in phone_numbers:
            try:
                self.send(phone_number, message)
                successful_sends.append(phone_number)
            except exceptions.MessageSendError as e:
                logger.error(f"Failed to send message to {phone_number}. Error: {str(e)}")
                failed_sends.append(phone_number)

        return successful_sends, failed_sends

    def get_chat_history(self, phone_number: str, limit: int = 10) -> List[dict]:
        """
        Retrieve chat history for a given phone number.

        Args:
            phone_number (str): The phone number to retrieve chat history for.
            limit (int, optional): The maximum number of messages to retrieve. Defaults to 10.

        Returns:
            List[dict]: A list of dictionaries containing message information.
        """
        # TODO: Implement chat history retrieval
        raise NotImplementedError("Chat history retrieval is not yet implemented.")

    def send_with_attachment(self, phone_number: str, message: str, attachment_path: str) -> bool:
        """
        Send a message with an attachment.

        Args:
            phone_number (str): The phone number of the recipient.
            message (str): The message content.
            attachment_path (str): The path to the attachment file.

        Returns:
            bool: True if the message was sent successfully, False otherwise.
        """
        # TODO: Implement sending messages with attachments
        raise NotImplementedError("Sending messages with attachments is not yet implemented.")

