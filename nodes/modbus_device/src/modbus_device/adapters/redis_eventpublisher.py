import logging

import aioredis
from modbus_device import config


class RedisPublisher:
    logger = logging.getLogger(__name__)
    client: aioredis.Redis

    async def publish(self, channel: str, message: str):
        self.logger.debug(f"publishing {message} to {channel}")
        await self.client.publish(channel, message)


class RedisServicePublisher(RedisPublisher):
    namespace: str

    def __init__(
        self,
        *sub_channels,
        client: aioredis.Redis = aioredis.Redis(),
        namespace: str = config.REDIS_NAMESPACE,
    ):
        if len(sub_channels):
            self.channels = sub_channels
        else:
            self.channels = [
                f"{namespace}.coils.read.res",
                f"{namespace}.discrete_inputs.read.res",
                f"{namespace}.input_registers.read.res",
                f"{namespace}.holding_registers.read.res",
                f"{namespace}.coils.write.res",
                f"{namespace}.holding_registers.write.res",
            ]
        self.client = client
        self.pubsub = self.client.pubsub(ignore_subscribe_messages=True)
        self.namespace = namespace

    async def publish_request(self, channel: str, message: str):
        full_channel = ".".join((self.namespace, channel, "req"))
        await self.publish(channel=full_channel, message=message)

    async def publish_response(self, channel: str, message: str):
        full_channel = ".".join((self.namespace, channel, "res"))
        await self.publish(channel=full_channel, message=message)
