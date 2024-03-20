import subprocess
import logging
from .src.configuration import Configuration

logger = logging.getLogger(__name__)


class IMessageClient:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration

    def send(self, phone_number: str, message: str, delay: int = 0) -> bool:
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
            return False

    def get_chat_history(self, phone_number: str, limit: int = 10) -> list:
        # Implementation to retrieve chat history
        pass

    def send_with_attachment(self, phone_number: str, message: str, attachment_path: str) -> bool:
        # Implementation to send message with attachment
        pass