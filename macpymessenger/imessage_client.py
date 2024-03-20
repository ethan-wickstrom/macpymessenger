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
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.template_manager = TemplateManager()

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
            raise exceptions.MessageSendError(f"Failed to send message to {phone_number}") from e

    def send_template(self, phone_number, template_id):
        template = self.template_manager.get_template(template_id)
        return self.send(phone_number, template.content)

    def create_template(self, template_id, content):
        self.template_manager.create_template(template_id, content)

    def update_template(self, template_id, new_content):
        self.template_manager.update_template(template_id, new_content)

    def delete_template(self, template_id):
        self.template_manager.delete_template(template_id)

    def get_chat_history(self, phone_number: str, limit: int = 10) -> list:
        # Implementation to retrieve chat history
        pass

    def send_with_attachment(self, phone_number: str, message: str, attachment_path: str) -> bool:
        # Implementation to send message with attachment
        pass
