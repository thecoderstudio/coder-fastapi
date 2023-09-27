import sys

from pydantic import BaseModel, root_validator
from starlette.requests import Request


class HTTPRequestSchema(BaseModel):
    request_method: str
    request_url: str
    request_size: int
    remote_ip: str
    protocol: str
    referrer: str
    user_agent: str

    @root_validator(pre=True)
    def parse_request(cls, request: Request):
        values = {
            "request_method": request.method,
            "request_url": request.url.path,
            "request_size": sys.getsizeof(request),
            "remote_ip": request.client.host,
            "protocol": request.url.scheme,
        }

        if "referrer" in request.headers:
            values["referrer"] = request.headers["referrer"]

        if "user-agent" in request.headers:
            values["userAgent"] = request.headers["user-agent"]

        return values
