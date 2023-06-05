from inspect import signature
from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit

from codercore.lib.collection import Direction
from fastapi import Request, Response
from fastapi.params import Depends

from coderfastapi.lib.signature import copy_parameters
from coderfastapi.lib.validation.schemas.query import CursorSchema, QueryParameters


def paginate(id_attr: str):
    def decorate(func):
        func_signature = signature(func)

        async def wrapped(request: Request, response: Response, *args, **kwargs):
            schema_name, query_schema = _get_query_schema(func_signature, request)
            kwargs[schema_name] = query_schema

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


def _get_query_schema(func_signature, request):
    for name, parameter in func_signature.parameters.items():
        if _is_valid_query_parameter(parameter):
            return (name, parameter.annotation(**dict(request.query_params)))
    raise KeyError("QuerySchema not found")


def _is_valid_query_parameter(parameter):
    return (
        isinstance(parameter.default, Depends)
        and parameter.default.dependency is None
        and issubclass(parameter.annotation, QueryParameters)
    )


def _build_links(id_attr, query_schema, request, result):
    result_length = len(result)
    links = []

    if query_schema.cursor and result_length >= 1:
        cursor = _create_cursor(Direction.DESC, result, id_attr, 0)
        links.append(_construct_link(cursor, "previous", request))

    if result_length == query_schema.limit:
        cursor = _create_cursor(Direction.ASC, result, id_attr, -1)
        links.append(_construct_link(cursor, "next", request))

    return links


def _create_cursor(direction, result, id_attr, index):
    item = result[index]
    return str(
        CursorSchema(
            last_id=str(getattr(item, id_attr)),
            last_value=str(getattr(item, id_attr)),
            direction=direction,
        )
    )


def _construct_link(cursor, rel, request):
    url = _construct_url_with_cursor(cursor, request)
    return f'<{url}>; rel="{rel}"'


def _construct_url_with_cursor(cursor, request):
    scheme, netloc, path, query_string, fragment = urlsplit(str(request.url))
    query_params = parse_qs(query_string)
    query_params["cursor"] = [cursor]

    return urlunsplit(
        (
            scheme,
            netloc,
            path,
            urlencode(query_params, doseq=True),
            fragment,
        )
    )
