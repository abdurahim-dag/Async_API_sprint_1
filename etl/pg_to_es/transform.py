import json
import os
from contextlib import closing
from pathlib import PurePath

from logger import logger
from models import ESIndex, ESIndexLine, Movie, TransformSettings
from utils import UUIDEncoder


class DataTransform:

    def __init__(
        self,
        settings: TransformSettings,
    ):
        self.settings = settings

    def transform(
        self,
    ):
        """Transform pg json formatted to ES format."""
        for src_file in self.settings.extract_path.glob('**/*.json'):
            with closing(open(src_file, 'r', encoding='utf-8')) as file:
                src_json = json.load(file)
            movies = []
            for row in src_json:
                try:
                    # Чекаем данные по модели.
                    movie = Movie(**row[0])
                    movies.append(movie)
                except Exception as err:
                    logger.info("Error on check transform file %s", src_file)
                    raise err

            target_file = PurePath(self.settings.transform_path, src_file.name)
            with closing(open(target_file, 'w', encoding='utf-8')) as file:
                for movie in movies:
                    es_index = ESIndex(
                        _id=movie.id,
                        _index=self.settings.index_name
                    )
                    index_line = ESIndexLine(
                        index=es_index
                    )
                    json.dump(index_line.dict(by_alias=True), file, cls=UUIDEncoder)
                    file.write('\n')
                    json.dump(movie.dict(), file, cls=UUIDEncoder)
                    file.write('\n')

            os.remove(src_file)
