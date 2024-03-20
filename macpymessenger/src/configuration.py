import os
from pathlib import Path


class Configuration:
    def __init__(self, send_script_path=None):
        self.send_script_path = send_script_path or os.path.join(Path(__file__).parent, "osascript", "sendMessage.scpt")

        self._validate_script_paths()

    def _validate_script_paths(self):
        if not os.path.exists(self.send_script_path):
            raise FileNotFoundError(f"Send script not found at path: {self.send_script_path}")