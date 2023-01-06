import logging

import redis
from modbus_device import config
from modbus_device.domain import commands


class RedisPublisher:
    namespace: str

    def __init__(
        self, client: redis.Redis = redis.Redis(**config.REDIS_DEFAULT)
    ):
        self.logger = logging.getLogger(__name__)
        self.client = client

    def publish(self, channel: str, message: str):
        self.logger.info(f"publishing {message} on {channel}")
        self.client.publish(channel, message)


class RedisServicePublisher(RedisPublisher):
    namespace: str

    def __init__(
        self,
        client: redis.Redis = redis.Redis(**config.REDIS_DEFAULT),
        namespace: str = config.REDIS_NAMESPACE,
    ):
        super().__init__(client)
        self.namespace = namespace

    def publish_request(self, channel: str, message: str):
        full_channel = ".".join(("modbus", channel, "req"))

        self.publish(channel=full_channel, message=message)

    def publish_response(self, channel: str, message: str):
        full_channel = ".".join((self.namespace, channel, "res"))
        self.publish(channel=full_channel, message=message)
