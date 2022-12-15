from functools import lru_cache

from .query_parameters import ModelParams
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic

from models import Film, FilmDetail, es_query
from services.utils import Service


class FilmService(Service):
    model = Film
    modelDetail = FilmDetail
    es_index = 'movies'

    def _get_search_query_match(self, params: ModelParams) -> es_query.Match:
        return es_query.Match(
            match=es_query.TitleMatch(
                title=es_query.MatchFieldQuery(
                    query=params.query
                )
            )
        )

    def _get_search_sort(self, params: ModelParams) -> es_query.FieldFilmRating:
        if params.sort.startswith('-'):
            order = es_query.OrderEnum.DESC
        else:
            order = es_query.OrderEnum.ASC
        sort = es_query.FieldFilmRating(
            imdb_rating=order
        )
        return sort


@lru_cache()
def get_film_service(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(elastic)
