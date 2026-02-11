from dataclasses import dataclass

import httpx
import pytest
from codercore.lib.collection import Direction
from fastapi import Depends, Request

from coderfastapi.lib.decorators import paginate
from coderfastapi.lib.validation.schemas.pagination import DeserializableCursor
from coderfastapi.lib.validation.schemas.query import (
    OrderableQueryParameters,
    QueryParameters,
)
from coderfastapi.test import assert_link_header


class ListEntityParameters(OrderableQueryParameters):
    _orderable_properties = ("value",)


@dataclass
class Entity:
    id: int
    value: str


@dataclass
class MultiIDEntity:
    id_a: str
    id_b: int
    value: str


@paginate("id")
async def decorated(
    value: list[Entity],
    params: QueryParameters = Depends(),
) -> list[Entity]:
    return value


@paginate("id_a", "id_b")
async def decorated_multi_id(
    value: list[MultiIDEntity],
    params: QueryParameters = Depends(),
) -> list[MultiIDEntity]:
    return value


@paginate("id")
async def decorated_orderable(
    value: list[Entity],
    params: ListEntityParameters = Depends(),
) -> list[Entity]:
    return value


@paginate("id")
async def decorated_not_injectable(
    value: list[Entity],
    params: QueryParameters,
) -> list[Entity]:
    return value


def create_request_mock(mocker, params: QueryParameters):
    request_mock = mocker.MagicMock()
    request_mock.query_params = params.model_dump()
    request_mock.url = httpx.URL(f"http://localhost?limit={params.limit}")
    if params.cursor:
        request_mock.url = httpx.URL(f"{request_mock.url}&cursor={params.cursor}")
    return request_mock


def create_response_mock(mocker, request: Request):
    response_mock = mocker.MagicMock()
    response_mock.headers = {}
    response_mock.request = request
    return response_mock


async def test_paginate_no_links(mocker):
    limit = 2
    request_mock = create_request_mock(
        mocker,
        QueryParameters(cursor=None, limit=limit),
    )
    response_mock = create_response_mock(mocker, request_mock)
    value = [Entity(id=1, value="a")]

    result = await decorated(request_mock, response_mock, value=value)

    assert result == value
    assert response_mock.headers == {}


@pytest.mark.parametrize("direction", (Direction.ASC, Direction.DESC))
async def test_paginate_no_links_due_to_result_size(mocker, direction):
    limit = 1
    value = []
    request_mock = create_request_mock(
        mocker,
        QueryParameters(
            cursor=DeserializableCursor(
                last_id=1,
                last_value=1,
                direction=direction,
            ),
            limit=limit,
        ),
    )
    response_mock = create_response_mock(mocker, request_mock)

    result = await decorated(request_mock, response_mock, value=value)

    assert result == value
    assert response_mock.headers == {}


async def test_paginate_not_injectable(mocker):
    limit = 1
    params = QueryParameters(cursor=None, limit=limit)
    request_mock = create_request_mock(mocker, params)
    response_mock = create_response_mock(mocker, request_mock)
    value = [Entity(id=1, value="a")]

    result = await decorated_not_injectable(
        request_mock,
        response_mock,
        value=value,
        params=params,
    )

    assert result == value
    assert_link_header(
        response_mock,
        {
            "next": {
                "limit": limit,
                "cursor": DeserializableCursor(
                    last_id=value[0].id,
                    last_value=value[0].id,
                    direction=Direction.ASC,
                ),
            }
        },
    )


async def test_paginate_next_link(mocker):
    limit = 1
    request_mock = create_request_mock(
        mocker,
        QueryParameters(cursor=None, limit=limit),
    )
    response_mock = create_response_mock(mocker, request_mock)
    value = [Entity(id=1, value="a")]

    result = await decorated(request_mock, response_mock, value=value)

    assert result == value
    assert_link_header(
        response_mock,
        {
            "next": {
                "limit": limit,
                "cursor": DeserializableCursor(
                    last_id=value[0].id,
                    last_value=value[0].id,
                    direction=Direction.ASC,
                ),
            }
        },
    )


async def test_paginate_multi_id_next_link(mocker):
    limit = 1
    request_mock = create_request_mock(
        mocker,
        QueryParameters(cursor=None, limit=limit),
    )
    response_mock = create_response_mock(mocker, request_mock)
    value = [MultiIDEntity(id_a="b", id_b=1, value="a")]

    result = await decorated_multi_id(request_mock, response_mock, value=value)

    assert result == value
    assert_link_header(
        response_mock,
        {
            "next": {
                "limit": limit,
                "cursor": DeserializableCursor(
                    last_id=[value[0].id_a, value[0].id_b],
                    last_value=[value[0].id_a, value[0].id_b],
                    direction=Direction.ASC,
                ),
            }
        },
    )


async def test_paginate_orderable_next_link(mocker):
    limit = 1
    request_mock = create_request_mock(
        mocker,
        ListEntityParameters(
            cursor=None,
            limit=limit,
            order_direction=Direction.ASC,
            order_by="value",
        ),
    )
    response_mock = create_response_mock(mocker, request_mock)
    value = [Entity(id=1, value="a")]

    result = await decorated_orderable(request_mock, response_mock, value=value)

    assert result == value
    assert_link_header(
        response_mock,
        {
            "next": {
                "limit": limit,
                "cursor": DeserializableCursor(
                    last_id=value[0].id,
                    last_value=value[0].value,
                    direction=Direction.ASC,
                ),
            }
        },
    )


async def test_paginate_with_previous_cursor_next_link(mocker):
    limit = 2
    value = [Entity(id=1, value="a"), Entity(id=2, value="b")]
    request_mock = create_request_mock(
        mocker,
        QueryParameters(
            cursor=DeserializableCursor(
                last_id=value[1].id,
                last_value=value[1].id,
                direction=Direction.DESC,
            ),
            limit=limit,
        ),
    )
    response_mock = create_response_mock(mocker, request_mock)

    result = await decorated(request_mock, response_mock, value=value[:1])

    assert result == value[:1]
    assert_link_header(
        response_mock,
        {
            "next": {
                "limit": limit,
                "cursor": DeserializableCursor(
                    last_id=value[0].id,
                    last_value=value[0].id,
                    direction=Direction.ASC,
                ),
            }
        },
    )


async def test_paginate_with_previous_cursor_previous_link(mocker):
    limit = 2
    value = [Entity(id=1, value="a"), Entity(id=2, value="b")]
    request_mock = create_request_mock(
        mocker,
        QueryParameters(
            cursor=DeserializableCursor(
                last_id=value[0].id,
                last_value=value[0].id,
                direction=Direction.ASC,
            ),
            limit=limit,
        ),
    )
    response_mock = create_response_mock(mocker, request_mock)

    result = await decorated(request_mock, response_mock, value=value[1:])

    assert result == value[1:]
    assert_link_header(
        response_mock,
        {
            "previous": {
                "limit": limit,
                "cursor": DeserializableCursor(
                    last_id=value[1].id,
                    last_value=value[1].id,
                    direction=Direction.DESC,
                ),
            }
        },
    )


@pytest.mark.parametrize("direction", ("asc", "desc"))
async def test_paginate_with_previous_cursor_full_links(mocker, direction):
    limit = 1
    value = [Entity(id=1, value="a"), Entity(id=2, value="b")]
    request_mock = create_request_mock(
        mocker,
        QueryParameters(
            cursor=DeserializableCursor(
                last_id=value[0].id,
                last_value=value[0].id,
                direction=direction,
            ),
            limit=limit,
        ),
    )
    response_mock = create_response_mock(mocker, request_mock)

    result = await decorated(request_mock, response_mock, value=value[1:])

    assert result == value[1:]
    assert_link_header(
        response_mock,
        {
            "previous": {
                "limit": limit,
                "cursor": DeserializableCursor(
                    last_id=value[1].id,
                    last_value=value[1].id,
                    direction=Direction.DESC,
                ),
            },
            "next": {
                "limit": limit,
                "cursor": DeserializableCursor(
                    last_id=value[-1].id,
                    last_value=value[-1].id,
                    direction=Direction.ASC,
                ),
            },
        },
    )


async def test_paginate_query_schema_not_found(mocker):
    limit = 2
    request_mock = create_request_mock(
        mocker,
        QueryParameters(cursor=None, limit=limit),
    )
    response_mock = create_response_mock(mocker, request_mock)
    value = [Entity(id=1, value="a"), Entity(id=2, value="b")]

    async def decorated_without_schema(value: list[Entity]) -> list[Entity]:
        return value

    decorated_without_schema = paginate("id")(decorated_without_schema)

    with pytest.raises(KeyError):
        await decorated_without_schema(request_mock, response_mock, value=value)
