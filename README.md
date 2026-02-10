# noaio

![Licensed under BSD-3-Clause-Clear](https://img.shields.io/badge/license-BSD--3--Clause--Clear-yellow?style=for-the-badge)

Run (some) coroutine functions synchronously.

## Usage

Coroutine functions can be checked for syncifiability with `can_syncify`. Functions that contain any `await`, `async with`, or `async for` expression are not syncifiable. If they are, wrap them in `syncify` to run them as regular synchronous functions.

```python
from noaio import syncify, can_syncify


async def func_without_await():
    return 1


can_syncify(func_without_await) == True
syncify(func_without_await)() == 1
```

```python
async def func_with_await():
    await asyncio.sleep(0)
    return 1


can_syncify(func_with_await) == False
syncify(func_with_await)  ## ValueError
```

## How can I break it?

`can_syncify` checks the AST of the function you provide it. If it contains any `await`, `async with` or `async for` opcodes at the root level (immediately executed), it will return `False`.

`syncify` wraps the provided async function in a synchronous one that drives the coroutine to completion using `.send`, catching the iteration error and returning the result.

The library is typed, and expects you to use it in compliance with its type signatures.
