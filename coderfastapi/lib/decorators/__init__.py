from functools import wraps
from http import HTTPStatus
from typing import Awaitable, Callable, Optional, TypeVar

from fastapi import HTTPException

from coderfastapi.lib.decorators.pagination import paginate  # noqa

T = TypeVar("T")


def http_require(
    entity_name: str,
) -> Callable[[Callable[..., Awaitable[Optional[T]]]], Callable[..., Awaitable[T]]]:
    def decorate(
        func: Callable[..., Awaitable[Optional[T]]]
    ) -> Callable[..., Awaitable[T]]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            entity = await func(*args, **kwargs)
            if entity is None:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail=f"The {entity_name} is not found.",
                )
            return entity

        return wrapper

    return decorate
