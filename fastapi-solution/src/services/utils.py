from .query_parameters import ModelParams
from typing import Any
from uuid import UUID
from elasticsearch import AsyncElasticsearch, NotFoundError
from abc import ABC
from models import FilmDetail, Genre, Person, Film, GenreDetail, PersonDetail, es_query

class Service(ABC):
    model: None
    modelDetail: None
    es_index: str

    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_by_id(self, item_id: UUID) -> FilmDetail | GenreDetail | PersonDetail | None:
        return await self._get_item_from_elastic(item_id)


    async def get_list(
        self,
        params: ModelParams = None
    ) -> list[Film | Genre | Person | None]:
        query_body = self._get_query_body(params)
        return await self._get_items_from_elastic(query_body)


    async def _get_item_from_elastic(self, item_id: UUID) -> FilmDetail | GenreDetail | PersonDetail | None:
        try:
            doc = await self.elastic.get(self.es_index, item_id)
        except NotFoundError:
            return None
        return self.modelDetail(**doc['_source'])

    async def _get_items_from_elastic(self, query_body) -> list[Film | Genre | Person | None] | None:
        try:
            docs = await self.elastic.search(index=self.es_index, body=query_body)
        except NotFoundError:
            return None
        return [self.model(**doc['_source']) for doc in docs["hits"]["hits"]]

    def _get_query_body(self, params: ModelParams) -> str | None:
        if params:
            body = es_query.ESBodyQuery()
            if params.query or params.filter_genre or params.ids:
                query = es_query.BodyQuery()
                query_bool = es_query.QueryBool()
                query_bool.must = []
                query.bool = query_bool

                if params.query:
                    match = self._get_search_query_match(params)
                    query_bool.must.append(match)

                if params.ids:
                    filter_ids = self._get_search_ids(params)
                    query_bool.filter = filter_ids

                body.query = query

            if params.sort:
                sort = self._get_search_sort(params)
                body.sort = sort

            body.size = params.page_size
            body.from_ = params.page_num
            return body.json(by_alias=True, exclude_none=True)
        return None

    def _get_search_query_match(self, params: ModelParams) -> es_query.Match:
        pass

    def _get_search_ids(self, params: ModelParams) -> es_query.IDS:
        return es_query.IDS(
            ids=es_query.IDSValues(
                values=[
                    str(_id) for _id in params.ids
                ]
            )
        )

    def _get_search_sort(self, params: ModelParams) -> es_query.FieldFilmRating | es_query.FieldId:
        pass