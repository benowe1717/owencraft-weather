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
    Get the API Key from the environment. This relies on the
    OPENWEATHERMAP_API_KEY environment variable to be set.

    Args:
        None

    Returns:
        The OpenWeatherMap API Key in str format.

    Raises:
        ValueError if the environment variable is not set or empty.
    """
    api_key: str | None = os.getenv('OPENWEATHERMAP_API_KEY')
    if not api_key:
        raise ValueError(f'OPENWEATHERMAP_API_KEY is unset!')
    return api_key


def get_lat_and_lon(zipcode: int, country_code: str) -> tuple[str, str]:
    """
    Retrieve the latitude and longitude from the given zipcode and
    country code.

    https://openweathermap.org/api/geocoding-api#direct_zip

    Args:
        zipcode: An integer representing the location you want to check
        the weather in.
        country_code: A two letter string representing the country the
        zipcode belongs to.

    Returns:
        A tuple representing the Latitude and Longitude matching the
        zipcode and country code. The values are converted from float to str.

    Raises:
        ValueError when the environment variable for the API Key is not set.
        ValueError when the request encounters an HTTPError
        ValueError when the request encounters a ReadTimeout
        ValueError when the request encounters a ConnectionError
        KeyError if the `lat` and `lon` cannot be found in the returned data.
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
    Get the current weather for the given latitude and longitude.

    https://openweathermap.org/api/one-call-3#current

    Args:
        lat: The latitude in str format.
        lon: The longitude in str format.

    Returns:
        An ID representing the current weather.

    Raises:
        ValueError when the environment variable for the API Key is not set.
        ValueError when the request encounters an HTTPError
        ValueError when the request encounters a ReadTimeout
        ValueError when the request encounters a ConnectionError
        KeyError if the `id` cannot be found in the returned data.
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
