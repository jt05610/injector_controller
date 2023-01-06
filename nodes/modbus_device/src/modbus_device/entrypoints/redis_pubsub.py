from modbus_device.entrypoints.redis_subscriber import RedisSubscriber
from modbus_device.adapters.redis_eventpublisher import RedisPublisher


class RedisPubsub:
    def __init__(self, publisher: RedisPublisher, subscriber: RedisSubscriber):
        self.publisher = publisher
        self.subscriber = subscriber
