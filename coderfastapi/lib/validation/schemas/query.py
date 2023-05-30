from pydantic import BaseModel, validator

from coderfastapi.lib.validation.schemas.pagination import CursorSchema

MAX_LIMIT = 100
DEFAULT_LIMIT = 25


class QueryParameters(BaseModel):
    _max_limit: int = MAX_LIMIT

    cursor: CursorSchema | None = None
    limit: int = DEFAULT_LIMIT

    @validator("limit")
    def limit_within_bounds(cls, v: int) -> int:
        if v < 1 or v > cls._max_limit:
            raise ValueError(f"ensure limit is >= 1 and <= {cls._max_limit}")
        return v
