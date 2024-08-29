import uuid

import pytest
from codercore.lib.collection import Direction
from codercore.test.pydantic import check_validation_value_error

from coderfastapi.lib.validation.schemas.pagination import DeserializableCursor
from coderfastapi.lib.validation.schemas.query import (
    DEFAULT_LIMIT,
    MAX_LIMIT,
    ORDERABLE_PROPERTIES,
    OrderableQueryParameters,
    QueryParameters,
)


def test_query_parameters_load():
    cursor = DeserializableCursor(
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
    assert check_validation_value_error(
        e.value,
        ("limit",),
        f"ensure limit is >= 1 and <= {MAX_LIMIT}",
        limit,
    )


def test_orderable_query_parameters_load():
    schema = OrderableQueryParameters(order_direction=Direction.ASC, order_by="id")
    assert schema.cursor is None
    assert schema.limit == DEFAULT_LIMIT
    assert schema.order_direction == Direction.ASC
    assert schema.order_by == "id"


def test_orderable_query_parameters_load_order_by_multiple():
    class ModifiedQueryParams(OrderableQueryParameters):
        _orderable_properties = ("id", "foo", "bar")

    schema = ModifiedQueryParams(order_by=["bar", "foo"])
    assert schema.order_by == ("bar", "foo")


def test_orderable_query_parameters_load_defaults():
    schema = OrderableQueryParameters()
    assert schema.cursor is None
    assert schema.limit == DEFAULT_LIMIT
    assert schema.order_direction == Direction.DESC
    assert schema.order_by == "id"


def test_orderable_query_parameters_invalid_order_by():
    with pytest.raises(ValueError) as e:
        OrderableQueryParameters(order_by="wrong")

    assert check_validation_value_error(
        e.value,
        ("order_by",),
        f"order_by must be one of {ORDERABLE_PROPERTIES}",
        "wrong",
    )
