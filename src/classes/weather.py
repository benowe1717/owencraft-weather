#!/usr/bin/env python3
import os.path

from src.constants import constants


class OpenWeatherMap():
    API_VERSION = constants.API_VERSION
    HOST = constants.API_HOST
    BASE_URL = constants.API_BASE_URL

    def __init__(self, credentials_file) -> None:
        self.credentials_file = credentials_file
        with open(self.credentials_file, 'r') as file:
            self._appid = file.readlines()[0].strip()
        self._headers = {
            'Accept': 'application/json',
            'Host': self.HOST
        }

    @property
    def credentials_file(self) -> str:
        return self._credentials_file

    @credentials_file.setter
    def credentials_file(self, value: str) -> None:
        filepath = os.path.abspath(value)
        if not self._file_exists(filepath):
            raise ValueError(f'Unable to find {filepath}')
        if not self._is_file(filepath):
            raise ValueError(f'{filepath} is not a file')
        if not self._is_readable(filepath):
            raise ValueError(f'{filepath} is not readable')
        self._credentials_file = filepath

    def _file_exists(self, value: str) -> bool:
        if os.path.exists(value):
            return True
        return False

    def _is_file(self, value: str) -> bool:
        if os.path.isfile(value):
            return True
        return False

    def _is_readable(self, value: str) -> bool:
        if os.access(value, os.R_OK):
            return True
        return False
