import logging
from dataclasses import dataclass
from typing import Callable, Iterable

from redis import Redis

from modbus_device import config


@dataclass
class Subscription:
    channel: str
    callback: Callable


class RedisSubscriber:
    def __init__(
        self,
        client: Redis = Redis(**config.REDIS_DEFAULT),
        subscriptions=Iterable[Subscription],
    ):
        self.logger = logging.getLogger(__name__)
        self.client = client
        self.pubsub = self.client.pubsub(ignore_subscribe_messages=True)
        self.subscriptions = subscriptions
        self.sub_lookup = {s.channel: s for s in self.subscriptions}
        self.keep_alive = False

    def listen(self):
        self.pubsub.subscribe(*tuple(s.channel for s in self.subscriptions))
        self.keep_alive = True
        for m in self.pubsub.listen():
            if m:
                try:
                    self.sub_lookup[str(m["channel"])].callback(m["data"])
                except KeyError:
                    pass

    def kill(self):
        self.keep_alive = False
