import os
from pathlib import Path

import pendulum

import state
from config import Config
from extract import PostgresExtractor
from load import Load
from logger import logger
from models import Environments
from storage.base import BaseStorage
from storage.json import JsonFileStorage
from transform import DataTransform


class EtlProcessing:

    file_status = '.RUNING'

    def __init__(
            self,
            storage: BaseStorage,
            config: Config,
    ):

        self._check_run_status()
        self._set_run_status()

        self.load_settings = config.load_settings
        self.extract_settings = config.extract_settings
        self.transform_settings = config.transform_settings

        self.state = state.State(storage)

    def _set_run_status(self):
        """Set flag started etl process."""
        open(self.file_status, 'w').close()

    def _check_run_status(self):
        """Raise if other etl process started."""
        path = Path(self.file_status)
        if path.exists():
            raise Exception('Параллельно работает такой же процесс!')

    def _init_state_step(self, name: str) -> None:
        """ Функция инициализации состояния процесса name.
        Если состояние ранее не сохранялось, то выгружаем всё по вчера.
        Если step < 0, то значит предыдущий этап успешно закончился.
        Тогда, устанавливаем дату выгрузки по вчера.
        Не сбиваем сохранённое состояние, если step > 0!

        Args:
            name (str): extract key of EtlProcessing
        """
        state = self.state.get_state(name)
        if state.step is None:
            state.step = 0
            state.date_from = pendulum.parse('1900-01-01', exact=True)
            state.date_to = pendulum.yesterday('UTC').date()
        elif state.step < 0:
            state.step = 0
            state.date_to = pendulum.yesterday('UTC').date()
        self.state.set_state(name, state)

    def extract(self):
        self._init_state_step('extract')
        extracter = PostgresExtractor(
            settings=self.extract_settings,
            state=self.state,
        )
        extracter.extract()

    def transform(self):
        trancformer = DataTransform(
            settings=self.transform_settings,
        )
        trancformer.transform()

    def load(self):
        self._init_state_step('load')
        load = Load(
            self.load_settings,
        )
        load.load()

    def main(self):
        logger.info('Started etl')
        self.extract()
        self.transform()
        self.load()
        os.remove(self.file_status)


if __name__ == '__main__':
    etl = EtlProcessing(
        config=Config(environments=Environments()),
        storage=JsonFileStorage('common/state.json'),
    )
    etl.main()
