#!/usr/bin/env python3
import sys
import traceback

from src.classes.parseargs import ParseArgs
from src.classes.weather import OpenWeatherMap


def main():
    args = sys.argv
    myparser = ParseArgs(args)
    action = myparser.action

    credentials_file = './src/configs/.creds'
    lat = 36.0178911
    long = -78.8083965
    try:
        weather = OpenWeatherMap(credentials_file, lat, long)

    except ValueError:
        errors = traceback.format_exc().splitlines()
        error = errors[-1]
        print(f'ERROR: {error}')
        exit(1)

    if action == 'test':
        # TODO:
        # Call the weather class test method
        # it makes a basic call and returns a basic check of data
        result = weather.test()
        if not result:
            exit(1)
        exit(0)

    result = weather.onecall()
    if not result:
        exit(1)
    print(weather.weather)


if __name__ == '__main__':
    main()
