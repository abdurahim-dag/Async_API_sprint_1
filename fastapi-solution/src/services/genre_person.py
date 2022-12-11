from elasticsearch import AsyncElasticsearch, NotFoundError
from typing import Optional

from src.models.person import Person_PD

FILM_CACHE_EXPIRE_IN_SECONDS = 300


class GenrePersons:
    def __init__(self, elastic: AsyncElasticsearch, index_name, model, name_colum):
        self.elastic = elastic
        self.index_name = index_name
        self.model = model
        self.name_colum = name_colum

    async def get_by_id(self, data_id: str):
        data = await self.from_cache(data_id)
        if not data:
            data = await self.get_from_elastic(data_id)
            if not data:
                # Если он отсутствует в Elasticsearch, значит, фильма вообще нет в базе
                return None

            # await self._put_to_cache(data)
        return data

    async def get_by_text(self, data_text: str):
        data = await self.from_cache(data_text)
        if not data:
            qw_text = await self._get_qw_text(data_text)
            data = await self.search_from_elastic(qw_text)
            if not data:
                # Если он отсутствует в Elasticsearch, значит, фильма вообще нет в базе
                return None

            # await self._put_to_cache(data)
        return data

    async def get_from_elastic(self, Data_id: str) -> Optional[Person_PD]:
        try:
            doc = await self.elastic.get(self.index_name, Data_id)
        except NotFoundError:
            return None
        return self.model(**doc['_source'])

    async def search_from_elastic(self, Data_id: str) -> Optional[Person_PD]:
        try:
            doc = await self.elastic.search(index=self.index_name, body=Data_id)
        except NotFoundError:
            return None
        return [self.model(**rezult['_source']) for rezult in doc['hits']['hits']]

    async def from_cache(self, data_id: str) -> Optional[Person_PD]:
        """
        Пытаемся получить данные о фильме из кеша, используя команду get
        https://redis.io/commands/get
        """
        return None

        data = await self.redis.get(data_id)
        if not data:
            return None

        # pydantic предоставляет удобное API для создания объекта моделей из json
        data_mod = self.model.parse_raw(data)
        return data_mod

    async def _put_to_cache(self, data_mod):
        """
        Сохраняем данные о фильме, используя команду set
        Выставляем время жизни кеша — 5 минут
        https://redis.io/commands/set
        pydantic позволяет сериализовать модель в json
        """
        await self.redis.set(data_mod.id, data_mod.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _get_qw_text(self, text: str) -> dict:
        search = {'query': {'match': {self.name_colum: text}}}
        return search
