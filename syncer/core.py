import inspect
from dis import get_instructions
from functools import wraps
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from collections.abc import Callable, Coroutine
    from typing import ParamSpec, TypeVar

    P = ParamSpec("P")
    T = TypeVar("T")

_ASYNC_CODES = {
    "GET_AWAITABLE",
    "GET_AITER",
    "GET_ANEXT",
    "END_ASYNC_FOR",
    "BEFORE_ASYNC_WITH",
    "SETUP_ASYNC_WITH",
}


def can_syncify(func: "Callable[P, T]") -> bool:
    if not inspect.iscoroutinefunction(func):
        return False

    return all(instr.opname not in _ASYNC_CODES for instr in get_instructions(func))


def syncify(func: "Callable[P, Coroutine[None, None, T]]") -> "Callable[P, T]":
    if not can_syncify(func):
        raise ValueError("Function is not syncifiable.")

    @wraps(func)
    def _wrapper(*args: "P.args", **kwargs: "P.kwargs") -> "T":
        coro = func(*args, **kwargs)
        try:
            coro.send(None)
            raise RuntimeError(
                "Attempted to complete a syncifiable coroutine, but it did not stop."
            )
        except StopIteration as e:
            return cast("T", e.value)
        finally:
            coro.close()

    return _wrapper
