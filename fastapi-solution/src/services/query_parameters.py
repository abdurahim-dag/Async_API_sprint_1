import abc
from uuid import UUID
from pydantic import BaseModel
from enum import Enum


class OrderEnum(str, Enum):
     ASC: str
     DESC: str

class ModelParams(BaseModel, abc.ABC):
    sort: OrderEnum | None
    page_num: int | None
    page_size: int | None
    filter_genre: UUID | None
    query: str | None
    ids: list[UUID] | None


