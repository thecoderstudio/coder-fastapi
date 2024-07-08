import json
from dataclasses import asdict
from typing import Annotated, Self

from codercore.db.pagination import Cursor as BaseCursor
from fastapi.encoders import jsonable_encoder
from pydantic import BeforeValidator


class Cursor(BaseCursor):
    def _json_dumps(self) -> str:
        return json.dumps(jsonable_encoder(asdict(self)))

    @classmethod
    def decode(cls, v: bytes) -> Self:
        return Cursor(**cls._json_loads(v))


DeserializableCursor = Annotated[Cursor, BeforeValidator(lambda v: _deserialize(v))]


def _deserialize(v: Cursor | str | bytes) -> Cursor:
    if isinstance(v, str):
        return Cursor.decode(v.encode())
    elif isinstance(v, bytes):
        return Cursor.decode(v)
    return v
