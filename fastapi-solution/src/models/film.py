from models.genre import Genre
from models.person import PersonName
from models.config import UUIDMixin, OrjsonConfigMixin


class FilmSearchMixin(UUIDMixin):
    title: str
    imdb_rating: float | None

class FilmDetailMixin(FilmSearchMixin):
    description: str | None = ''
    actor_names: list[str] = []
    writer_names: list[str] = []
    genre: list[Genre] = []
    actors: list[PersonName] = []
    writers: list[PersonName] = []
    directors: list[PersonName] = []


class FilmDetail(FilmDetailMixin, OrjsonConfigMixin):
    pass

class Film(FilmSearchMixin, OrjsonConfigMixin):
    pass