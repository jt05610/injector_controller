from dataclasses import dataclass


class Event:
    pass


@dataclass
class TableRead(Event):
    table: str
    address: str
    value: int


@dataclass
class TableWritten(Event):
    table: str
