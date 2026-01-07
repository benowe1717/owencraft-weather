#!/usr/bin/env python3
"""
OpenWeatherMap API Wrapper

These functions are used to interact with the OpenWeatherMap One Call 3.0
REST API. Docs can be found here: https://openweathermap.org/api/one-call-3
"""
import logging
import os
from typing import Any

import requests

SCHEME: str = 'https'
DOMAIN: str = 'api.openweathermap.org'
BASE_URL: str = f'{SCHEME}://{DOMAIN}'
LOGGER = logging.getLogger('owencraftWeater')


def get_api_key() -> str:
    """
    Get the API Key from the environment
    """
    api_key: str | None = os.getenv('OPENWEATHERMAP_API_KEY')
    if not api_key:
        raise ValueError(f'OPENWEATHERMAP_API_KEY is unset!')
    return api_key


def get_lat_and_lon(zipcode: int, country_code: str) -> tuple[str, str]:
    """
    Get the Latitude and Longitude from the given zipcode and country code.

    https://openweathermap.org/api/geocoding-api#direct_zip
    """
    try:
        api_key: str = get_api_key()
    except ValueError as err:
        raise ValueError(err) from err

    uri: str = f'geo/1.0/zip?zip={zipcode},{country_code}&appid={api_key}'
    url: str = f'{BASE_URL}/{uri}'

    try:
        response: requests.Response = requests.get(url=url, timeout=10)
        if response.status_code != 200:
            LOGGER.error(
                '[ERR] %s :: %s' %
                (response.status_code, response.text))
            return ('', '')

        data: dict[str, Any] = response.json()
        lat: str = str(data['lat'])
        lon: str = str(data['lon'])
        return (lat, lon)
    except (
            requests.exceptions.HTTPError,
            requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectionError) as err:
        raise ValueError(err) from err
    except KeyError as err:
        raise KeyError(err) from err


def get_current_weather(lat: str, lon: str) -> int:
    """
    Get the current weather from the given Latitude and Longitude.

    https://openweathermap.org/api/one-call-3#current
    """
    try:
        api_key: str = get_api_key()
    except ValueError as err:
        raise ValueError(err) from err

    parts: list[str] = ['data/3.0/onecall?lat=', lat, '&lon=', lon,
                        '&exclude=minutely,hourly,daily,alerts&appid=', api_key]
    uri: str = ''.join(parts)
    url: str = f'{BASE_URL}/{uri}'

    try:
        response: requests.Response = requests.get(url=url, timeout=10)
        if response.status_code != 200:
            LOGGER.error(
                '[ERR] %s :: %s' %
                (response.status_code, response.text))
            return -1

        data: dict[str, Any] = response.json()
        return data['current']['weather'][0]['id']
    except (
            requests.exceptions.HTTPError,
            requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectionError) as err:
        raise ValueError(err) from err
    except KeyError as err:
        raise KeyError(err) from err
