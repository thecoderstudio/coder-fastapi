from typing import Optional, Self
from uuid import UUID

from fastapi import Request


class RequestWithSession(Request):
    user_id: Optional[UUID] = None

    @staticmethod
    def from_request(request: Request) -> Self:
        return RequestWithSession(
            scope=request.scope,
            receive=request.receive,
            send=request._send,
        )
