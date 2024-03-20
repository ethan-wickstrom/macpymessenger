import os
import subprocess
from .configuration import Configuration


class IMessageClient:
    def __init__(self, config: Configuration):
        self.config = config
        self.send_script_path = os.path.join(os.path.dirname(__file__), "osascript", "sendMessage.scpt")
        self.check_compatibility_script_path = os.path.join(
            os.path.dirname(__file__), "osascript", "checkCompatibility.scpt"
        )

    def send(self, phone_number: str, message: str) -> bool:
        cmd = f'osascript "{self.send_script_path}" "{phone_number}" "{message}"'
        try:
            result = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
            return not result.startswith("Error:")
        except subprocess.CalledProcessError:
            return False

    def check_compatibility(self, phone_number: str) -> bool:
        cmd = f'osascript "{self.check_compatibility_script_path}" "{phone_number}"'
        try:
            result = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
            return result == "true"
        except subprocess.CalledProcessError:
            return False

    def close(self):
        pass
