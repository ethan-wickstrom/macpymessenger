import os
import subprocess
import platform
from time import sleep
from shlex import quote
from .db_manager import DBManager
from .message import Message
from .configuration import Configuration


def check_compatibility(phone: str) -> bool:
    mac_ver, _, _ = platform.mac_ver()
    mac_ver = float('.'.join(mac_ver.split('.')[:2]))

    dir_path = os.path.dirname(os.path.realpath(__file__))
    relative_path = 'osascript/check_imessage.js'
    path = f'{dir_path}/{relative_path}'
    cmd = f'osascript -l JavaScript {path} {phone} {mac_ver}'
    output = subprocess.check_output(cmd, shell=True)

    return 'true' in output.decode('utf-8')


class IMessageClient:
    def __init__(self):
        self.config = Configuration()
        self.db_manager = DBManager(self.config)

    def send(self, phone: str, message: str) -> str:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        relative_path = 'osascript/send_message.js'
        path = f'{dir_path}/{relative_path}'
        cmd = f'osascript -l JavaScript {path} {quote(phone)} {quote(message)}'
        subprocess.call(cmd, shell=True)

        sleep(1)  # Allow local db to update
        guid = self.db_manager.get_most_recently_sent_text()
        return guid

    def status(self, guid: str) -> Message:
        return self.db_manager.get_message(guid)

    def close(self):
        self.db_manager.close_connection()
