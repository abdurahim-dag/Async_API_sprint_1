from models.genre import Genre
from models.person import Person
from models.config import UUIDMixin, OrjsonConfigMixin


class Film(UUIDMixin, OrjsonConfigMixin):
    title: str
    imdb_rating: float | None


class FilmDetail(Film):
    description: str | None = ''
    actor_names: list[str] = []
    writer_names: list[str] = []
    genre: list[Genre] = []
    actors: list[Person] = []
    writers: list[Person] = []
    directors: list[Person] = []


