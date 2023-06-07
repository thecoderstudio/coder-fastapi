from base64 import urlsafe_b64decode, urlsafe_b64encode
from typing import Any, Callable, Iterator, Self

from codercore.db.pagination import Cursor
from codercore.lib.collection import Direction
from pydantic import BaseModel


class CursorSchema(BaseModel, Cursor):
    last_id: Any
    last_value: Any
    direction: Direction

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable]:
        yield cls.validate

    @classmethod
    def validate(cls, v: Self | str | bytes) -> Self:
        if isinstance(v, str):
            return cls.decode(v.encode())
        elif isinstance(v, bytes):
            return cls.decode(v)
        return v

    def __bytes__(self) -> bytes:
        return self.encode()

    def __str__(self) -> str:
        return self.encode().decode()

    def __repr__(self) -> str:
        return str(self._dict())

    def _dict(self) -> dict[str, Any]:
        return {
            "last_id": self.last_id,
            "last_value": self.last_value,
            "direction": self.direction,
        }

    def encode(self) -> bytes:
        return urlsafe_b64encode(self.json().encode())

    @staticmethod
    def decode(v: bytes) -> Self:
        return CursorSchema.parse_raw(urlsafe_b64decode(v))
