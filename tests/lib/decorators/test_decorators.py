from http import HTTPStatus

import pytest
from fastapi import HTTPException

from coderfastapi.lib.decorators import http_require


@http_require("sample")
async def decorated(value):
    return value


@http_require("sample", boolean=True)
async def decorated_boolean(value):
    return value


@pytest.mark.parametrize("sample", ("a", False, True))
async def test_http_require_found(sample):
    assert await decorated(sample) == sample


async def test_http_require_not_found():
    with pytest.raises(HTTPException) as e:
        await decorated(None)
    http_exception = e.value
    assert http_exception.status_code == HTTPStatus.NOT_FOUND
    assert http_exception.detail == "The sample is not found."


async def test_http_require_found_boolean():
    sample = True
    assert await decorated_boolean(sample) == sample


@pytest.mark.parametrize("sample", ("a", False, None))
async def test_http_require_not_found_boolean(sample):
    with pytest.raises(HTTPException) as e:
        await decorated_boolean(sample)
    http_exception = e.value
    assert http_exception.status_code == HTTPStatus.NOT_FOUND
    assert http_exception.detail == "The sample is not found."
