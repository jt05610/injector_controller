from dataclasses import dataclass
from typing import Iterable


class Command:
    pass


@dataclass
class ReadTable(Command):
    device_ref: str
    table: str
    endpoint: str


@dataclass
class WriteTable(Command):
    device_ref: str
    table: str
    endpoint: str
    value: int


@dataclass
class ProcessTableReadResponse(Command):
    node_address: int
    table: str
    table_address: int
    value: int


@dataclass
class ProcessTableWriteResponse(Command):
    node_address: int
    table: str
    table_address: int
    value: int


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
