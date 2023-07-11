from base64 import urlsafe_b64encode

from codercore.lib.collection import Direction

from coderfastapi.lib.validation.schemas.pagination import CursorSchema


def test_cursor_schema_load():
    last_id = "A"
    last_value = 1
    direction = Direction.ASC
    schema = CursorSchema(
        last_id=last_id,
        last_value=last_value,
        direction=direction,
    )
    assert schema.last_id == last_id
    assert schema.last_value == last_value
    assert schema.direction == direction


def test_cursor_schema_validate():
    schema = CursorSchema(last_id="A", last_value=1, direction="asc")
    assert CursorSchema.validate(schema) == schema


def test_cursor_schema_validate_from_base64_str():
    schema = CursorSchema(last_id="A", last_value=1, direction="asc")
    assert CursorSchema.validate(str(schema)) == schema


def test_cursor_schema_validate_from_base64_bytes():
    schema = CursorSchema(last_id="A", last_value=1, direction="asc")
    assert CursorSchema.validate(bytes(schema)) == schema


def test_cursor_schema_bytes():
    schema = CursorSchema(last_id="A", last_value=1, direction="asc")
    assert bytes(schema) == schema.encode()


def test_cursor_schema_str():
    schema = CursorSchema(last_id="A", last_value=1, direction="asc")
    assert str(schema) == schema.encode().decode()


def test_cursor_schema_repr():
    schema = CursorSchema(last_id="A", last_value=1, direction="asc")
    assert repr(schema) == str(
        {
            "last_id": schema.last_id,
            "last_value": schema.last_value,
            "direction": schema.direction,
        }
    )


def test_cursor_schema_encode():
    schema = CursorSchema(last_id="A", last_value=1, direction="asc")
    expected_bytes = urlsafe_b64encode(schema.json().encode())
    assert schema.encode() == expected_bytes


def test_cursor_schema_decode():
    schema = CursorSchema(last_id="A", last_value=1, direction="asc")
    assert schema.decode(schema.encode()) == schema
