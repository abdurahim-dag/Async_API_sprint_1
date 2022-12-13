from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models import Genre
from services.utils import Service

class GenrePersonsService(Service):
    model: Genre


@lru_cache()
def get_genre_service( elastic: AsyncElasticsearch = Depends(get_elastic),
                      ) -> GenrePersonsService:
    return GenrePersonsService(elastic, 'genres', Genre, 'name')
