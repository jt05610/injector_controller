from abc import ABC, abstractmethod
from typing import Any, Mapping, Type

from bson import ObjectId
from pymongo.database import Database


class AbstractRepository(ABC):
    async def get_all(self, **kwargs) -> list:
        return await self._get_all(**kwargs)

    async def get_one(self, **kwargs) -> Any:
        return await self._get_one(**kwargs)

    async def insert(self, item: Any, **kwargs) -> Any:
        return await self._insert(item, **kwargs)

    async def update(self, item: Any, **kwargs) -> Any:
        return await self._update(item, **kwargs)

    async def delete_one(self, **kwargs) -> Any:
        return await self._delete_one(**kwargs)

    async def delete_all(self, **kwargs) -> list:
        return await self._delete_all(**kwargs)

    @abstractmethod
    async def _insert(self, item: Any, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def _update(self, item: Any, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def _get_one(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def _get_all(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def _delete_one(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def _delete_all(self, **kwargs):
        raise NotImplementedError


class MongoDBRepository(AbstractRepository):
    def __init__(self, session, base_type: Type):
        self.session = session
        self.base_type = base_type
    async def _insert(self, item: Any, **kwargs):
        new_item = await self.session.insert_one(item)
        created_item = await self.session.find_one(
            {"_id": new_item.inserted_id}
        )
        return self.base_type(**created_item)

    async def _update(self, item: Any, **kwargs):
        update_result = await self.session.update_one(
            {"_id": item.id}, {"$set": kwargs})

        if update_result.modified_count == 1:
            return await self._get_one(item_id=item.id)

        return await self._get_one(**kwargs)

    async def _get_one(self, **kwargs):
        item = await self.session.find_one(
            {"_id": ObjectId(kwargs.get("item_id"))}
        )
        return self.base_type(**item)

    async def _get_all(self, **kwargs):
        items = await self.session.find().to_list(kwargs.get("limit"))
        return list(self.base_type(**i) for i in items[kwargs.get("skip"):])

    async def _delete_one(self, **kwargs):
        item = await self._get_one(**kwargs)
        await self.session.delete_one({"_id": item.dict()["id"]})
        return item

    async def _delete_all(self, **kwargs):
        await self.session.drop()