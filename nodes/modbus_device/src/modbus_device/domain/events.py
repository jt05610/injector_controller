from dataclasses import dataclass


class Event:
    pass


@dataclass
class TableRead(Event):
    device_ref: str
    table: str
    address: int
    function: str
    value: int


@dataclass
class TableWritten(Event):
    device_ref: str
    table: str
    address: int
    function: str
    value: int
