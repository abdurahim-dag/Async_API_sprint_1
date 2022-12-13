from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models import Person
from services.utils import Service

from models.person import Person_PD


class PersonService(Service):
    model: Person


@lru_cache()
def get_person_service(elastic: AsyncElasticsearch = Depends(get_elastic), ) -> GenrePersons:
    return GenrePersons(elastic, 'persons', Person_PD, 'id')
