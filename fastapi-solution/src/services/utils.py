from abc import ABC, abstractmethod
from uuid import UUID

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError

from models import Film, Genre, Person


CACHE_EXPIRE_IN_SECONDS = 60 * 5


class Service(ABC):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    @abstractmethod
    def model(*args, **kwargs) -> Film | Genre | Person:
        pass

    async def get_by_id(self, item_id: UUID) -> Film | Genre | Person | None:
        item = await self._item_from_cache(item_id)
        if not item:
            item = await self._get_item_from_elastic(item_id)
            if not item:
                return None
            await self._put_item_to_cache(item)

        return item

    async def get_list(self,) -> list[Film | Genre | Person]:
        # Нужно посмотреть как брать из эластика несколько позиций
        ...

    async def _get_item_from_elastic(self, item_id: UUID) -> Film | Genre | Person | None:
        try:
            doc = await self.elastic.get('movies', item_id)
        except NotFoundError:
            return None
        return self.model(**doc['_source'])

    async def _item_from_cache(self, item_id: UUID) -> Film | Genre | Person | None:
        data = await self.redis.get(item_id)
        if not data:
            return None
        item = self.model.parse_raw(data)
        return item

    async def _put_item_to_cache(self, item: Film | Genre | Person):
        await self.redis.set(item.uuid, item.json(), expire=CACHE_EXPIRE_IN_SECONDS)
