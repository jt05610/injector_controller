from abc import ABC, abstractmethod
from typing import Any, Mapping

from pymongo.database import Database


class AbstractRepository(ABC):
    def add(self, item: Any):
        self._add(item)

    def get(self, **kwargs):
        item = self._get(**kwargs)
        return item

    @abstractmethod
    def _add(self, item: Any):
        raise NotImplementedError

    @abstractmethod
    def _get(self, **kwargs):
        raise NotImplementedError


class MongoDBRepository(AbstractRepository):
    session: Database[Mapping[str, Any]]

    def __init__(self, session: Database[Mapping[str, Any]]):
        self.session = session

    def _add(self, item: Any):
        self.session.insert_one(item)

    def _get(self, **kwargs):
        return self.session.find(kwargs)
