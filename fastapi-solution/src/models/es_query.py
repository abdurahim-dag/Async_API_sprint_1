from pydantic import BaseModel, Field
import orjson
from typing import ForwardRef
from enum import Enum


class MatchFieldQuery(BaseModel):
    query: str
    fuzziness: str = Field(default='AUTO')


class FilmTitleMatch(BaseModel):
    title: MatchFieldQuery


class Match(BaseModel):
    match: FilmTitleMatch


class TermFieldGenre(BaseModel):
    genre_id: str = Field(alias='genre.id')

    class Config:
        allow_population_by_field_name = True


class IDSValues(BaseModel):
    values: list[str] = []


class IDS(BaseModel):
    ids: IDSValues


class Term(BaseModel):
    term: TermFieldGenre


BodyQueryRef = ForwardRef("BodyQuery")


class NestedInner(BaseModel):
    path: str
    query: BodyQueryRef

class Nested(BaseModel):
    nested: NestedInner


class QueryBool(BaseModel):
    must: list[Match|Nested] | None
    filter: Term | IDS | None


class BodyQuery(BaseModel):
    bool: QueryBool | None


class imbdbOrderEnum(str, Enum):
    ASC = 'asc'
    DESC = 'desc'


class SortFieldFilmRating(BaseModel):
    imdb_rating: imbdbOrderEnum


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class ESBodyQuery(BaseModel):
    query: BodyQuery | None
    sort: SortFieldFilmRating | None
    size: int = Field(default=0)
    from_: int = Field(default=0, alias='from')

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


NestedInner.update_forward_refs()
