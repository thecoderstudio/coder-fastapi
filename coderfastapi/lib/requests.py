from typing import Any, Self

from fastapi import Request


class AugmentableRequest(Request):
    additional_request_properties: dict[str, Any] = {}

    def __getattribute__(self, name: str) -> Any:
        additional_request_properties = super().__getattribute__(
            "additional_request_properties"
        )
        try:
            return additional_request_properties[name]
        except KeyError:
            return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Any) -> None:
        try:
            super().__getattribute__(name)
            super().__setattr__(name, value)
        except AttributeError:
            self.additional_request_properties[name] = value

    @staticmethod
    def from_request(request: Request) -> Self:
        return AugmentableRequest(
            scope=request.scope,
            receive=request.receive,
            send=request._send,
        )
