from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from .query_parameters import ModelParams
from models import Person, PersonDetail, es_query
from services.utils import Service


class PersonService(Service):
    model = Person
    modelDetail = PersonDetail
    es_index = 'persons'

    def _build_search_query(self, params: ModelParams) -> str | None:
        """Основная функция генерации json по модели тела запроса."""
        body = self._build_query_body(params=params)

        if params.query:
            if not body.query.bool or not body.query.bool.must:
                body.query.bool = self._build_query_bool()
                body.query.bool.must = []

            match_field_query = self._build_query_match_field_query(params.query)
            full_name = es_query.FullNameField(
                full_name = match_field_query
            )
            match = self._build_query_match(match=full_name)

            body.query.bool.must.append(
                match
            )

        return body.json(by_alias=True, exclude_none=True)

    def _build_query_order(self, order: es_query.OrderEnum) -> es_query.FieldId:
        """Функция генерации модели, для поля сортировки."""
        return es_query.FieldId(
            id=order
        )


@lru_cache()
def get_person_service(elastic: AsyncElasticsearch = Depends(get_elastic), ) -> PersonService:
    return PersonService(elastic)
