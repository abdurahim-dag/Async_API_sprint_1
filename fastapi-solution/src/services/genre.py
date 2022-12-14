from functools import lru_cache

from .query_parameters import ModelParams
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic

from models import Genre, GenreDetail
from services.utils import Service


class GenreService(Service):
    model = Genre
    modelDetail = GenreDetail
    es_index = 'genres'

    def _get_query_body(self, params: ModelParams = None):
        return None


@lru_cache()
def get_genre_service( elastic: AsyncElasticsearch = Depends(get_elastic),
                      ) -> GenreService:
    return GenreService(elastic)
