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

    def _build_search_query(self, params: ModelParams) -> str | None:
        """Основная функция генерации json по модели тела запроса."""
        body = self._build_query_body(params=params)

        if params.query:
            if not body.query.bool or not body.query.bool.must:
                body.query.bool = self._build_query_bool()
                body.query.bool.must = []

            match_field_query = self._build_query_match_field_query(params.query)
            title = es_query.TitleField(
                title=match_field_query
            )
            match = self._build_query_match(match=title)

            body.query.bool.must.append(
                match
            )

        if params.filter_genre:
            if not body.query.bool or not body.query.bool.must:
                body.query.bool = self._build_query_bool()
                body.query.bool.must = []

            query = self._build_query()
            query.bool = self._build_query_bool()

            term_field = es_query.TermFieldGenre(
                genre_id=str(params.filter_genre)
            )

            query.bool.filter = self._build_query_term(
                term=term_field
            )

            nested_inner = self._build_query_nested_inner(path="genre", query=query)
            nested = self._build_nested(nested=nested_inner)

            body.query.bool.must.append(nested)

        return body.json(by_alias=True, exclude_none=True)

    def _build_query_order(self, order: es_query.OrderEnum) -> es_query.FieldFilmRating:
        """Функция генерации модели, для поля сортировки."""
        return es_query.FieldFilmRating(
            imdb_rating=order
        )


@lru_cache()
def get_film_service(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(elastic)
