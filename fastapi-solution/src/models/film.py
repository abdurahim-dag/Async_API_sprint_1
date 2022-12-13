from models.genre import Genre
from models.person import PersonName
from models.config import UUIDMixin, OrjsonConfigMixin


class FilmMixin(UUIDMixin):
    title: str
    imdb_rating: float
    description: str = ''
    actor_names: list[str] = []
    writer_names: list[str] = []
    genre: list[Genre] = []
    actors: list[PersonName] = []
    writers: list[PersonName] = []
    directors: list[PersonName] = []




class Film(FilmMixin, OrjsonConfigMixin):
    pass
