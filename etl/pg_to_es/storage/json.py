import json
import pathlib
from typing import Optional

from .base import BaseStorage
from .utils import DateEncoder


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path
        self.path = pathlib.Path(self.file_path)

    def save_state(self, state: dict):
        with open(self.file_path, 'w', encoding='utf8') as f:
            json.dump(state, f, cls=DateEncoder)

    def retrieve_state(self) -> dict:
        state = {}
        if self.path.exists() and self.path.is_file():
            with open(self.path, 'r', encoding='utf8') as f:
                state = json.load(f)
        return state
