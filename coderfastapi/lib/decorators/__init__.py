from functools import wraps
from http import HTTPStatus
from typing import Awaitable, Callable, TypeVar

from fastapi import HTTPException

from coderfastapi.lib.decorators.pagination import paginate  # noqa

T = TypeVar("T")


def http_require(
    entity_name: str, boolean: bool = False
) -> Callable[[Callable[..., Awaitable[T | None]]], Callable[..., Awaitable[T]]]:
    """Decorator that raises HTTP 404 if the wrapped function returns None.

    When boolean=True, checks for False instead of None.
    """

    def decorate(
        func: Callable[..., Awaitable[T | None]],
    ) -> Callable[..., Awaitable[T]]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            entity = await func(*args, **kwargs)
            if boolean:
                if entity is True:
                    return entity
            else:
                if entity is not None:
                    return entity
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"The {entity_name} is not found.",
            )

        return wrapper

    return decorate
