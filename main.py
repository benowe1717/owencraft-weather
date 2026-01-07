#!/usr/bin/env python3
"""
Owencraft Weather - Control the weather on the Owencraft Minecraft Server

Owencraft Weather - Get the weather forecast from the OpenWeatherMap API
for the given zip code, translate the weather forecast into the available
Minecraft Weather commands, and then set the weather on the target server.
"""
import logging
import sys

from logger import logger
from mcrcon.mcrcon import Mcrcon
from openweathermap import openweathermap
from parseargs.parseargs import ParseArgs


def main() -> None:
    """
    This program's entry point.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """
    parser: ParseArgs = begin()
    tasks(parser)


def begin() -> ParseArgs:
    """
    Setup tasks to make the progam work.

    Args:
        None

    Returns:
        An instance of the ParseArgs class holding all of the arguments
        passed to the running instance of this program

    Raises:
        None
    """
    args: list[str] = sys.argv[1:]
    parser: ParseArgs = ParseArgs(args)
    logger.configure_logger('owencraftWeather')

    return parser


def tasks(parser: ParseArgs) -> None:
    """
    All tasks necessary to get the weather forecast and set the weater.

    Args:
        parser: An instance of the ParseArgs class holding all of the
        arguments passed to the running instance of this program

    Returns:
        None

    Raises:
        None
    """
    owlogger = logging.getLogger('owencraftWeather')
    owlogger.info('Starting script...')

    owlogger.info('Getting latitude and longitude from zipcode...')
    lat, lon = get_lat_and_lon_from_zipcode(
        parser.zipcode, parser.country_code)

    if not lat or not lon:
        owlogger.error('[ERR] Unable to retrieve latitude and longitude!')
        sys.exit(1)

    owlogger.info('Getting current weather...')
    weather_id = get_current_weather(lat, lon)
    current_weather = map_weather_id_to_minecraft_weather(weather_id)

    owlogger.info('Setting current weather...')
    mcrcon: Mcrcon = Mcrcon()
    try:
        mcrcon.set_weather(current_weather)
        owlogger.info('Weather set to `%s`!' % current_weather)
    except ValueError as err:
        owlogger.error(err)
        sys.exit(1)

    owlogger.info('Script finished!')


def get_lat_and_lon_from_zipcode(
        zipcode: int, country_code: str) -> tuple[str, str]:
    """
    Retrieve the latitude and longitude from the given zipcode and
    country code.
    """
    owlogger = logging.getLogger('owencraftWeather')

    try:
        lat, lon = openweathermap.get_lat_and_lon(zipcode, country_code)
        return (lat, lon)
    except (ValueError, KeyError) as err:
        owlogger.error('[ERR] %s' % err)
        sys.exit(1)


def get_current_weather(lat: str, lon: str) -> int:
    """
    Get the current weather for the given latitude and longitude.
    """
    owlogger = logging.getLogger('owencraftWeather')

    try:
        return openweathermap.get_current_weather(lat, lon)
    except (ValueError, KeyError) as err:
        owlogger.error('[ERR] %s' % err)
        sys.exit(1)


def map_weather_id_to_minecraft_weather(weather_id: int) -> str:
    """
    Map the Current Weather ID from OpenWeatherMap to Minecraft Weater.

    https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2
    """
    if weather_id == -1:
        return 'clear'

    storm: list[int] = [200, 201, 202, 210, 211, 212, 221, 230, 231, 232]
    rain: list[int] = [
        300, 301, 302, 310, 311, 312, 313, 314, 321, 500, 501, 502, 503,
        504, 511, 520, 521, 522, 531, 600, 601, 602, 612, 613, 615, 616,
        620, 621, 622]

    if weather_id in storm:
        return 'thunderstorm'

    if weather_id in rain:
        return 'rain'

    return 'clear'


if __name__ == '__main__':
    main()
