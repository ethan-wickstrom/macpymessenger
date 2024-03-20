import os
import sqlite3
import tempfile
import subprocess
from .message import Message
from .configuration import Configuration
from shlex import quote as shlex_quote


class DBManager:
    def __init__(self, config: Configuration):
        self.config = config
        self.connection = None
        self.temp_db_path = None

    def open_connection(self):
        if self.connection is None:
            # Create a temporary directory
            temp_dir = tempfile.mkdtemp()
            self.temp_db_path = os.path.join(temp_dir, 'chat.db')

            print(self.temp_db_path)

            # Use a terminal command to copy the chat.db file with proper permissions
            command = f"echo {self.config.os_password} | sudo -S cp {shlex_quote(self.config.db_path)} {shlex_quote(self.temp_db_path)}"
            subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

            # Connect to the temporary database
            self.connection = sqlite3.connect(self.temp_db_path, uri=True)

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

            # Clean up the temporary database file
            if self.temp_db_path:
                os.remove(self.temp_db_path)
                self.temp_db_path = None

    def get_most_recently_sent_text(self) -> str:
        self.open_connection()
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT guid, text, date
            FROM message
            WHERE is_from_me = 1
            ORDER BY date DESC
            LIMIT 1
        """)
        result = cursor.fetchone()
        cursor.close()
        return result[1] if result else None

    def get_message(self, guid: str) -> Message | None:
        self.open_connection()
        cursor = self.connection.cursor()
        cursor.execute(f"""
            SELECT guid, text, date
            FROM message
            WHERE guid = "{guid}"
            LIMIT 1
        """)
        result = cursor.fetchone()
        cursor.close()

        if result:
            return Message(
                guid=result[0],
                text=result[1],
                date=Message.from_apple_time(result[2])
            )
        return None

    def get_messages_for_phone_number(self, phone_number: str) -> list[Message]:
        self.open_connection()
        cursor = self.connection.cursor()
        cursor.execute(f"""
            SELECT m.guid, m.text, m.date
            FROM message m
            JOIN chat_message_join cmj ON m.ROWID = cmj.message_id
            JOIN chat c ON cmj.chat_id = c.ROWID
            JOIN chat_handle_join chj ON c.ROWID = chj.chat_id
            JOIN handle h ON chj.handle_id = h.ROWID
            WHERE h.id = "{phone_number}"
            ORDER BY m.date DESC
        """)
        results = cursor.fetchall()
        cursor.close()

        messages = []
        for result in results:
            message = Message(
                guid=result[0],
                text=result[1],
                date=Message.from_apple_time(result[2])
            )
            messages.append(message)

        return messages