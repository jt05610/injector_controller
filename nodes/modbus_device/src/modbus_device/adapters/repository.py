from abc import ABC, abstractmethod
from typing import Any, Mapping

from pymongo.database import Database


class AbstractRepository(ABC):
    def __init__(self):
        self.seen = set()

    def add(self, item: Any):
        self._add(item)
        self.seen.add(item)

    def get(self, **kwargs):
        item = self._get(**kwargs)
        if item:
            self.seen.add(item)
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
        super(MongoDBRepository, self).__init__()
        self.session = session

    def _add(self, item: Any):
        self.session.insert_one(item)

    def _get(self, **kwargs):
        return self.session.find(kwargs)
