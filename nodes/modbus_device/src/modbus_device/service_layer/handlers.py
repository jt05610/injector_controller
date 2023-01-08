from __future__ import annotations

import asyncio
import json
from dataclasses import asdict

import aioredis.client
import async_timeout

from modbus_device.domain import commands, events, model
from . import unit_of_work
from ..adapters.redis_eventpublisher import RedisServicePublisher


async def _reader(_channel: aioredis.client.PubSub):
    while True:
        try:
            async with async_timeout.timeout(1):
                message = await _channel.get_message(
                    ignore_subscribe_messages=True
                )
                if message is not None:
                    return message
            await asyncio.sleep(0.01)
        except asyncio.TimeoutError:
            break


async def read_table(
    cmd: commands.ReadTable,
    publisher: RedisServicePublisher,
):
    pdu = model.read_table(cmd.table, cmd.node_address, cmd.address)
    channel = ".".join((cmd.table, "read"))

    async with publisher.pubsub as p:
        await p.subscribe(f"{publisher.namespace}.{channel}.res")
        await publisher.publish_request(channel, pdu)
        msg = await _reader(p)
        await p.unsubscribe(f"{publisher.namespace}.{channel}.res")
    if msg is not None:
        return msg["data"]
    else:
        return None


async def write_table(
    cmd: commands.WriteTable,
    publisher: RedisServicePublisher,
):
    pdu = model.write_table(
        cmd.table, cmd.node_address, cmd.address, cmd.value
    )
    channel = ".".join((cmd.table, "write"))
    async with publisher.pubsub as p:
        await p.subscribe(f"{publisher.namespace}.{channel}.res")
        await publisher.publish_request(channel, pdu)
        msg = await _reader(p)
        await p.unsubscribe(f"{publisher.namespace}.{channel}.res")
    if msg is not None:
        return msg["data"]
    else:
        return None


COMMAND_HANDLERS = {
    commands.ReadTable: read_table,
    commands.WriteTable: write_table,
}
