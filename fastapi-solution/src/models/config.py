import orjson
from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class UUIDMixin(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class OrjsonConfigMixin(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
