from models.config import OrjsonConfigMixin, UUIDMixin


class Person(UUIDMixin, OrjsonConfigMixin):
    full_name: str
    role: str
