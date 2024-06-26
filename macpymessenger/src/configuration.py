import os
from pathlib import Path
from typing import Optional


class Configuration:
    """Manages configuration settings for the macpymessenger library."""

    def __init__(self, send_script_path: Optional[str] = None):
        """
        Initialize the Configuration object.

        Args:
            send_script_path (Optional[str]): The path to the send message script.
                If not provided, defaults to the bundled script.
        """
        self.send_script_path = send_script_path or self._get_default_send_script_path()
        self._validate_script_paths()

    def _get_default_send_script_path(self) -> str:
        """Get the default path for the send message script."""
        return os.path.join(Path(__file__).parent, "osascript", "sendMessage.scpt")

    def _validate_script_paths(self) -> None:
        """Validate that the specified script paths exist."""
        if not os.path.exists(self.send_script_path):
            raise FileNotFoundError(f"Send script not found at path: {self.send_script_path}")

    def __str__(self) -> str:
        """Return a string representation of the Configuration object."""
        return f"Configuration(send_script_path='{self.send_script_path}')"

    def __repr__(self) -> str:
        """Return a detailed string representation of the Configuration object."""
        return self.__str__()
