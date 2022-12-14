from .query_parameters import ModelParams
from uuid import UUID
from elasticsearch import AsyncElasticsearch, NotFoundError
from abc import ABC
from models import FilmDetail, Genre, Person, Film


class Service(ABC):
    model: None
    es_index: str

    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_by_id(self, item_id: UUID) -> FilmDetail | Genre | Person | None:
        item = await self._get_item_from_elastic(item_id)
        if not item:
            return None
        return item


    async def get_list(
        self,
        params: ModelParams
    ) -> list[FilmDetail | Film | Genre | Person]:
        query_body = self._get_query_body(params)
        docs = await self.elastic.search(index=self.es_index, body=query_body)
        return [self.model(**doc['_source']) for doc in docs["hits"]["hits"]]

    def _get_query_body(self, params: ModelParams):
        pass

    async def _get_item_from_elastic(self, item_id: UUID) -> FilmDetail | Genre | Person | None:
        try:
            doc = await self.elastic.get(self.es_index, item_id)
        except NotFoundError:
            return None
        return self.model(**doc['_source'])
