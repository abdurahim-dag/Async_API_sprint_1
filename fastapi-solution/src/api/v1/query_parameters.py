from fastapi import Query
from pydantic import BaseModel, Field
import enum

class imbdbOrderEnum(str, enum.Enum):
    ASC = '-imdb_rating'
    DESC = '-imdb_rating'

class FilmParams(BaseModel):
    sort: imbdbOrderEnum | None = Field(Query(default=None))
    page_num: int | None = Field(Query(default=None, alias="page[number]", gt=0))
    page_size: int | None = Field(Query(default=None, alias="page[size]", gt=0, lte=50))
    filter_genre: str | None = Field(Query(default=None, alias="filter[genre]"))
    query: str | None = Field(Query(default=None))
    ids: list[str] | None = Field(Query(default=None))

    # def __init__(
    #     self,
    #     sort: str | None = Query(default=None),
    #     page_num: int | None = Query(default=None, alias="page[number]"),
    #     page_size: int | None = Query(default=None, alias="page[size]"),
    #     filter_genre: str | None = Query(default=None, alias="filter[genre]"),
    #     query: str | None = Query(default=None),
    #     ids: list[str] | None = Query(default=None),
    # ):
    #     self.sort = sort
    #     self.page_num = page_num
    #     self.page_size = page_size
    #     self.filter_genre = filter_genre
    #     self.query = query
    #     self.ids = ids
    #
