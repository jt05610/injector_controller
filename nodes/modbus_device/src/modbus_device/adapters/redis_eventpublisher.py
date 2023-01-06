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
    def __init__(
        self, client: redis.Redis = redis.Redis(**config.REDIS_DEFAULT)
    ):
        super().__init__(client)

    def publish_request(self, channel: str, message: str):
        self.publish(
            channel=f"{self.namespace}.{channel}.req", message=message
        )

    def publish_response(self, channel: str, message: str):
        self.publish(
            channel=f"{self.namespace}.{channel}.res", message=message
        )


class RedisModbusPublisher(RedisServicePublisher):
    namespace = "modbus"

    def __init__(
        self, client: redis.Redis = redis.Redis(**config.REDIS_DEFAULT)
    ):
        super().__init__(client)

    @staticmethod
    def _read_channel(table: str):
        return f"{table}.read"

    @staticmethod
    def _write_channel(table: str):
        return f"{table}.write"

    def publish_read_table_request(self, command: commands.ReadTable):
        self.publish_request(self._read_channel(command.table), command.pdu)

    def publish_read_table_response(self, command: commands.ReadTable):
        self.publish_response(self._read_channel(command.table), command.pdu)

    def publish_write_table_request(self, command: commands.WriteTable):
        self.publish_request(self._write_channel(command.table), command.pdu)

    def publish_write_table_response(self, command: commands.WriteTable):
        self.publish_response(self._write_channel(command.table), command.pdu)
