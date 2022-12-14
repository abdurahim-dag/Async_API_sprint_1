from fastapi import Query
from pydantic import Field
from services import ModelParams, OrderEnum
from uuid import UUID

class imbdbOrderEnum(OrderEnum):
    ASC = '-imdb_rating'
    DESC = '-imdb_rating'

class FilmParams(ModelParams):
    sort: imbdbOrderEnum | None = Field(Query(default=None))
    page_num: int | None = Field(Query(default=None, alias="page[number]", gte=0))
    page_size: int | None = Field(Query(default=None, alias="page[size]", gt=0, lte=50))
    filter_genre: UUID | None = Field(Query(alias="filter[genre]"))
    query: str | None = Field(Query(default=None))
    ids: list[UUID] | None = Field(Query(default=None))
