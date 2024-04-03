from inspect import Parameter, Signature, isclass, signature
from typing import Awaitable, Callable, Iterable, TypeVar
from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit

from codercore.lib.collection import Direction
from fastapi import Request, Response
from fastapi.params import Depends

from coderfastapi.lib.signature import copy_parameters
from coderfastapi.lib.validation.schemas.pagination import DeserializableCursor
from coderfastapi.lib.validation.schemas.query import (
    OrderableQueryParameters,
    QueryParameters,
)

T = TypeVar("T")
S = TypeVar("S", bound=QueryParameters)
Entities = Iterable[T]


def paginate(
    id_attr: str,
) -> Callable[
    [Callable[..., Awaitable[Entities]]],
    Callable[[Request, Response, ...], Awaitable[Entities]],
]:
    def decorate(
        func: Callable[..., Awaitable[Entities]]
    ) -> Callable[[Request, Response, ...], Awaitable[Entities]]:
        func_signature = signature(func)

        async def wrapped(
            request: Request,
            response: Response,
            *args,
            **kwargs,
        ) -> Entities:
            schema_name, query_schema = _get_query_schema(func_signature, request)
            if query_schema:
                kwargs[schema_name] = query_schema
            else:
                query_schema = kwargs[schema_name]

            result = await func(*args, **kwargs)
            links = _build_links(id_attr, query_schema, request, result)

            if links:
                response.headers["Link"] = ", ".join(links)
            return result

        wrapped_signature = signature(wrapped)
        wrapped.__signature__ = copy_parameters(
            wrapped_signature, func_signature, ["request", "response"]
        )
        return wrapped

    return decorate


def _get_query_schema(func_signature: Signature, request: Request) -> tuple[str, S]:
    for name, parameter in func_signature.parameters.items():
        if _is_valid_query_parameter(parameter):
            if _is_injectable(parameter):
                return (name, parameter.annotation(**dict(request.query_params)))
            else:
                return (name, None)
    raise KeyError("QuerySchema not found")


def _is_valid_query_parameter(parameter: Parameter) -> bool:
    return (
        isclass(parameter.annotation)
        and getattr(parameter.annotation, "__canonical_name__", None)
        == "QueryParameters"
    )


def _is_injectable(parameter) -> bool:
    return (
        isinstance(parameter.default, Depends) and parameter.default.dependency is None
    )


def _build_links(
    id_attr: str,
    query_schema: S,
    request: Request,
    result: Entities,
) -> list[str]:
    result_length = len(result)
    links = []
    value_attr = id_attr
    if isinstance(query_schema, OrderableQueryParameters):
        value_attr = query_schema.order_by

    if query_schema.cursor and result_length >= 1:
        cursor = _create_cursor(Direction.DESC, id_attr, value_attr, result[0])
        links.append(_construct_link(cursor, "previous", request))

    if result_length == query_schema.limit:
        cursor = _create_cursor(Direction.ASC, id_attr, value_attr, result[-1])
        links.append(_construct_link(cursor, "next", request))

    return links


def _create_cursor(
    direction: Direction,
    id_attr: str,
    value_attr: str,
    item: T,
) -> DeserializableCursor:
    return DeserializableCursor(
        last_id=getattr(item, id_attr),
        last_value=getattr(item, value_attr),
        direction=direction,
    )


def _construct_link(cursor: DeserializableCursor, rel: str, request: Request) -> str:
    url = _construct_url_with_cursor(cursor, request)
    return f'<{url}>; rel="{rel}"'


def _construct_url_with_cursor(cursor: DeserializableCursor, request: Request) -> str:
    scheme, netloc, path, query_string, fragment = urlsplit(str(request.url))
    query_params = parse_qs(query_string)
    query_params["cursor"] = [str(cursor)]

    return urlunsplit(
        (
            scheme,
            netloc,
            path,
            urlencode(query_params, doseq=True),
            fragment,
        )
    )
