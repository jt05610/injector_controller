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


@dataclass
class TableReadRequested(Event):
    table: str
    pdu: str


@dataclass
class TableWriteRequested(Event):
    table: str
    pdu: str


@dataclass
class DeviceCreated(Event):
    ref: str
    device_channel: str


@dataclass
class DataModelCreated(Event):
    ref: str
