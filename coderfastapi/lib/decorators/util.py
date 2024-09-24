import copy
import inspect
from typing import Any, Awaitable, Callable, ParamSpec, TypeVar

T = TypeVar("T")
P = ParamSpec("P")


def propagate_params(
    func: Callable[P, Awaitable[T] | T],
    kwargs: [str, Any],
    **to_propagate,
) -> dict[str, Any]:
    new_kwargs = copy.copy(kwargs)
    func_signature = inspect.signature(func)
    for key, value in to_propagate.items():
        if func_signature.parameters.get(key):
            new_kwargs[key] = value
    return new_kwargs
