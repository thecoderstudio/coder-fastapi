import inspect

from fastapi import APIRouter, Request
from fastapi.requests import HTTPConnection

from coderfastapi.lib.security import AuthorizationPolicy
from coderfastapi.lib.security.acl import ACL, ACLProvider
from coderfastapi.lib.signature import copy_parameters


class SecureRouter(APIRouter, ACLProvider):
    def __init__(self, acl: ACL = (), *args, **kwargs):
        ACLProvider.__init__(acl)
        APIRouter.__init__(*args, **kwargs)
        self.acl_policy = AuthorizationPolicy(self)

    async def _call_handler_with_authentication(
        self,
        handler,
        permission,
        http_connection: HTTPConnection,
        *args,
        **kwargs,
    ):
        enhanced_http_connection = self.acl_policy.enhance_http_connection(
            http_connection
        )
        self.acl_policy.validate_permission(permission, enhanced_http_connection)

        output = handler(*args, **kwargs)
        if inspect.iscoroutine(output):
            output = await output

        return output

    def post(self, *outer_args, **outer_kwargs):
        return lambda func: self._http_method(func, "post", *outer_args, **outer_kwargs)

    def put(self, *outer_args, **outer_kwargs):
        return lambda func: self._http_method(func, "put", *outer_args, **outer_kwargs)

    def patch(self, *outer_args, **outer_kwargs):
        return lambda func: self._http_method(
            func, "patch", *outer_args, **outer_kwargs
        )

    def delete(self, *outer_args, **outer_kwargs):
        return lambda func: self._http_method(
            func, "delete", *outer_args, **outer_kwargs
        )

    def get(self, *outer_args, **outer_kwargs):
        return lambda func: self._http_method(func, "get", *outer_args, **outer_kwargs)

    def options(self, *outer_args, **outer_kwargs):
        return lambda func: self._http_method(
            func, "options", *outer_args, **outer_kwargs
        )

    def trace(self, *outer_args, **outer_kwargs):
        return lambda func: self._http_method(
            func, "trace", *outer_args, **outer_kwargs
        )

    def head(self, *outer_args, **outer_kwargs):
        return lambda func: self._http_method(func, "head", *outer_args, **outer_kwargs)

    def _http_method(
        self, func, http_method, *outer_args, permission="public", **outer_kwargs
    ):
        route = getattr(super(SecureRouter, self), http_method)

        @route(*outer_args, **outer_kwargs)
        async def wrapped(request: Request, *args, **kwargs):
            return await self._call_handler_with_authentication(
                func, permission, request, *args, **kwargs
            )

        wrapped_signature = inspect.signature(wrapped)
        func_signature = inspect.signature(func)
        wrapped.__signature__ = copy_parameters(
            wrapped_signature, func_signature, ["request"]
        )
        return wrapped
