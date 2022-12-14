from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models import FilmDetail
from services.utils import Service


class FilmService(Service):
    model = FilmDetail
    es_index = 'movies'


@lru_cache()
def get_film_service(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(elastic)
