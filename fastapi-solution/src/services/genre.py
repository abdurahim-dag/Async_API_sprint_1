from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models import Genre
from services.utils import Service
from services.genre_person import GenrePersons

class GenreService(Service):
    model: Genre


@lru_cache()
def get_genre_service(redis: Redis = Depends(get_redis),
                      elastic: AsyncElasticsearch = Depends(get_elastic),
                      ) -> GenrePersons:
    return GenrePersons(elastic, 'genres', Genre, 'name')
