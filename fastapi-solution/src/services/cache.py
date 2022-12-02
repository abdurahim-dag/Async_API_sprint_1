from aioredis import Redis
from functools import wraps
from typing import Any, Awaitable, Callable, Optional, Type, TypeVar

def cache(
        expire: int,
):
    """
    Cache for Operation on Redis.
    """
    def wrapper(func: Awaitable):
        @wraps(func)
        async def inner(*args, **kwargs):
            await func(*args, **kwargs)
        return inner
    return wrapper

