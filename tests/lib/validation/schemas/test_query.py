import uuid

import pytest

from coderfastapi.lib.validation.schemas.pagination import CursorSchema
from coderfastapi.lib.validation.schemas.query import (
    DEFAULT_LIMIT,
    MAX_LIMIT,
    QueryParameters,
)


def test_query_parameters_load():
    cursor = CursorSchema(
        last_id=str(uuid.uuid4()),
        last_value="a",
        direction="asc",
    )
    limit = 10
    schema = QueryParameters(
        cursor=str(cursor),
        limit=limit,
    )
    assert schema.cursor == cursor
    assert limit == limit


def test_query_parameters_load_defaults():
    schema = QueryParameters()
    assert schema.cursor is None
    assert schema.limit == DEFAULT_LIMIT


@pytest.mark.parametrize("limit", (0, MAX_LIMIT + 1))
def test_query_parameters_limit_out_of_bounds(limit):
    with pytest.raises(ValueError) as e:
        QueryParameters(limit=limit)
    assert e.value.errors() == [
        {
            "loc": ("limit",),
            "msg": f"ensure limit is >= 1 and <= {MAX_LIMIT}",
            "type": "value_error",
        }
    ]
