import os
from logging import config as logging_config

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = os.getenv('PROJECT_NAME', 'movies')

# Настройки Redis
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))

# Настройки Elasticsearch
ELASTIC_HOST = os.getenv('ES_HOST')
ELASTIC_PORT = int(os.getenv('ES_PORT'))

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

origins = [
    "http://localhost:8007",
    "http://localhost",
    "http://localhost:8080",
]
