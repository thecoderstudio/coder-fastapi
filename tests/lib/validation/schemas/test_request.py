import sys
from ipaddress import IPv4Address

from starlette.datastructures import URL

from coderfastapi.lib.validation.schemas.request import HTTPRequestSchema


def test_http_request_schema_from_request_complete(mocker):
    request_method = "POST"
    request_url = "http://localhost"
    remote_ip = "127.0.0.1"
    referrer = "/referrer"
    user_agent = "Mozilla Firefox"
    request = mocker.Mock(
        method=request_method,
        url=URL(request_url),
        client=mocker.Mock(host=remote_ip),
        headers={
            "referrer": referrer,
            "user-agent": user_agent,
        },
    )

    schema = HTTPRequestSchema.from_request(request)
    assert schema.dict(by_alias=True) == {
        "requestMethod": request_method,
        "requestUrl": request_url,
        "requestSize": sys.getsizeof(request),
        "remoteIp": IPv4Address(remote_ip),
        "protocol": "http",
        "referrer": referrer,
        "userAgent": user_agent,
    }


def test_http_request_schema_from_request_minimal(mocker):
    request_method = "POST"
    request_url = "http://localhost"
    request = mocker.Mock(
        method=request_method,
        url=URL(request_url),
        client=mocker.Mock(host=None),
        headers={},
    )

    schema = HTTPRequestSchema.from_request(request)
    assert schema.dict(by_alias=True, exclude_none=True) == {
        "requestMethod": request_method,
        "requestUrl": request_url,
        "requestSize": sys.getsizeof(request),
        "protocol": "http",
    }
