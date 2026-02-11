import sys
from typing import Self

from pydantic import AnyHttpUrl, BaseModel, Field
from starlette.requests import Request


class HTTPRequestSchema(BaseModel):
    """Structured representation of an HTTP request (primarily for Cloud Logging)."""

    request_method: str = Field(alias="requestMethod")
    request_url: AnyHttpUrl = Field(alias="requestUrl")
    request_size: int = Field(alias="requestSize")
    remote_ip: str | None = Field(alias="remoteIp")
    protocol: str
    referrer: str | None
    user_agent: str | None = Field(alias="userAgent")

    @classmethod
    def from_request(cls, request: Request) -> Self:
        return cls(
            requestMethod=request.method,
            requestUrl=str(request.url),  # ty: ignore[invalid-argument-type]
            requestSize=sys.getsizeof(request),
            remoteIp=request.client.host if request.client else None,
            protocol=request.url.scheme,
            referrer=request.headers.get("referrer"),
            userAgent=request.headers.get("user-agent"),
        )
