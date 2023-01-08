from __future__ import annotations
import logging
from typing import Callable, Dict, List, Union, Type, TYPE_CHECKING
from modbus_device.domain import commands, events

if TYPE_CHECKING:
    from . import unit_of_work

logger = logging.getLogger(__name__)

Message = Union[commands.Command, events.Event]


class MessageBus:
    def __init__(
        self,
        command_handlers: Dict[Type[commands.Command], Callable],
    ):
        self.queue: List[Message] = []
        self.command_handlers = command_handlers

    async def handle(self, command: commands.Command):
        logger.debug(f"handling command {command}")
        try:
            handler = self.command_handlers[type(command)]
            return await handler(command)
        except Exception:
            msg = f"Exception handling command {command}"
            logger.exception(msg)
            raise Exception(msg)
