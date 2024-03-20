import os


class Configuration:
    DATE_OFFSET = 978307200

    def __init__(self):
        home = os.environ['HOME']
        self.db_path = f'{home}/Library/Messages/chat.db'
        self.send_script_path = os.path.join(os.path.dirname(__file__), "osascript", "sendMessage.scpt")
        self.check_compatibility_script_path = os.path.join(
            os.path.dirname(__file__), "osascript", "checkCompatibility.scpt"
        )
