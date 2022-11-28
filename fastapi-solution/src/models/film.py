from models.genre import Genre
from models.person import Person
from models.config import UUIDMixin, OrjsonConfigMixin


class FilmMixin(UUIDMixin):
    title: str
    imdb_rating: float
    description: str = ''
    genre: list[Genre] = []
    actors: list[Person] = []
    writers: list[Person] = []
    directors: list[Person] = []


class Film(FilmMixin, OrjsonConfigMixin):
    pass
