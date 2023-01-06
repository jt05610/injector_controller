from dataclasses import dataclass


class Command:
    pass


@dataclass
class ReadTable(Command):
    table: str
    pdu: str


@dataclass
class WriteTable(Command):
    table: str
    pdu: str
