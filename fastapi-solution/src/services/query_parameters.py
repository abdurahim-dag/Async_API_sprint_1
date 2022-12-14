import abc
from uuid import UUID
from pydantic import BaseModel
from enum import Enum


class OrderEnum(str, Enum):
     ASC: str
     DESC: str

class ModelParams(BaseModel, abc.ABC):
    sort: OrderEnum
    page_num: int
    page_size: int
    filter_genre: UUID
    query: str
    ids: list[UUID]


