import sqlite3
from .message import Message
from .configuration import Configuration

class DBManager:
    def __init__(self, config: Configuration):
        self.config = config
        self.connection = None

    def open_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.config.db_path, uri=True)

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def get_most_recently_sent_text(self) -> str:
        self.open_connection()
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT guid, id as handle, text, date, date_read, date_delivered
            FROM message
            LEFT OUTER JOIN handle ON message.handle_id=handle.ROWID
            WHERE is_from_me = 1
            ORDER BY date DESC
            LIMIT 1
        """)
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None

    def get_message(self, guid: str) -> Message | None:
        self.open_connection()
        cursor = self.connection.cursor()
        cursor.execute(f"""
            SELECT guid, date, date_read, date_delivered
            FROM message
            LEFT OUTER JOIN handle ON message.handle_id=handle.ROWID
            WHERE is_from_me = 1 and guid="{guid}"
            LIMIT 1
        """)
        result = cursor.fetchone()
        cursor.close()

        if result:
            return Message(
                guid=result[0],
                date=Message.from_apple_time(result[1]),
                date_read=Message.from_apple_time(result[2]),
                date_delivered=Message.from_apple_time(result[3])
            )
        return None

    def get_messages_for_phone_number(self, phone_number: str) -> list[Message]:
        self.open_connection()
        cursor = self.connection.cursor()
        cursor.execute(f"""
            SELECT guid, date, date_read, date_delivered
            FROM message
            LEFT OUTER JOIN handle ON message.handle_id=handle.ROWID
            WHERE handle.id = "{phone_number}"
            ORDER BY date DESC
        """)
        results = cursor.fetchall()
        cursor.close()

        messages = []
        for result in results:
            message = Message(
                guid=result[0],
                date=Message.from_apple_time(result[1]),
                date_read=Message.from_apple_time(result[2]),
                date_delivered=Message.from_apple_time(result[3])
            )
            messages.append(message)

        return messages