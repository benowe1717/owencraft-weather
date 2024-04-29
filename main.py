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
    try:
        weather = OpenWeatherMap(credentials_file)

    except ValueError:
        errors = traceback.format_exc().splitlines()
        error = errors[-1]
        print(f'ERROR: {error}')
        exit(1)

    if action == 'test':
        # TODO:
        # Call the weather class test method
        # it makes a basic call and returns a basic check of data
        pass


if __name__ == '__main__':
    main()
