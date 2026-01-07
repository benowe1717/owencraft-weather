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

    if weather_id >= 700:
        return 'clear'

    if weather_id >= 300:
        return 'rain'

    if weather_id >= 200:
        return 'storm'

    return 'clear'


if __name__ == '__main__':
    main()
