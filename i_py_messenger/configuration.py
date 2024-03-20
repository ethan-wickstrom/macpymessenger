import os


class Configuration:
    send_script_path: str
    check_compatibility_script_path: str

    def __init__(self):
        self.send_script_path = os.path.join(os.path.dirname(__file__), "osascript", "sendMessage.scpt")
        self.check_compatibility_script_path = os.path.join(
            os.path.dirname(__file__), "osascript", "checkCompatibility.scpt"
        )