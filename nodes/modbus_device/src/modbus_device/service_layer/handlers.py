from __future__ import annotations

import json
from dataclasses import asdict

from modbus_device.domain import commands, events, model
from . import unit_of_work
from ..adapters.redis_eventpublisher import RedisServicePublisher


def create_data_model(
    cmd: commands.CreateDataModel,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow["data_model"] as collection:
        collection.items.add(model.data_model(**asdict(cmd)))
        uow.events.append(events.DataModelCreated(cmd.ref))


def create_device(
    cmd: commands.CreateDevice,
    uow: unit_of_work.AbstractUnitOfWork,
):

    with uow["data_model"] as collection:
        dm = collection.items.get(ref=cmd.data_model_ref)
    with uow["devices"] as collection:
        collection.items.add(
            model.ModbusDevice(
                ref=cmd.ref, node_address=cmd.address, data_model=dm
            )
        )
        uow.events.append(
            events.DeviceCreated(cmd.ref, device_channel=f"device.{cmd.ref}")
        )


def read_table(
    cmd: commands.ReadTable,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow["devices"] as collection:
        device = collection.items.get(ref=cmd.device_ref)
        pdu = model.read_table(
            getattr(device.data_model, cmd.table),
            device.node_address,
            cmd.endpoint,
        )
        uow.events.append(events.TableReadRequested(cmd.table, pdu))


def write_table(
    cmd: commands.WriteTable,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow["devices"] as collection:
        device = collection.items.get(ref=cmd.device_ref)
        pdu = model.write_table(
            getattr(device.data_model, cmd.table),
            device.node_address,
            cmd.endpoint,
            cmd.value,
        )
        uow.events.append(events.TableWriteRequested(cmd.table, pdu))


def process_read_table_response(
    cmd: commands.ProcessTableReadResponse,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow["devices"] as collection:
        device = collection.items.get(node_address=cmd.node_address)
        uow.events.append(
            events.TableRead(
                device_ref=device.ref,
                table=cmd.table,
                address=cmd.table_address,
                function=getattr(device.data_model, cmd.table).addresses[
                    cmd.table_address
                ],
                value=cmd.value,
            )
        )


def process_write_table_response(
    cmd: commands.ProcessTableWriteResponse,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow["devices"] as collection:
        device = collection.items.get(node_address=cmd.node_address)
        uow.events.append(
            events.TableWritten(
                device_ref=device.ref,
                table=cmd.table,
                address=cmd.table_address,
                function=getattr(device.data_model, cmd.table).addresses[
                    cmd.table_address
                ],
                value=cmd.value,
            )
        )


def publish_read_request(
    event: events.TableReadRequested,
    publisher: RedisServicePublisher,
):
    channel = ".".join((event.table, "read"))
    publisher.publish_request(channel=channel, message=event.pdu)


def publish_read_response(
    event: events.TableRead,
    publisher: RedisServicePublisher,
):
    publisher.publish_response(
        channel=f"{event.device_ref}.{event.table}.read",
        message=json.dumps(asdict(event)),
    )


def publish_write_response(
    event: events.TableWritten,
    publisher: RedisServicePublisher,
):
    publisher.publish_response(
        channel=f"{event.device_ref}.{event.table}.write",
        message=json.dumps(asdict(event)),
    )


def publish_write_request(
    event: events.TableWriteRequested,
    publisher: RedisServicePublisher,
):
    publisher.publish_request(
        channel=".".join((event.table, "write")), message=event.pdu
    )


def publish_device_created(
    event: events.DeviceCreated,
    publisher: RedisServicePublisher,
):
    publisher.publish_response(
        channel="create_device",
        message=json.dumps(asdict(event)),
    )


def publish_data_model_created(
    event: events.DataModelCreated,
    publisher: RedisServicePublisher,
):
    publisher.publish_response(
        channel="create_data_model",
        message=json.dumps(asdict(event)),
    )


EVENT_HANDLERS = {
    events.TableRead: [publish_read_response],
    events.TableWritten: [publish_write_response],
    events.TableReadRequested: [publish_read_request],
    events.TableWriteRequested: [publish_write_request],
    events.DeviceCreated: [publish_device_created],
    events.DataModelCreated: [publish_data_model_created],
}

COMMAND_HANDLERS = {
    commands.ReadTable: read_table,
    commands.WriteTable: write_table,
    commands.ProcessTableReadResponse: process_read_table_response,
    commands.ProcessTableWriteResponse: process_write_table_response,
    commands.CreateDataModel: create_data_model,
    commands.CreateDevice: create_device,
}
