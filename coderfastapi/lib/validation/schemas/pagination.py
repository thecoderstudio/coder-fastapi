from typing import Annotated

from codercore.db.pagination import Cursor
from pydantic import BeforeValidator

SerializableCursor = Annotated[Cursor, BeforeValidator(lambda v: _serialize(v))]


def _serialize(v: Cursor | str | bytes) -> Cursor:
    if isinstance(v, str):
        return Cursor.decode(v.encode())
    elif isinstance(v, bytes):
        return Cursor.decode(v)
    return v
