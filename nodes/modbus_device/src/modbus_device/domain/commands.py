from dataclasses import dataclass


class Command:
    pass


@dataclass
class ReadTable(Command):
    node_address: int
    table: str
    address: int
    num: int = 1


@dataclass
class WriteTable(Command):
    node_address: str
    table: str
    address: int
    value: int
