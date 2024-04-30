#!/usr/bin/env python3
import sys
import traceback

from src.classes.mcrcon import McRcon
from src.classes.parseargs import ParseArgs
from src.classes.weather import OpenWeatherMap
from src.constants import constants


def get_weather(weather: dict) -> str:
    condition = weather['current']['weather'][0]['main']
    if condition in constants.RAIN_CONDITIONS:
        return 'rain'
    return 'clear'


def main():
    args = sys.argv
    myparser = ParseArgs(args)
    action = myparser.action

    credentials_file = './src/configs/.creds'
    lat = 36.0178911
    long = -78.8083965

    mcrcon_file = '/usr/local/bin/mcrcon'
    hostname = 'localhost'
    creds_file = './src/configs/.mcrcon'
    try:
        weather = OpenWeatherMap(credentials_file, lat, long)
        mcrcon = McRcon(mcrcon_file, hostname, creds_file)

    except ValueError:
        errors = traceback.format_exc().splitlines()
        error = errors[-1]
        print(f'ERROR: {error}')
        exit(1)

    if action == 'test':
        result = weather.test()
        if not result:
            exit(1)
        print('Your credentials work!')
        exit(0)

    result = weather.onecall()
    if not result:
        exit(1)
    condition = get_weather(weather.weather)

    result = mcrcon.set_weather(condition)
    if not result:
        exit(1)


if __name__ == '__main__':
    main()
