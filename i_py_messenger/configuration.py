import os


class Configuration:
    DATE_OFFSET = 978307200

    def __init__(self):
        home = os.environ['HOME']
        self.db_path = f'{home}/Library/Messages/chat.db'
