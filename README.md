# syncer

![Licensed under BSD-3-Clause-Clear](https://img.shields.io/badge/license-BSD--3--Clause--Clear-yellow?style=for-the-badge)

Run (some) coroutine functions synchronously.

## Usage

Coroutine functions can be checked for syncifiability with `can_syncify`. Functions that contain any `await`, `async with`, or `async for` expression are not syncifiable. If they are, wrap them in `syncify` to run them as regular synchronous functions.

```python
from syncer import syncify, can_syncify


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
