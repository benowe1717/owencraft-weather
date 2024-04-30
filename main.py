#!/usr/bin/env python3
import logging
import logging.config
import os
import sys
import traceback
from datetime import datetime

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
    logger_conf = './src/configs/logging.config'
    logger_conf_filepath = os.path.abspath(logger_conf)
    if not os.path.exists(logger_conf):
        print(f'ERROR: Unable to locate {logger_conf_filepath}')
        exit(1)
    logging.config.fileConfig(logger_conf_filepath)
    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.event_date = datetime.now().strftime(constants.TIME_FORMAT)
        record.hostname = os.uname().nodename
        record.program = constants.PROGRAM_NAME
        record.pid = os.getpid()
        return record

    logging.setLogRecordFactory(record_factory)
    logger = logging.getLogger(constants.PROGRAM_NAME)

    args = sys.argv
    myparser = ParseArgs(args)
    action = myparser.action

    logger.info('Starting script...')

    credentials_file = './src/configs/.creds'
    lat = 36.0178911
    long = -78.8083965

    mcrcon_file = '/usr/local/bin/mcrcon'
    hostname = 'localhost'
    creds_file = './src/configs/.mcrcon'
    try:
        logger.info('Starting up the OpenWeatherMap class...')
        weather = OpenWeatherMap(credentials_file, lat, long)

        logger.info('Starting up the McRcon class...')
        mcrcon = McRcon(mcrcon_file, hostname, creds_file)

    except ValueError:
        errors = traceback.format_exc().splitlines()
        error = errors[-1]
        logger.error(f'ERROR: {error}')
        exit(1)

    if action == 'test':
        logger.info('Testing your credentials...')
        result = weather.test()
        if not result:
            exit(1)
        logger.info('Your credentials work!')
        logger.info('Script finished successfully!')
        exit(0)

    logger.info('Getting the current weather...')
    result = weather.onecall()
    if not result:
        exit(1)
    condition = get_weather(weather.weather)
    logger.info(f'The weather right now is {condition}!')

    logger.info('Setting the weather on the Owencraft server...')
    result = mcrcon.set_weather(condition)
    if not result:
        exit(1)
    logger.info('Weather has been set!')

    logger.info('Script finished successfully!')


if __name__ == '__main__':
    main()
