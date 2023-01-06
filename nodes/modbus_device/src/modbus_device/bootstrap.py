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
    publisher: RedisServicePublisher = RedisServicePublisher(),
):
    dependencies = {"uow": uow, "publisher": publisher}
    injected_event_handlers = {
        event_type: [
            inject_dependencies(handler, dependencies)
            for handler in event_handlers
        ]
        for event_type, event_handlers in handlers.EVENT_HANDLERS.items()
    }
    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }
    return MessageBus(
        uow=uow,
        event_handlers=injected_event_handlers,
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
