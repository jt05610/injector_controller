from typing import Type, Optional, Union, List, Any, Callable, Coroutine

from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from fastapi_crudrouter.core import CRUDGenerator, NOT_FOUND
from fastapi_crudrouter.core._types import (
    DEPENDENCIES,
    PYDANTIC_SCHEMA,
    PAGINATION,
)

from modbus_device.adapters.repository import MongoDBRepository
CALLABLE = Callable[..., Coroutine[Any, Any, PYDANTIC_SCHEMA]]
CALLABLE_LIST = Callable[..., Coroutine[Any, Any, List[PYDANTIC_SCHEMA]]]


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
        self.repo = MongoDBRepository(self.db[self.tbl], schema)

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
        ) -> List[PYDANTIC_SCHEMA]:
            skip, limit = pagination.get("skip"), pagination.get("limit")
            return await self.repo.get_all(skip=skip, limit=limit)
        return route

    def _get_one(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(item_id: str) -> PYDANTIC_SCHEMA:
            item = await self.repo.get_one(item_id=item_id)
            if item is not None:
                return item
            else:
                raise NOT_FOUND

        return route

    def _create(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(
            model: self.create_schema,  # type: ignore
        ) -> PYDANTIC_SCHEMA:
            _model = jsonable_encoder(model)
            return await self.repo.insert(_model)

        return route

    def _update(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(
            item_id: str, model: self.update_schema  # type: ignore
        ) -> PYDANTIC_SCHEMA:
            update = {k: v for k, v in model.dict().items() if v is not None}
            if len(update):
                _model = await self.repo.get_one(item_id=item_id)
                return await self.repo.update(_model, **update)
            raise NOT_FOUND

        return route

    def _delete_all(self, *args: Any, **kwargs: Any) -> CALLABLE_LIST:
        async def route() -> List[PYDANTIC_SCHEMA]:
            await self.repo.delete_all()
            return await self._get_all()(pagination={"skip": 0, "limit": None})

        return route

    def _delete_one(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(item_id: str) -> PYDANTIC_SCHEMA:
            return await self.repo.delete_one(item_id=item_id)
        return route
