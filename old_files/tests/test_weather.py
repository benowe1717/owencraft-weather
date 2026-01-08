#!/usr/bin/env python3
import json
import os.path

import pytest
import requests_mock

from src.classes.weather import OpenWeatherMap


class TestOpenWeatherMap():
    def setUp(self):
        self.file = 'tests/data/.creds'
        self.lat = 36.0178911
        self.long = -78.8083965
        self.weather = OpenWeatherMap(self.file, self.lat, self.long)

    def tearDown(self):
        del self.weather
        del self.long
        del self.lat
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
        self.setUp()
        file = '/tmp/.creds'
        with pytest.raises(ValueError):
            weather = OpenWeatherMap(file, self.lat, self.long)
            assert weather.credentials_file is None
        self.tearDown()

    def test_set_credentials_file_failed_not_file(self):
        self.setUp()
        file = '/tmp'
        with pytest.raises(ValueError):
            weather = OpenWeatherMap(file, self.lat, self.long)
            assert weather.credentials_file is None
        self.tearDown()

    def test_set_credentials_file_failed_not_readable(self):
        self.setUp()
        file = '/swapfile'
        with pytest.raises(ValueError):
            weather = OpenWeatherMap(file, self.lat, self.long)
            assert weather.credentials_file is None
        self.tearDown()

    def test_set_credentials_file(self):
        self.setUp()
        filepath = os.path.abspath(self.file)
        weather = OpenWeatherMap(self.file, self.lat, self.long)
        assert weather.credentials_file == filepath
        self.tearDown()

    def test_appid_is_set_correctly_failed(self):
        self.setUp()
        file = '/tmp/.creds'
        with pytest.raises(ValueError):
            weather = OpenWeatherMap(file, self.lat, self.long)
            assert weather.credentials_file is None
            assert weather._appid is None
        self.tearDown()

    def test_appid_is_set_correctly(self):
        self.setUp()
        filepath = os.path.abspath(self.file)
        with open(filepath, 'r') as file:
            data = file.readlines()[0].strip()
        assert self.weather.credentials_file == filepath
        assert self.weather._appid == data
        self.tearDown()

    def test_onecall_failed_401(self, requests_mock):
        self.setUp()
        endpoint = f'/onecall?lat={self.lat}&lon={self.long}'
        endpoint += '&exclude=minutely,hourly,daily,alerts'
        endpoint += f'&appid={self.weather._appid}'
        url = self.weather.BASE_URL + endpoint
        status_code = 401
        response = {
            'cod': status_code,
            'message': 'Please note that using One Call 3.0 requires a...'
        }
        requests_mock.register_uri(
            'GET',
            url,
            text=json.dumps(response),
            status_code=status_code)
        result = self.weather.onecall()
        assert result is False
        assert self.weather.weather == {}
        self.tearDown()

    def test_onecall(self, requests_mock):
        self.setUp()
        endpoint = f'/onecall?lat={self.lat}&lon={self.long}'
        endpoint += '&exclude=minutely,hourly,daily,alerts'
        endpoint += f'&appid={self.weather._appid}'
        url = self.weather.BASE_URL + endpoint
        status_code = 200
        response = {
            'lat': self.lat,
            'lon': self.long,
            'timezone': 'America/Chicago',
            'timezone_offset': -18000,
            'current': {
                'dt': 1684929490,
                'weather': [
                    {
                        'id': 803,
                        'main': 'Clouds',
                        'description': 'broken clouds',
                        'icon': '04d'
                    }
                ]
            }
        }
        requests_mock.register_uri(
            'GET',
            url,
            text=json.dumps(response),
            status_code=status_code)
        result = self.weather.onecall()
        assert result is True
        assert self.weather.weather == response
        assert 'lat' in self.weather.weather.keys()
        assert self.weather.weather['lat'] == response['lat']
        self.tearDown()

    def test_test_failed(self, requests_mock):
        self.setUp()
        endpoint = f'/onecall?lat={self.lat}&lon={self.long}'
        endpoint += '&exclude=minutely,hourly,daily,alerts'
        endpoint += f'&appid={self.weather._appid}'
        url = self.weather.BASE_URL + endpoint
        status_code = 401
        requests_mock.register_uri(
            'HEAD',
            url,
            status_code=status_code)
        result = self.weather.test()
        assert result is False
        self.tearDown()

    def test_test(self, requests_mock):
        self.setUp()
        endpoint = f'/onecall?lat={self.lat}&lon={self.long}'
        endpoint += '&exclude=minutely,hourly,daily,alerts'
        endpoint += f'&appid={self.weather._appid}'
        url = self.weather.BASE_URL + endpoint
        status_code = 200
        requests_mock.register_uri(
            'HEAD',
            url,
            status_code=status_code)
        result = self.weather.test()
        assert result is True
        self.tearDown()
