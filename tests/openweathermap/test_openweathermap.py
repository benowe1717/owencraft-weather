#!/usr/bin/env python3
"""TestOpenWeatherMap class file"""
import pytest

import requests
import requests_mock

from openweathermap import openweathermap


class TestOpenWeatherMap():
    """Tests for functions in openweathermap.py"""

    def set_up(self) -> None:
        self.base_url = 'https://api.openweathermap.org'
        self.zipcode = 10001
        self.api_key = 'b8c37e33defde51cf91e1e03e51657da'
        self.lat = '10.234'
        self.lon = '-10.234'

    def test_get_lat_and_lon_value_error(
            self, requests_mock) -> None:
        self.set_up()
        url = f'/geo/1.0/zip?zip={self.zipcode},US'
        requests_mock.register_uri(
            'GET', url, exc=requests.exceptions.HTTPError)
        with pytest.raises(ValueError):
            openweathermap.get_lat_and_lon(self.zipcode, 'US')

        requests_mock.register_uri(
            'GET', url, exc=requests.exceptions.ReadTimeout)
        with pytest.raises(ValueError):
            openweathermap.get_lat_and_lon(self.zipcode, 'US')

        requests_mock.register_uri(
            'GET', url, exc=requests.exceptions.ConnectionError)
        with pytest.raises(ValueError):
            openweathermap.get_lat_and_lon(self.zipcode, 'US')

    def test_get_lat_and_lon_key_error(
            self, requests_mock: requests_mock.Mocker) -> None:
        self.set_up()
        url = f'/geo/1.0/zip?zip={self.zipcode},US'
        data = {
            'zip': self.zipcode,
            'name': 'New York City',
            'country': 'US',
        }

        requests_mock.register_uri('GET', url, json=data, status_code=200)
        with pytest.raises(KeyError):
            openweathermap.get_lat_and_lon(self.zipcode, 'US')

    def test_get_lat_and_lon_empty_response(
            self, requests_mock: requests_mock.Mocker) -> None:
        self.set_up()
        url = f'/geo/1.0/zip?zip={self.zipcode},US'

        requests_mock.register_uri(
            'GET', url, text='Forbidden', status_code=401)
        lat, lon = openweathermap.get_lat_and_lon(self.zipcode, 'US')
        assert '' == lat
        assert '' == lon

    def test_get_lat_and_lon(
            self,
            requests_mock: requests_mock.Mocker) -> None:
        self.set_up()
        url = f'/geo/1.0/zip?zip={self.zipcode},US'
        data = {
            'zip': self.zipcode,
            'name': 'New York City',
            'country': 'US',
            'lat': 10.234,
            'lon': -10.234,
        }

        requests_mock.register_uri('GET', url, json=data, status_code=200)
        lat, lon = openweathermap.get_lat_and_lon(self.zipcode, 'US')
        assert '10.234' == lat
        assert '-10.234' == lon

    def test_get_current_weather_value_error(
            self, requests_mock) -> None:
        self.set_up()
        url = f'/data/3.0/onecall?lat={self.lat}&lon={self.lon}'
        requests_mock.register_uri(
            'GET', url, exc=requests.exceptions.HTTPError)
        with pytest.raises(ValueError):
            openweathermap.get_current_weather(self.lat, self.lon)

        requests_mock.register_uri(
            'GET', url, exc=requests.exceptions.ReadTimeout)
        with pytest.raises(ValueError):
            openweathermap.get_current_weather(self.lat, self.lon)

        requests_mock.register_uri(
            'GET', url, exc=requests.exceptions.ConnectionError)
        with pytest.raises(ValueError):
            openweathermap.get_current_weather(self.lat, self.lon)

    def test_get_current_weather_key_error(
            self, requests_mock: requests_mock.Mocker) -> None:
        self.set_up()
        url = f'/data/3.0/onecall?lat={self.lat}&lon={self.lon}'
        data = {
            'lat': self.lat,
            'lon': self.lon,
            'timezone': 'America/New_York',
            'current': {
                'weather': [{
                    'main': 'Clouds',
                    'description': 'broken clouds',
                    'icon': '04d'
                }]
            }
        }

        requests_mock.register_uri('GET', url, json=data, status_code=200)
        with pytest.raises(KeyError):
            openweathermap.get_current_weather(self.lat, self.lon)

    def test_get_current_weather_empty_response(
            self, requests_mock: requests_mock.Mocker) -> None:
        self.set_up()
        url = f'/data/3.0/onecall?lat={self.lat}&lon={self.lon}'

        requests_mock.register_uri(
            'GET', url, text='Forbidden', status_code=401)
        weather_id = openweathermap.get_current_weather(self.lat, self.lon)
        assert -1 == weather_id

    def test_get_current_weather(
            self,
            requests_mock: requests_mock.Mocker) -> None:
        self.set_up()
        url = f'/data/3.0/onecall?lat={self.lat}&lon={self.lon}'
        data = {
            'lat': self.lat,
            'lon': self.lon,
            'timezone': 'America/New_York',
            'current': {
                'weather': [{
                    'id': 803,
                    'main': 'Clouds',
                    'description': 'broken clouds',
                    'icon': '04d'
                }]
            }
        }
        requests_mock.register_uri('GET', url, json=data, status_code=200)
        weather_id = openweathermap.get_current_weather(self.lat, self.lon)
        assert 803 == weather_id
