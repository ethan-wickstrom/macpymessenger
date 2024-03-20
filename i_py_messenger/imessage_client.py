import os
import subprocess
from .configuration import Configuration
from .db_manager import DBManager
from .message import Message


class IMessageClient:
    def __init__(self, config: Configuration):
        self.config = config
        self.db_manager = DBManager(config)

    def send(self, phone_number: str, message: str) -> bool:
        cmd = f'osascript "{self.config.send_script_path}" "{phone_number}" "{message}"'
        try:
            result = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
            return not result.startswith("Error:")
        except subprocess.CalledProcessError:
            return False

    def check_compatibility(self, phone_number: str) -> bool:
        cmd = f'osascript "{self.config.check_compatibility_script_path}" "{phone_number}"'
        try:
            result = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
            return result == "true"
        except subprocess.CalledProcessError:
            return False

    def get_most_recently_sent_text(self) -> str:
        return self.db_manager.get_most_recently_sent_text()

    def get_message(self, guid: str) -> Message | None:
        return self.db_manager.get_message(guid)

    def get_messages_for_phone_number(self, phone_number: str) -> list[Message]:
        return self.db_manager.get_messages_for_phone_number(phone_number)

    def close(self):
        self.db_manager.close_connection()
