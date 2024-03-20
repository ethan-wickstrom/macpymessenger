import subprocess
from .configuration import Configuration


class IMessageClient:
    def __init__(self, config: Configuration):
        self.config = config

    def send(self, phone_number: str, message: str) -> bool:
        cmd = f'osascript "{self.config.send_script_path}" "{phone_number}" "{message}"'
        try:
            result = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
            return not result.startswith("Error:")
        except subprocess.CalledProcessError:
            return False