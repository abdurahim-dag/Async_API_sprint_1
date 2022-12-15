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

    def _get_search_query_match(self, params: ModelParams) -> es_query.Match:
        return es_query.Match(
            match=es_query.FullNameMatch(
                full_name=es_query.MatchFieldQuery(
                    query=params.query
                )
            )
        )

    def _get_search_sort(self, params: ModelParams) -> es_query.FieldId:
        if params.sort.startswith('-'):
            order = es_query.OrderEnum.DESC
        else:
            order = es_query.OrderEnum.ASC
        sort = es_query.FieldId(
            id=order
        )
        return sort




@lru_cache()
def get_person_service(elastic: AsyncElasticsearch = Depends(get_elastic), ) -> PersonService:
    return PersonService(elastic)
