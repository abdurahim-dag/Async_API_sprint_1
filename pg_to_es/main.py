from models import Environments, Movie, Genre
from storage.json import JsonFileStorage
from .etl import EtlProcessing
from config import Config
from state import State
from logger import logger


if __name__ == '__main__':

    etl_targets = {
        'extract.sql': {
            'model': Movie,
            'es_index': 'movies',
            'es_schema_file': 'es_schema.json'

        },
        'extract_genres.sql': {
            'model': Genre,
            'es_index': 'genres',
            'es_schema_file': 'es_schema_genres.json'

        },
    }
    storage = JsonFileStorage('common/state.json')

    envs = Environments(_env_file='.env.edv', _env_file_encoding='utf-8')

    for sql_file_name, etl_target in etl_targets:

        config = Config(
            environments=envs,
            es_index=etl_target['es_index'],
            es_schema_file_name=etl_target['es_schema_file'],
            sql_extract_file_name=sql_file_name,
            model=etl_target['model'],

        )


        state = State(
            storage=storage,
            key=envs.sql_extract_file_name,
        )

        logger.info(f"Etl for {envs.sql_extract_file_name} started!")


        model=models[envs.sql_extract_file_name],

        etl = EtlProcessing(
            extract_settings=config.extract_settings,
            load_settings=config.load_settings,
            transform_settings=config.transform_settings,
            state=state,
            state_key=envs.sql_extract_file_name,
        )
        etl.main()

        logger.info(f"Etl for {envs.sql_extract_file_name} finished!")