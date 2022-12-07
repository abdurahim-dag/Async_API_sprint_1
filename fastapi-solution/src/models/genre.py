from models.config import OrjsonConfigMixin, UUIDMixin


class Genre(UUIDMixin, OrjsonConfigMixin):
    name: str
