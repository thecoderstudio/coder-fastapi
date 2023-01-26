from http import HTTPStatus

import pytest
from fastapi import HTTPException

from coderfastapi.lib.decorators import http_require


@http_require("sample")
async def decorated(value):
    return value


async def test_http_require_found():
    sample = "a"
    assert await decorated(sample) == sample


async def test_http_require_not_found():
    with pytest.raises(HTTPException) as e:
        await decorated(None)
    http_exception = e.value
    assert http_exception.status_code == HTTPStatus.NOT_FOUND
    assert http_exception.detail == "The sample is not found."
