from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Callable, Mapping

from pymongo import MongoClient
from pymongo.database import Database

from modbus_device import config
from modbus_device.adapters import repository


class AbstractUnitOfWork(ABC):
    items: repository.AbstractRepository
    events: list

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    def __getitem__(self, item):
        raise NotImplementedError

    def commit(self):
        self._commit()

    def collect_new_events(self):
        while self.events:
            yield self.events.pop(0)

    @abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


def mongo_db_session(conn_string: str = config.MONGO_DB_CONN_STRING):
    def factory(collection: str) -> Database[Mapping[str, Any]]:
        client = MongoClient(conn_string)
        return client[collection]

    return factory


class MongoDBUnitOfWork(AbstractUnitOfWork):
    session: Database[Mapping[str, Any]]

    def __init__(self, session_factory: Callable = mongo_db_session):
        self.session_factory = session_factory
        self.events = []

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        pass

    def rollback(self):
        pass

    def __getitem__(self, item: str) -> MongoDBUnitOfWork:
        self.session = self.session_factory(item)
        self.items = repository.MongoDBRepository(self.session)
        return super().__enter__()
