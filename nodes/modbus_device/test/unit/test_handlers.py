from __future__ import annotations
from typing import Any

from fakeredis import FakeRedis

from modbus_device import bootstrap
from modbus_device.adapters import redis_eventpublisher, repository
from modbus_device.service_layer.handlers import *
from modbus_device.service_layer.messagebus import MessageBus


class FakeRepository(repository.AbstractRepository):
    def __init__(self, items):
        super(FakeRepository, self).__init__()
        self._items = list(items)

    def _add(self, item: Any):
        self._items.append(item)

    def _get(self, **kwargs):
        key, value = kwargs.popitem()
        return next((i for i in self._items if getattr(i, key) == value), None)

    def list_items(self):
        return self._items


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.item_dict = {}
        self.events = []
        self.committed = False

    def __getitem__(self, item):
        self.items = FakeRepository(self.item_dict.get(item, []))
        self.item_dict[item] = self.items.list_items()
        return super().__enter__()

    def _commit(self):
        self.committed = True

    def rollback(self):
        pass


class FakeRedisServicePublisher(redis_eventpublisher.RedisServicePublisher):
    def __init__(self, *channels):
        self.client = FakeRedis()
        self.channel = channels
        super().__init__(client=self.client)
        self.pubsub = self.client.pubsub(ignore_subscribe_messages=True)
        self.pubsub.subscribe(*self.channel)

    def get_message(self):
        return next(self.pubsub.listen())


def bootstrap_test_app(publisher: FakeRedisServicePublisher):
    return bootstrap.bootstrap(uow=FakeUnitOfWork(), publisher=publisher)


def create_data_model(bus: MessageBus, ref: str):
    bus.handle(
        commands.CreateDataModel(
            ref=ref,
            discrete_inputs=("a", "b"),
            coils=("c", "d"),
            input_registers=("e", "f"),
            holding_registers=("g", "h"),
        )
    )


def create_device(bus: MessageBus, ref: str, node_address: int):
    create_data_model(bus, "abc")
    bus.handle(
        commands.CreateDevice(
            ref=ref, address=node_address, data_model_ref="abc"
        )
    )


def test_create_data_model():
    fake_service = FakeRedisServicePublisher("device.create_data_model.res")
    bus = bootstrap_test_app(fake_service)
    ref = "abc"
    create_data_model(bus, ref)
    msg = fake_service.get_message()
    assert json.loads(msg["data"]) == dict(ref=ref)


def test_create_device():
    fake_service = FakeRedisServicePublisher("device.create_device.res")
    bus = bootstrap_test_app(fake_service)
    ref = "fake_device"
    addr = 0x01
    expected = {"ref": ref, "device_channel": f"device.{ref}"}
    create_device(bus, ref, addr)
    msg = fake_service.get_message()
    assert json.loads(msg["data"]) == expected


def test_read_table():
    fake_service = FakeRedisServicePublisher("modbus.coils.read.req")
    bus = bootstrap_test_app(fake_service)
    ref = "fake_device"
    addr = 0xFF
    create_device(bus, ref, addr)
    bus.handle(
        commands.ReadTable(
            device_ref=ref,
            table="coils",
            endpoint="c",
        )
    )
    msg = fake_service.get_message()
    assert msg["data"] == b"255 0 1"


def test_write_table():
    fake_service = FakeRedisServicePublisher("modbus.coils.write.req")
    bus = bootstrap_test_app(fake_service)
    ref = "fake_device"
    addr = 0xFF
    create_device(bus, ref, addr)
    bus.handle(
        commands.WriteTable(
            device_ref=ref, table="coils", endpoint="c", value=1
        )
    )
    msg = fake_service.get_message()
    assert msg["data"] == b"255 0 1"


def test_process_table_read_response():
    fake_service = FakeRedisServicePublisher(
        "device.fake_device.coils.read.res"
    )
    bus = bootstrap_test_app(fake_service)
    ref = "fake_device"
    addr = 0xFF
    create_device(bus, ref, addr)
    bus.handle(
        commands.ProcessTableReadResponse(
            node_address=addr, table="coils", table_address=0x00, value=1
        )
    )
    msg = fake_service.get_message()
    expected = dict(
        device_ref=ref, table="coils", address=0x00, function="c", value=1
    )
    assert json.loads(msg["data"]) == expected


def test_process_table_write_response():
    fake_service = FakeRedisServicePublisher(
        "device.fake_device.coils.write.res"
    )
    bus = bootstrap_test_app(fake_service)
    ref = "fake_device"
    addr = 0xFF
    create_device(bus, ref, addr)
    bus.handle(
        commands.ProcessTableWriteResponse(
            node_address=addr, table="coils", table_address=0x00, value=1
        )
    )
    msg = fake_service.get_message()
    expected = dict(
        device_ref=ref, table="coils", address=0x00, function="c", value=1
    )
    assert json.loads(msg["data"]) == expected
