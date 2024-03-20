import math
import datetime
import pytz
from .configuration import Configuration


class Message:
    def __init__(self, guid: str, text: str, date: datetime.datetime):
        self.guid = guid
        self.text = text
        self.date = date

    @staticmethod
    def from_apple_time(timestamp: int) -> datetime.datetime | None:
        if timestamp == 0:
            return None

        timestamp = Message.unpack_time(timestamp)
        return datetime.datetime.fromtimestamp(timestamp + Configuration.DATE_OFFSET, tz=pytz.timezone('US/Pacific'))

    @staticmethod
    def unpack_time(timestamp: int) -> int:
        return math.floor(timestamp / (10 ** 9))

    @staticmethod
    def pack_time_conditionally(timestamp: int) -> int:
        return timestamp * 10 ** 9
