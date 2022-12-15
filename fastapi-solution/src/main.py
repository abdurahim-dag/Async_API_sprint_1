import logging

import redis.asyncio as redisio
from redis.backoff import ExponentialBackoff
from redis.retry import Retry
from redis.exceptions import (
    BusyLoadingError,
    ConnectionError,
    TimeoutError
)
import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from api.v1 import films, genres, persons
#from api.v1 import films, genres, persons
from core import config
from core.logger import LOGGING

from db import elastic, redis

import db.redis as redis


app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    url = f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}"

    # Run 3 retries with exponential backoff strategy
    retry = Retry(ExponentialBackoff(), 3)
    redis.redis = await redisio.from_url(url,  db=1, retry=retry,
              retry_on_error=[BusyLoadingError, ConnectionError, TimeoutError])
    elastic.es = AsyncElasticsearch(hosts=[f'{config.ELASTIC_HOST}:{config.ELASTIC_PORT}'])


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['genres'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['persons'])
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=config.origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8080,
        reload=True,
    )
