from typing import Annotated

from codercore.db.pagination import Cursor
from pydantic import BeforeValidator

DeserializableCursor = Annotated[Cursor, BeforeValidator(lambda v: _deserialize(v))]


def _deserialize(v: Cursor | str | bytes) -> Cursor:
    if isinstance(v, str):
        return Cursor.decode(v.encode())
    elif isinstance(v, bytes):
        return Cursor.decode(v)
    return v
