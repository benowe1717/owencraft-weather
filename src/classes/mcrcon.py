#!/usr/bin/env python3
import os.path
import re
import subprocess

from src.constants import constants


class McRcon():
    HOSTNAME_REGEX = constants.MCRCON_HOSTNAME_REGEX
    MIN_PORT = constants.MCRCON_MIN_PORT
    MAX_PORT = constants.MCRCON_MAX_PORT
    WEATHER_TIME = constants.MCRCON_WEATHER_TIME

    def __init__(
            self,
            mcrcon_filepath: str,
            hostname: str,
            credentials_file: str,
            port=25575) -> None:
        self.mcrcon = mcrcon_filepath
        self.hostname = hostname
        self.port = port
        self.credentials_file = credentials_file
        with open(self.credentials_file, 'r') as file:
            self._password = file.readlines()[0].strip()

    @property
    def mcrcon(self) -> str:
        return self._mcrcon

    @mcrcon.setter
    def mcrcon(self, value: str) -> None:
        filepath = os.path.abspath(value)
        if not self._file_exists(filepath):
            raise ValueError(f'Unable to find {filepath}')
        if not self._is_file(filepath):
            raise ValueError(f'{filepath} is not a file')
        if not self._is_executable(filepath):
            raise ValueError(f'{filepath} is not an executable')
        self._mcrcon = filepath

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

    @property
    def hostname(self) -> str:
        return self._hostname

    @hostname.setter
    def hostname(self, value: str) -> None:
        if not self._is_valid_hostname(value):
            raise ValueError(f'{value} is not a valid hostname')
        self._hostname = value

    @property
    def port(self) -> int:
        return self._port

    @port.setter
    def port(self, value: int) -> None:
        if not self._is_valid_port(value):
            raise ValueError(f'{value} is not a valid port')
        self._port = value

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

    def _is_executable(self, value: str) -> bool:
        if os.access(value, os.X_OK):
            return True
        return False

    def _is_valid_hostname(self, value: str) -> bool:
        if re.match(self.HOSTNAME_REGEX, value):
            return True
        return False

    def _is_valid_port(self, value: int) -> bool:
        if value < self.MIN_PORT or value > self.MAX_PORT:
            return False
        return True

    def set_weather(self, value: str) -> bool:
        cmd = [
            self.mcrcon,
            '-H',
            self.hostname,
            '-P',
            str(self.port),
            '-p',
            self._password,
            f'weather {value} {str(self.WEATHER_TIME)}']
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(result.stderr)
            return False
        return True
