import inspect

from modbus_device.adapters.redis_eventpublisher import RedisServicePublisher
from modbus_device.service_layer.messagebus import MessageBus
from modbus_device.service_layer.unit_of_work import (
    AbstractUnitOfWork,
    MongoDBUnitOfWork,
)
from modbus_device.service_layer import handlers


def bootstrap(
    uow: AbstractUnitOfWork = MongoDBUnitOfWork(),
    publisher: RedisServicePublisher = None,
    namespace: str = "modbus",
):
    if publisher is None:
        publisher = RedisServicePublisher(namespace=namespace)
    dependencies = {"uow": uow, "publisher": publisher}

    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }
    return MessageBus(
        command_handlers=injected_command_handlers,
    )


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return lambda message: handler(message, **deps)
