from dataclasses import dataclass
from typing import Iterable


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


@dataclass
class CreateDataModel(Command):
    ref: str
    discrete_inputs: Iterable[str]
    coils: Iterable[str]
    input_registers: Iterable[str]
    holding_registers: Iterable[str]


@dataclass
class CreateDevice(Command):
    ref: str
    address: int
    data_model_ref: str
