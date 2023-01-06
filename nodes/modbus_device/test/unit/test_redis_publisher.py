from pytest import fixture
from fakeredis import FakeRedis
from modbus_device.adapters.redis_eventpublisher import RedisModbusPublisher
from modbus_device.domain import commands

fake_sub = FakeRedis()


@fixture()
def fake_redis():
    return FakeRedis()


@fixture()
def fake_redis_modbus_service(fake_redis):
    return RedisModbusPublisher(client=fake_redis)


@fixture()
def pub_test(fake_redis):

    pub = RedisModbusPublisher(client=fake_redis)
    sub = fake_redis.pubsub(ignore_subscribe_messages=True)

    def _test(function: str, table: str, read_write: str, req_or_res: str):
        channel = f"modbus.{table}.{read_write}.{req_or_res}"
        sub.subscribe(channel)
        message = "1 0 1"
        command = commands.ReadTable(table, pdu=message)
        getattr(pub, function)(command)
        actual = next(sub.listen())
        assert actual["channel"] == bytes(channel, "utf-8")
        assert actual["data"] == bytes(message, "utf-8")

    return _test


def test_publisher(pub_test):
    tests = (
        ("publish_read_table_request", "coils", "read", "req"),
        ("publish_read_table_response", "coils", "read", "res"),
        ("publish_write_table_request", "coils", "write", "req"),
        ("publish_write_table_response", "coils", "write", "res"),
    )
    for test in tests:
        pub_test(*test)
