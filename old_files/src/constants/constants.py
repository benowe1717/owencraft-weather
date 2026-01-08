#!/usr/bin/env python3

# argparse
ARGPARSE_PROGRAM_NAME = 'set_weather.py'
ARGPARSE_PROGRAM_DESCRIPTION = 'A program to get the current weather for '
ARGPARSE_PROGRAM_DESCRIPTION += 'a given Latitude and Longitude and then set '
ARGPARSE_PROGRAM_DESCRIPTION += 'the retrieved weather on a Minecraft server.'
ARGPARSE_VERSION = '0.0.1'
ARGPARSE_AUTHOR = 'Benjamin Owen'
ARGPARSE_REPO = 'https://github.com/benowe1717/owencraft-weather'

# openweathermap api
API_SCHEME = 'https://'
API_HOST = 'api.openweathermap.org'
API_VERSION = '3.0'
API_BASE_URL = f'{API_SCHEME}{API_HOST}/data/{API_VERSION}'

# mcrcon
MCRCON_HOSTNAME_REGEX = r"^(localhost|[\w\-\_\.]+\.[\w\.]{2,})"
MCRCON_MIN_PORT = 1
MCRCON_MAX_PORT = 65535
MCRCON_WEATHER_TIME = 3600

# main
RAIN_CONDITIONS = ['Rain', 'Drizzle', 'Snow', 'Thunderstorm']
TIME_FORMAT = '%b %d %H:%M:%S'
PROGRAM_NAME = 'OwencraftWeather'
