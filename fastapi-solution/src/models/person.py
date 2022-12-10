from models.config import OrjsonConfigMixin, UUIDMixin
from pydantic import Field
from uuid import UUID


class PersonName(UUIDMixin, OrjsonConfigMixin):
    name: str = Field(alias='full_name')

    class Config:
        allow_population_by_field_name = True

class Person(PersonName):
    role: str
    film_ids: list[UUID] = []
