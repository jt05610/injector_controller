import asyncio
from typing import Any

import async_timeout

from modbus_device.adapters.redis_eventpublisher import RedisServicePublisher


class MockRedisService(RedisServicePublisher):
    def __init__(self):
        namespace = "mockbus"
        tables = (
            "coils",
            "discrete_inputs",
            "holding_registers",
            "input_registers",
        )
        self._channels = tuple(map(lambda t: f"{namespace}.{t}", tables))
        req_channels = map(lambda c: f"{c}.req", self._channels)
        expect_channels = map(lambda c: f"{c}.expect", self._channels)

        self.channels = tuple(req_channels) + tuple(expect_channels)
        self.expects = {c: None for c in self._channels}

        super(MockRedisService, self).__init__(
            namespace=namespace, *self.channels
        )

    def expect(self, channel: str, value):
        self.expects[channel] = value

    async def run(self):
        await self.pubsub.subscribe(*self.channels)
        while True:
            try:
                async with async_timeout.timeout(1):
                    m = await self.pubsub.get_message(
                        ignore_subscribe_messages=True
                    )
                    if m is not None:
                        channel_split = str(m["channel"], "utf-8").split(".")
                        _chan = ".".join(channel_split)
                        req_type = channel_split.pop(-1)
                        if req_type == "expect":
                            self.expect(_chan, m["data"])
                        elif req_type == "req":
                            await self.publish(
                                f"{_chan}.res", self.expects[_chan]
                            )

                        if m["channel"] == "mockbus.stop":
                            break
                    await asyncio.sleep(0.01)
            except asyncio.TimeoutError:
                pass


async def main():
    service = MockRedisService()
    await service.run()
    await service.client.close()


if __name__ == "__main__":
    asyncio.run(main())
