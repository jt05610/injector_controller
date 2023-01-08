from typing import Optional, Tuple

import aioredis
from bson import ObjectId
from fastapi_crudrouter.core import NOT_FOUND
from fastapi import FastAPI, APIRouter
from modbus_device.adapters.mongodb_orm import MongoDBCRUDRouter as CRUDRouter
from motor.motor_asyncio import AsyncIOMotorClient

from modbus_device import bootstrap, config
from modbus_device.adapters.redis_eventpublisher import RedisServicePublisher
from modbus_device.domain import commands
from modbus_device.config import MONGO_DB_CONN_STRING
from modbus_device.domain.model import DataModel, CreateDataModel, \
    UpdateDataModel, ModbusDevice, CreateModbusDevice, UpdateModbusDevice, \
    WriteTableResult, WriteTableRequest, ReadTableResult


def map_routers(
    app: FastAPI,
    db: str,
    redis_client: aioredis.Redis = aioredis.Redis(),
    client: AsyncIOMotorClient = AsyncIOMotorClient(MONGO_DB_CONN_STRING),
    namespace: str = "modbus",
):
    _db = getattr(client, db)

    data_model_router = CRUDRouter(
        db=_db,
        schema=DataModel,
        collection="device.data_model",
        create_schema=CreateDataModel,
        update_schema=UpdateDataModel,
        prefix="device/data_model",
    )

    app.include_router(data_model_router)

    publisher = RedisServicePublisher(client=redis_client, namespace=namespace)
    bus = bootstrap.bootstrap(publisher, namespace=namespace)

    device_router = CRUDRouter(
        db=_db,
        schema=ModbusDevice,
        collection="device",
        create_schema=CreateModbusDevice,
        update_schema=UpdateModbusDevice,
        prefix="device",
    )

    @device_router.post(
        "/{item_id}/{function}", response_model=WriteTableResult
    )
    async def write_table(
        item_id: str, function: str, request: WriteTableRequest
    ):
        device: ModbusDevice = await device_router._get_one()(item_id)
        data_model: DataModel = await data_model_router._get_one()(
            device.data_model_id
        )
        lookup = data_model.read_write_lookup
        table, address = lookup.get(function)
        if table is not None:
            cmd = commands.WriteTable(
                device.node_address, table, address, value=request.value
            )
            result = await bus.handle(cmd)
            if result is not None:
                return WriteTableResult(ok=True)
            return WriteTableResult(ok=False)
        raise NOT_FOUND

    @device_router.get("/{item_id}/{function}", response_model=ReadTableResult)
    async def read_table(item_id: str, function: str) -> ReadTableResult:
        device: ModbusDevice = await device_router._get_one()(item_id)
        data_model: DataModel = await data_model_router._get_one()(
            device.data_model_id
        )
        lookup = dict(data_model.iter_func())
        table, address = lookup.get(function)
        if table is not None:
            cmd = commands.ReadTable(device.node_address, table, address)
            result = await bus.handle(cmd)
            if result is not None:
                return ReadTableResult(value=int(result))
            return ReadTableResult(value=-1)
        raise NOT_FOUND

    app.include_router(device_router)

    @app.on_event("shutdown")
    async def shutdown_event():
        await publisher.client.close()

    return app, publisher
