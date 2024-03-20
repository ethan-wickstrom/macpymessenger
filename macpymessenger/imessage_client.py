import subprocess

from .src import TemplateManager, Configuration, exceptions
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('macpymessenger.log')
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class IMessageClient:
    """
    A client for sending iMessages on macOS.

    Args:
        configuration (Configuration): The configuration object for the client.
    """

    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.template_manager = TemplateManager()

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

        :param phone_number:
        :param message:
        :param delay:

        :returns bool:
        :raises MessageSendError:
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

    def send_template(self, phone_number, template_id) -> bool:
        """
        Send a message using a template.

        Args:
            phone_number (str): The phone number of the recipient.
            template_id (str): The ID of the template to use.

        Returns:
            bool: True if the message was sent successfully, False otherwise.

        :param phone_number:
        :param template_id:
        :returns bool:
        """
        template = self.template_manager.get_template(template_id)
        return self.send(phone_number, template.content)

    def create_template(self, template_id, content) -> None:
        """
        Create a new message template.

        Args:
            template_id (str): The ID of the template.
            content (str): The content of the template.

        :param template_id:
        :param content:
        :return None:
        """
        self.template_manager.create_template(template_id, content)

    def update_template(self, template_id, new_content) -> None:
        """
        Update an existing message template.

        Args:
            template_id (str): The ID of the template.
            new_content (str): The new content of the template.

        :param template_id:
        :param new_content:
        :return None:
        """
        self.template_manager.update_template(template_id, new_content)

    def delete_template(self, template_id) -> None:
        """
        Delete an existing message template.

        Args:
            template_id (str): The ID of the template.

        :param template_id:
        :return None:
        """
        self.template_manager.delete_template(template_id)

    def send_bulk(self, phone_numbers, message) -> tuple:
        """
        Send a message to multiple recipients.

        Args:
            phone_numbers (list): A list of phone numbers.
            message (str): The message content.

        Returns: tuple: A tuple containing the phone numbers to which the message was successfully sent, and the phone numbers to which the message failed to send.

        :param phone_numbers:
        :param message:
        :return tuple:
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

    def get_chat_history(self, phone_number: str, limit: int = 10) -> list:
        # Implementation to retrieve chat history
        pass

    def send_with_attachment(self, phone_number: str, message: str, attachment_path: str) -> bool:
        # Implementation to send message with attachment
        pass
