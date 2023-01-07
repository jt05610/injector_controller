from typing import Type, Optional, Union, List, Any, Callable, Coroutine

from fastapi.encoders import jsonable_encoder
from fastapi_crudrouter.core import CRUDGenerator, NOT_FOUND
from fastapi_crudrouter.core._types import (
    DEPENDENCIES,
    PYDANTIC_SCHEMA,
    PAGINATION,
)

from pydantic import BaseModel

CALLABLE = Callable[..., Coroutine[Any, Any, BaseModel]]
CALLABLE_LIST = Callable[..., Coroutine[Any, Any, List[BaseModel]]]


class MongoDBCRUDRouter(CRUDGenerator[PYDANTIC_SCHEMA]):
    def __init__(
        self,
        schema: Type[PYDANTIC_SCHEMA],
        collection: str,
        db,
        create_schema: Optional[Type[PYDANTIC_SCHEMA]] = None,
        update_schema: Optional[Type[PYDANTIC_SCHEMA]] = None,
        prefix: Optional[str] = None,
        tags: Optional[List[str]] = None,
        paginate: Optional[int] = None,
        get_all_route: Union[bool, DEPENDENCIES] = True,
        get_one_route: Union[bool, DEPENDENCIES] = True,
        create_route: Union[bool, DEPENDENCIES] = True,
        update_route: Union[bool, DEPENDENCIES] = True,
        delete_one_route: Union[bool, DEPENDENCIES] = True,
        delete_all_route: Union[bool, DEPENDENCIES] = True,
        **kwargs: Any,
    ) -> None:
        self.db = db
        self.tbl = collection

        super().__init__(
            schema=schema,
            create_schema=create_schema or schema,
            update_schema=update_schema or schema,
            prefix=prefix,
            tags=tags,
            paginate=paginate,
            get_all_route=get_all_route,
            get_one_route=get_one_route,
            create_route=create_route,
            update_route=update_route,
            delete_one_route=delete_one_route,
            delete_all_route=delete_all_route,
            **kwargs,
        )

    def _get_all(self, *args: Any, **kwargs: Any) -> CALLABLE_LIST:
        async def route(
            pagination: PAGINATION = self.pagination,
        ) -> List[BaseModel]:
            skip, limit = pagination.get("skip"), pagination.get("limit")
            items: List[BaseModel] = (
                await self.db[self.tbl].find().to_list(limit)
            )
            return items

        return route

    def _get_one(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(item_id: int) -> PYDANTIC_SCHEMA:
            item = await self.db[self.tbl].find_one({"_id": item_id})
            if item:
                return item
            else:
                raise NOT_FOUND

        return route

    def _create(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(
            model: self.create_schema,  # type: ignore
        ) -> BaseModel:
            item = jsonable_encoder(model)
            new_item = await self.db[self.tbl].insert_one(item)
            created_item = await self.db[self.tbl].find_one(
                {"_id": new_item.inserted_id}
            )
            return created_item

        return route

    def _update(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(
            item_id: int, model: self.update_schema  # type: ignore
        ) -> PYDANTIC_SCHEMA:
            item = {k: v for k, v in model.dict().items() if v is not None}
            if len(item) >= 1:
                update_result = await self.db[self.tbl].update_one(
                    {"_id": item_id}, {"$set": item}
                )

                if update_result.modified_count == 1:
                    return await self.db[self.tbl].find_one({"_id": item_id})

                return await self.db[self.tbl].find_one({"_id": item_id})

            raise NOT_FOUND

        return route

    def _delete_all(self, *args: Any, **kwargs: Any) -> CALLABLE_LIST:
        async def route() -> List[PYDANTIC_SCHEMA]:
            return await self.db[self.tbl].delete()

        return route

    def _delete_one(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(item_id: int) -> PYDANTIC_SCHEMA:
            return await self.db[self.tbl].delete_one({"_id": item_id})

        return route
