from codercore.lib.collection import Direction
from pydantic import BaseModel, validator

from coderfastapi.lib.validation.schemas.pagination import CursorSchema

MAX_LIMIT = 100
DEFAULT_LIMIT = 25
DEFAULT_ORDER_BY = "id"
ORDERABLE_PROPERTIES = (DEFAULT_ORDER_BY,)


class QueryParameters(BaseModel):
    _max_limit: int = MAX_LIMIT

    cursor: CursorSchema | None = None
    limit: int = DEFAULT_LIMIT

    @validator("limit")
    def limit_within_bounds(cls, v: int) -> int:
        if v < 1 or v > cls._max_limit:
            raise ValueError(f"ensure limit is >= 1 and <= {cls._max_limit}")
        return v


class OrderableQueryParameters(QueryParameters):
    _orderable_properties: tuple[str] = ORDERABLE_PROPERTIES

    order_by: str = DEFAULT_ORDER_BY
    order_direction: Direction = Direction.DESC

    @validator("order_by")
    def validate_order_by(cls, v: str) -> str:
        if v in cls._orderable_properties:
            return v
        raise ValueError(f"order_by must be one of {cls._orderable_properties}")
