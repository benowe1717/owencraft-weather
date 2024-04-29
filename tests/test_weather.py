#!/usr/bin/env python3
import os.path

import pytest
import requests_mock

from src.classes.weather import OpenWeatherMap


class TestOpenWeatherMap():
    def setUp(self):
        self.file = 'tests/data/.creds'
        self.weather = OpenWeatherMap(self.file)

    def tearDown(self):
        del self.weather
        del self.file

    def test_file_exists_failed(self):
        self.setUp()
        file = '/tmp/.creds'
        result = self.weather._file_exists(file)
        assert result is False
        self.tearDown()

    def test_file_exists(self):
        self.setUp()
        result = self.weather._file_exists(self.file)
        assert result is True
        self.tearDown()

    def test_is_file_failed(self):
        self.setUp()
        file = '/tmp'
        result = self.weather._is_file(file)
        assert result is False
        self.tearDown()

    def test_is_file(self):
        self.setUp()
        result = self.weather._is_file(self.file)
        assert result is True
        self.tearDown()

    def test_is_readable_failed(self):
        self.setUp()
        file = '/swapfile'
        result = self.weather._is_readable(file)
        assert result is False
        self.tearDown()

    def test_is_readable(self):
        self.setUp()
        result = self.weather._is_readable(self.file)
        assert result is True
        self.tearDown()

    def test_get_credentials_file(self):
        self.setUp()
        filepath = os.path.abspath(self.file)
        assert self.weather.credentials_file == filepath
        self.tearDown()

    def test_set_credentials_file_failed_not_found(self):
        file = '/tmp/.creds'
        with pytest.raises(ValueError):
            weather = OpenWeatherMap(file)
            assert weather.credentials_file is None

    def test_set_credentials_file_failed_not_file(self):
        file = '/tmp'
        with pytest.raises(ValueError):
            weather = OpenWeatherMap(file)
            assert weather.credentials_file is None

    def test_set_credentials_file_failed_not_readable(self):
        file = '/swapfile'
        with pytest.raises(ValueError):
            weather = OpenWeatherMap(file)
            assert weather.credentials_file is None

    def test_set_credentials_file(self):
        self.setUp()
        filepath = os.path.abspath(self.file)
        weather = OpenWeatherMap(self.file)
        assert weather.credentials_file == filepath
        self.tearDown()

    def test_appid_is_set_correctly_failed(self):
        file = '/tmp/.creds'
        with pytest.raises(ValueError):
            weather = OpenWeatherMap(file)
            assert weather.credentials_file is None
            assert weather._appid is None

    def test_appid_is_set_correctly(self):
        self.setUp()
        filepath = os.path.abspath(self.file)
        with open(filepath, 'r') as file:
            data = file.readlines()[0].strip()
        assert self.weather.credentials_file == filepath
        assert self.weather._appid == data
        self.tearDown()
