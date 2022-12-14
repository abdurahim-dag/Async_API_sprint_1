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

    def _get_query_body(self, params: ModelParams):
        body = es_query.ESBodyQuery()
        if params.query or params.filter_genre or params.ids:
            query = es_query.BodyQuery()
            query_bool = es_query.QueryBool()
            query_bool.must = []
            query.bool = query_bool
        
            if params.query:
                match = es_query.Match(
                    match=es_query.FilmTitleMatch(
                        title=es_query.MatchFieldQuery(
                            query=params.query
                        )
                    )
                )
                query_bool.must.append(match)
        
            if params.filter_genre:
                nested = es_query.NestedInner(
                    path="genre",
                    query=es_query.BodyQuery(
                        bool=es_query.QueryBool(
                            filter=es_query.Term(
                                term=es_query.TermFieldGenre(
                                    genre_id=str(params.filter_genre)
                                )
                            )
                        )
                    )
                )
                query_bool.must.append(
                    es_query.Nested(nested=nested)
                )
        
            if params.ids:
                filter_ids = es_query.IDS(
                    ids=es_query.IDSValues(
                        values=[
                            str(id) for id in params.ids
                        ]
                    )
                )
                query_bool.filter = filter_ids
        
            if params.sort:
                if params.sort.startswith('-'):
                    order = es_query.imbdbOrderEnum.DESC
                else:
                    order = es_query.imbdbOrderEnum.ASC
                sort = es_query.SortFieldFilmRating(
                    imdb_rating=order
                )
                body.sort = sort
            body.query = query
            body.size = params.page_size
            body.from_ = params.page_num
            return body.json(by_alias=True, exclude_none=True)


@lru_cache()
def get_film_service(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(elastic)
