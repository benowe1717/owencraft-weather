#!/usr/bin/env python3
import os.path

import requests

from src.constants import constants


class OpenWeatherMap():
    API_VERSION = constants.API_VERSION
    HOST = constants.API_HOST
    BASE_URL = constants.API_BASE_URL

    def __init__(self, credentials_file, lat: float, long: float) -> None:
        self.credentials_file = credentials_file
        with open(self.credentials_file, 'r') as file:
            self._appid = file.readlines()[0].strip()
        self._headers = {
            'Accept': 'application/json',
            'Host': self.HOST
        }
        self.lat = lat
        self.long = long
        self.weather = {}

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

    def _handle_error_response(self, response: requests.Response) -> None:
        text = ''
        for key, value in response.json().items():
            text += f'[{key}] {value} '
        msg = f'ERROR: {response.status_code} :: {text.strip()}'
        print(msg)

    def onecall(self) -> bool:
        exclude = 'minutely,hourly,daily,alerts'
        endpoint = f'/onecall?lat={self.lat}&lon={self.long}'
        endpoint += f'&exclude={exclude}&appid={self._appid}'
        url = self.BASE_URL + endpoint
        r = requests.get(url=url, headers=self._headers)
        if r.status_code == 200:
            self.weather = r.json()
            return True
        else:
            self._handle_error_response(r)
            return False

    def test(self) -> bool:
        exclude = 'minutely,hourly,daily,alerts'
        endpoint = f'/onecall?lat={self.lat}&lon={self.long}'
        endpoint += f'&exclude={exclude}&appid={self._appid}'
        url = self.BASE_URL + endpoint
        r = requests.head(url=url, headers=self._headers)
        if r.status_code == 200:
            return True
        else:
            print(f'ERROR: Status Code: {r.status_code}')
            return False
