from dataclasses import dataclass

import httpx
from codercore.lib.collection import Direction
from fastapi import Depends, Request

from coderfastapi.lib.decorators import paginate
from coderfastapi.lib.validation.schemas.query import CursorSchema, QueryParameters
from coderfastapi.test import assert_link_header


@dataclass
class Entity:
    id: int
    value: str


@paginate("id")
async def decorated(
    value: list[Entity],
    params: QueryParameters = Depends(),
) -> list[Entity]:
    return value


def create_request_mock(mocker, params: QueryParameters):
    request_mock = mocker.MagicMock()
    request_mock.query_params = params.dict()
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
                "cursor": CursorSchema(
                    last_id=str(value[0].id),
                    last_value=str(value[0].id),
                    direction=Direction.ASC,
                ),
            }
        },
    )


async def test_paginate_previous_link():
    pass


async def test_paginate_full_links():
    pass


async def test_paginate_full_links_alt_order_by():
    pass


async def test_paginate_query_schema_not_found():
    pass
