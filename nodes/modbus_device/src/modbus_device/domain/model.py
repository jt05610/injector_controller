from dataclasses import dataclass
from typing import Tuple, Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from modbus_device.domain import exceptions


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid object id")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class DataModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    ref: str = Field(...)
    discrete_inputs: Tuple[str, ...] = Field(...)
    coils: Tuple[str, ...] = Field(...)
    input_registers: Tuple[str, ...] = Field(...)
    holding_registers: Tuple[str, ...] = Field(...)

    @property
    def functions(self) -> Tuple[str, ...]:
        return (
            self.discrete_inputs
            + self.coils
            + self.input_registers
            + self.holding_registers
        )

    def iter_func(self):
        for table in (
            "discrete_inputs",
            "coils",
            "input_registers",
            "holding_registers",
        ):
            for i, a in enumerate(getattr(self, table)):
                yield a, (table, i)

    @property
    def read_write_lookup(self):
        def _gen():
            for table in ("coils", "holding_registers"):
                for i, a in enumerate(getattr(self, table)):
                    yield a, (table, i)

        return dict(_gen())

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "ref": "example_data_model",
                "discrete_inputs": ["discrete_input_1", "discrete_input_2"],
                "coils": ["coil_1", "coil_2"],
                "input_registers": ["input_register_1", "input_register_2"],
                "holding_registers": [
                    "holding_register_1",
                    "holding_register_2",
                ],
            }
        }


class CreateDataModel(BaseModel):
    ref: str
    discrete_inputs: Optional[Tuple[str, ...]] = None
    coils: Optional[Tuple[str, ...]] = None
    input_registers: Optional[Tuple[str, ...]] = None
    holding_registers: Optional[Tuple[str, ...]] = None


class UpdateDataModel(BaseModel):
    discrete_inputs: Optional[Tuple[str, ...]] = None
    coils: Optional[Tuple[str, ...]] = None
    input_registers: Optional[Tuple[str, ...]] = None
    holding_registers: Optional[Tuple[str, ...]] = None


class ModbusDevice(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    ref: str = Field(...)
    node_address: int = Field(...)
    data_model_id: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "ref": "example_data_model",
                "node_address": 0xCC,
                "data_model": "1234",
            }
        }


class ReadTableResult(BaseModel):
    value: int


class WriteTableRequest(BaseModel):
    value: int


class WriteTableResult(BaseModel):
    ok: bool


class CreateModbusDevice(BaseModel):
    ref: str
    node_address: int
    data_model_id: str


class UpdateModbusDevice(BaseModel):
    node_address: Optional[int] = None
    data_model_id: Optional[str] = None


@dataclass(frozen=True)
class Table:
    name: str
    read_code: int
    write_code: Optional[int] = None
    read_only: bool = True


TABLE_LOOKUP = {
    "discrete_inputs": Table(name="discrete_inputs", read_code=0x02),
    "coils": Table(
        name="coils",
        read_code=0x01,
        write_code=0x05,
        read_only=False,
    ),
    "input_registers": Table(name="input_registers", read_code=0x04),
    "holding_registers": Table(
        name="holding_registers",
        read_code=0x03,
        write_code=0x06,
        read_only=False,
    ),
}


def message_str(node: int, address: int, nb: int) -> str:
    return f"{node} {address} {nb}"


def read_table(tbl: str, node: int, address: int) -> str:
    table = TABLE_LOOKUP[tbl]
    num = 1 if table.read_code < 0x03 else 2
    return message_str(node, address, num)


def write_table(tbl: str, node: int, address: int, value: int) -> str:
    table = TABLE_LOOKUP[tbl]
    if not table.read_only:
        max_value = 1 if table.write_code == 0x05 else 0xFFFFFFFF
        if value <= max_value:
            return message_str(node, address, value)
        else:
            raise exceptions.ValueOutOfRangeException(0x01)
    else:
        raise exceptions.WriteToReadOnlyException(table_name=table.name)
