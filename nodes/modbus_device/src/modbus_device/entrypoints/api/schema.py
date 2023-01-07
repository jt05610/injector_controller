from typing import Optional, Tuple

from bson import ObjectId
from pydantic import BaseModel, Field
from fastapi import FastAPI
from modbus_device.adapters.mongodb_orm import MongoDBCRUDRouter as CRUDRouter
from motor.motor_asyncio import AsyncIOMotorClient


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
    id: int
    ref: str
    node_address: int
    data_model: DataModel


class CreateModbusDevice(BaseModel):
    ref: str
    node_address: int
    data_model_ref: str


class UpdateModbusDevice(BaseModel):
    node_address: int


def map_routers(app: FastAPI, client: AsyncIOMotorClient, db: str):
    _db = getattr(client, db)
    app.include_router(
        CRUDRouter(
            db=_db,
            schema=DataModel,
            collection="device.data_model",
            create_schema=CreateDataModel,
            update_schema=UpdateDataModel,
            prefix="device/data_model",
        )
    )

    app.include_router(
        CRUDRouter(
            db=_db,
            schema=ModbusDevice,
            collection="device",
            create_schema=CreateModbusDevice,
            update_schema=UpdateModbusDevice,
            prefix="device",
        )
    )
