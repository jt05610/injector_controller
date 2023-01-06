from dataclasses import dataclass
from typing import Tuple, Optional, Union

from modbus_device.domain import exceptions


@dataclass(frozen=True)
class Table:
    addresses: Tuple[str, ...]
    name: str
    read_code: int
    write_code: Optional[int] = None
    read_only: bool = True

    def read(self, node: str, address: Union[int, str]) -> str:
        num = 1 if self.read_code < 0x03 else 2
        return self._message_str(node, self._addr(address), num)

    def write(self, node: str, address: Union[int, str], value: int) -> str:
        if not self.read_only:
            max_value = 1 if self.write_code == 0x05 else 0xFFFFFFFF
            if value <= max_value:
                return self._message_str(node, self._addr(address), value)
            else:
                raise exceptions.ValueOutOfRangeException(0x01)
        else:
            raise exceptions.WriteToReadOnlyException(table_name=self.name)

    @staticmethod
    def _message_str(node: int, address: int, nb: int) -> str:
        return f"{node} {address} {nb}"

    def _addr(self, address: Union[int, str]) -> int:
        if isinstance(address, int):
            addr_int = address
        elif isinstance(address, str):
            try:
                addr_int = self.addresses.index(address)
            except ValueError:
                raise exceptions.AddressNotInTableException(address, self.name)
        else:
            raise exceptions.BadAddressPassedException(address)
        if addr_int not in range(len(self.addresses)):
            raise exceptions.AddressNotInTableException(address, self.name)
        else:
            return addr_int


def discrete_inputs(addresses: Tuple[str, ...]):
    return Table(addresses=addresses, name="discrete_inputs", read_code=0x02)


def coils(addresses: Tuple[str, ...]):
    return Table(
        addresses=addresses,
        name="coils",
        read_code=0x01,
        write_code=0x05,
        read_only=False,
    )


def input_registers(addresses: Tuple[str, ...]):
    return Table(addresses=addresses, name="input_registers", read_code=0x04)


def holding_registers(addresses: Tuple[str, ...]):
    return Table(
        addresses=addresses,
        name="holding_registers",
        read_code=0x03,
        write_code=0x06,
        read_only=False,
    )


@dataclass(frozen=True)
class DataModel:
    discrete_inputs: Optional[Table] = None
    coils: Optional[Table] = None
    input_registers: Optional[Table] = None
    holding_registers: Optional[Table] = None


class ModbusDevice:
    _id: int
    ref: str
    address: int

    def __init__(
        self,
        data_model: DataModel,
        _id: Optional[int] = None,
        ref: str = "",
        address: int = 0xFF,
    ):
        self._id = _id
        self.ref = ref
        self.address = address
        self.data_model = data_model

    def read_coils(self):
        pass

    def read_discrete_inputs(self):
        pass

    def read_holding_registers(self):
        pass

    def write_single_coil(self):
        pass

    def write_single_register(self):
        pass
