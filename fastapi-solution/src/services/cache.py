import inspect
import pickle
from functools import wraps
from typing import Any, Awaitable, Callable, Optional, Type, TypeVar
from fastapi.concurrency import run_in_threadpool
from fastapi import Request, Response
import db.redis as redis


def cache(
        ttl: int = 10,
):
    """
    Cache for Operation on Redis.
    """
    def wrapper(func: Awaitable):

        # Если в сигнатуре функции не объявлены Request и Response.
        # То добавим их.
        signature = inspect.signature(func)
        request_param = next(
            (param for param in signature.parameters.values() if param.annotation is Request),
            None,
        )
        response_param = next(
            (param for param in signature.parameters.values() if param.annotation is Response),
            None,
        )
        parameters = [*signature.parameters.values()]
        if not request_param:
            parameters.append(
                inspect.Parameter(
                    name="_request",
                    annotation=Request,
                    kind=inspect.Parameter.KEYWORD_ONLY,
                ),
            )
        if not response_param:
            parameters.append(
                inspect.Parameter(
                    name="_response",
                    annotation=Response,
                    kind=inspect.Parameter.KEYWORD_ONLY,
                ),
            )
        if parameters:
            signature = signature.replace(parameters=parameters)
        func.__signature__ = signature


        @wraps(func)
        async def inner(*args, **kwargs):
            async def exec_func(*args, **kwargs):
                if inspect.iscoroutinefunction(func):
                    # Если функция асинхронная.
                    return await func(*args, **kwargs)
                else:
                    # Если функция синхронная.
                    return await run_in_threadpool(func, *args, **kwargs)

            # Забираем request, он должен быть там.
            request: Optional[Request] = kwargs.pop("_request")
            response: Optional[Request] = kwargs.pop("_response")
            res = None
            if request:
                cache_control = request.headers.get("Cache-Control")
                if cache_control in ("no-store", "no-cache") or \
                   request.method != "GET":
                    await exec_func(*args, **kwargs)
                else:
                    cache_key = request.url.path
                    client = await redis.get_redis()
                    cache_value = await client.get(cache_key)
                    if cache_value:
                        res = pickle.loads(cache_value)
                    else:
                        res = await exec_func(*args, **kwargs)
                        await client.set(cache_key, pickle.dumps(res))
                        await client.expire(cache_key, ttl)
            else:
                response.headers["Cache-Control"] = f"max-age={ttl}"
            return res

        return inner
    return wrapper

