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
        """Функция запрашивает модель по id."""
        return await self._get_item_from_elastic(item_id)

    async def get_list(
        self,
        params: ModelParams = None
    ) -> list[Film | Genre | Person | None]:
        """Функция запрашивает список моделей по параметрам запроса."""
        search_query = self._build_search_query(params)
        return await self._get_items_from_elastic(search_query)

    async def _get_item_from_elastic(self, item_id: UUID) -> FilmDetail | GenreDetail | PersonDetail | None:
        """Запрос в индекс ES по id doc."""
        try:
            doc = await self.elastic.get(self.es_index, item_id)
        except NotFoundError:
            return None
        return self.modelDetail(**doc['_source'])

    async def _get_items_from_elastic(self, query_body) -> list[Film | Genre | Person | None] | None:
        """Запрос в индекс ES по телу запроса."""
        try:
            docs = await self.elastic.search(index=self.es_index, body=query_body)
        except NotFoundError:
            return None
        return [self.model(**doc['_source']) for doc in docs["hits"]["hits"]]

    def _build_search_query(self, params: ModelParams) -> str | None:
        """Основная функция генерации json по модели тела запроса."""
        return self._build_query_body(params=params).json(by_alias=True, exclude_none=True)

    def _build_query_body(self, params: ModelParams):
        """Основная функция генерации модели тела запроса."""
        body = self._build_query_body_()
        query = self._build_query()
        body.query = query

        if params.ids:
            if not query.bool:
                query.bool = self._build_query_bool()

            values = [
                str(_id) for _id in params.ids
            ]
            ids_values = self._build_ids_values(values=values)
            query.bool.filter = self._build_query_ids(ids=ids_values)

        if params.sort:
            if params.sort.startswith('-'):
                order = es_query.OrderEnum.DESC
            else:
                order = es_query.OrderEnum.ASC
            body.sort = self._build_query_order(order=order)

        body.size = params.page_size
        body.from_ = params.page_num
        return body

    # Вспомогательные функции, для генерации модели запроса.
    def _build_query_order(self, order: es_query.OrderEnum) -> Any:
        pass

    def _build_ids_values(self, values: list[str]) -> es_query.IDSValues:
        return es_query.IDSValues(
            values=values
        )

    def _build_query_ids(self, ids: es_query.IDSValues) -> es_query.IDS:
        return es_query.IDS(
            ids=ids
        )

    def _build_query_body_(self) -> es_query.ESBodyQuery:
        return es_query.ESBodyQuery()

    def _build_query_match_field_query(self, query) -> es_query.MatchFieldQuery:
        return es_query.MatchFieldQuery(
            query=query,
        )

    def _build_query_match(self, match: es_query.TitleField | es_query.FullNameField) -> es_query.Match:
        return es_query.Match(match=match)

    def _build_query(self) -> es_query.Query:
        return es_query.Query()

    def _build_query_bool(self) -> es_query.QueryBool:
        return es_query.QueryBool()
    #
    def _build_query_term(self, term: es_query.TermFieldGenre) -> es_query.Term:
        return es_query.Term(
            term=term
        )

    def _build_query_nested_inner(self, path: str, query: es_query.Query) -> es_query.NestedInner:
        return es_query.NestedInner(
            path=path,
            query=query
        )

    def _build_nested(self, nested: es_query.NestedInner) -> es_query.Nested:
        return es_query.Nested(nested=nested)
