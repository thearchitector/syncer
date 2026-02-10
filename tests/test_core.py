import asyncio
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import nullcontext
from typing import Any

import pytest

from syncer import can_syncify
from syncer.core import syncify


async def await_fn() -> int:
    await asyncio.sleep(0)
    return 1


async def async_with_fn() -> int:
    async with nullcontext():
        return 1


async def async_for_fn() -> list[int]:
    async def agen() -> AsyncIterator[int]:
        yield 1

    return [1 async for _ in agen()]


def sync_fn() -> int:
    return 1


async def no_await_fn() -> int:
    return 1


async def no_async_with_fn() -> Callable[[], Awaitable[int]]:
    async def inner() -> int:
        async with nullcontext():
            return 1

    return inner


async def no_async_for_fn() -> Callable[[], Awaitable[list[int]]]:
    async def inner() -> list[int]:
        async def agen() -> AsyncIterator[int]:
            yield 1

        return [1 async for _ in agen()]

    return inner


@pytest.mark.parametrize(
    "func,expected",
    [
        (sync_fn, False),
        (await_fn, False),
        (async_with_fn, False),
        (async_for_fn, False),
        (no_await_fn, True),
        (no_async_with_fn, True),
        (no_async_for_fn, True),
    ],
    ids=[
        "sync",
        "await",
        "async_with",
        "async_for",
        "no_await",
        "no_async_with",
        "no_async_for",
    ],
)
def test_can_syncify(func: Callable[..., Any], expected: bool) -> None:
    assert can_syncify(func) is expected


@pytest.mark.parametrize(
    "func",
    [no_await_fn, no_async_with_fn, no_async_for_fn],
    ids=["no_await", "no_async_with", "no_async_for"],
)
async def test_syncify(func: Callable[..., Any]) -> None:
    assert syncify(func)()


def test_syncify_fail() -> None:
    with pytest.raises(ValueError):
        syncify(await_fn)
