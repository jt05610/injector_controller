from __future__ import annotations
from abc import ABC, abstractmethod
from collections import Mapping
from typing import Any, Callable

from pymongo import MongoClient
from pymongo.database import Database

from modbus_device import config
from modbus_device.adapters import repository


class AbstractUnitOfWork(ABC):
    items: repository.AbstractRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    def collect_new_events(self):
        for item in self.items.seen:
            while item.events:
                yield item.events.pop(0)

    @abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


def mongo_db_session(
    collection: str, conn_string: str = config.MONGO_DB_CONN_STRING
) -> Database[Mapping[str, Any]]:
    client = MongoClient(conn_string)
    return client[collection]


class MongoDBUnitOfWork(AbstractUnitOfWork):
    session: Database[Mapping[str, Any]]

    def __init__(
        self, collection: str, session_factory: Callable = mongo_db_session
    ):
        self.session_factory = session_factory
        self.collection = collection

    def __enter__(self):
        self.session = self.session_factory()
        self.items = repository.MongoDBRepository(self.session)

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        pass

    def rollback(self):
        pass
