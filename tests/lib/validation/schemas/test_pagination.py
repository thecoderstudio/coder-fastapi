import json
import uuid
from base64 import urlsafe_b64encode
from dataclasses import asdict

from codercore.lib.collection import Direction
from fastapi.encoders import jsonable_encoder
from pydantic import TypeAdapter

from coderfastapi.lib.validation.schemas.pagination import DeserializableCursor


def test_deserializable_cursor_init():
    last_id = "A"
    last_value = 1
    direction = Direction.ASC
    cursor = DeserializableCursor(
        last_id=last_id,
        last_value=last_value,
        direction=direction,
    )
    assert cursor.last_id == last_id
    assert cursor.last_value == last_value
    assert cursor.direction == direction


def test_deserializable_cursor_encode():
    cursor = DeserializableCursor(last_id=uuid.uuid4(), last_value=1, direction="asc")
    expected_bytes = urlsafe_b64encode(
        json.dumps(jsonable_encoder(asdict(cursor))).encode()
    )
    assert cursor.encode() == expected_bytes


def test_deserializable_cursor_decode():
    cursor = DeserializableCursor(last_id=uuid.uuid4(), last_value=1, direction="asc")
    assert cursor.decode(cursor.encode()) == DeserializableCursor(
        last_id=str(cursor.last_id),
        last_value=cursor.last_value,
        direction=cursor.direction,
    )


def test_deserializable_cursor_deserialize():
    type_adapter = TypeAdapter(DeserializableCursor)
    cursor = DeserializableCursor(last_id="A", last_value=1, direction="asc")
    assert type_adapter.validate_python(cursor) == cursor


def test_deserializable_cursor_deserialize_from_base64_str():
    type_adapter = TypeAdapter(DeserializableCursor)
    cursor = DeserializableCursor(last_id="A", last_value=1, direction="asc")
    assert type_adapter.validate_python(str(cursor)) == cursor


def test_deserializable_cursor_deserialize_from_base64_bytes():
    type_adapter = TypeAdapter(DeserializableCursor)
    cursor = DeserializableCursor(last_id="A", last_value=1, direction="asc")
    assert type_adapter.validate_python(bytes(cursor)) == cursor
