from dataclasses import dataclass
from typing import Tuple, Optional, Union, Iterable

from modbus_device.domain import exceptions
from pydantic import BaseModel


@dataclass(frozen=True)
class Table:
    addresses: Tuple[str, ...]
    name: str
    read_code: int
    write_code: Optional[int] = None
    read_only: bool = True


@dataclass(frozen=True)
class DataModel:
    ref: str
    discrete_inputs: Optional[Table] = None
    coils: Optional[Table] = None
    input_registers: Optional[Table] = None
    holding_registers: Optional[Table] = None


@dataclass(frozen=True)
class ModbusDevice:
    ref: str
    node_address: int
    data_model: DataModel


def discrete_inputs(addresses: Tuple[str, ...]) -> Table:
    return Table(addresses=addresses, name="discrete_inputs", read_code=0x02)


def coils(addresses: Tuple[str, ...]) -> Table:
    return Table(
        addresses=addresses,
        name="coils",
        read_code=0x01,
        write_code=0x05,
        read_only=False,
    )


def input_registers(addresses: Tuple[str, ...]) -> Table:
    return Table(addresses=addresses, name="input_registers", read_code=0x04)


def holding_registers(addresses: Tuple[str, ...]) -> Table:
    return Table(
        addresses=addresses,
        name="holding_registers",
        read_code=0x03,
        write_code=0x06,
        read_only=False,
    )


TABLE_MAP = {
    "discrete_inputs": discrete_inputs,
    "coils": coils,
    "input_registers": input_registers,
    "holding_registers": holding_registers,
}


def create_table(table: str, addresses: Iterable[str]) -> Table:
    return TABLE_MAP[table](addresses)


def table_iter(**kwargs) -> Iterable[Tuple[str, Table]]:
    for table, factory in TABLE_MAP.items():
        yield table, factory(kwargs.get(table))


def data_model(**kwargs) -> DataModel:
    return DataModel(ref=kwargs.get("ref"), **dict(table_iter(**kwargs)))


def message_str(node: int, address: int, nb: int) -> str:
    return f"{node} {address} {nb}"


def get_addr(tbl: Table, address: Union[int, str]) -> int:
    if isinstance(address, int):
        addr_int = address
    elif isinstance(address, str):
        try:
            addr_int = tbl.addresses.index(address)
        except ValueError:
            raise exceptions.AddressNotInTableException(address, tbl.name)
    else:
        raise exceptions.BadAddressPassedException(address)
    if addr_int not in range(len(tbl.addresses)):
        raise exceptions.AddressNotInTableException(address, tbl.name)
    else:
        return addr_int


def read_table(tbl: Table, node: str, address: Union[int, str]) -> str:
    num = 1 if tbl.read_code < 0x03 else 2
    return message_str(node, get_addr(tbl, address), num)


def write_table(
    tbl: Table, node: str, address: Union[int, str], value: int
) -> str:
    if not tbl.read_only:
        max_value = 1 if tbl.write_code == 0x05 else 0xFFFFFFFF
        if value <= max_value:
            return message_str(node, get_addr(tbl, address), value)
        else:
            raise exceptions.ValueOutOfRangeException(0x01)
    else:
        raise exceptions.WriteToReadOnlyException(table_name=tbl.name)
