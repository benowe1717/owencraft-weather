#!/usr/bin/env python3
"""
Owencraft Weather - Control the weather on the Owencraft Minecraft Server

Owencraft Weather - Get the weather forecast from the OpenWeatherMap API
for the given zip code, translate the weather forecast into the available
Minecraft Weather commands, and then set the weather on the target server.
"""
import sys

from mcrcon.mcrcon import Mcrcon


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
    tasks()


def begin() -> None:
    """
    Setup tasks to make the progam work.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """


def tasks() -> None:
    """
    All tasks necessary to get the weather forecast and set the weater.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """
    mcrcon: Mcrcon = Mcrcon()
    try:
        mcrcon.set_weather('clear')
    except ValueError as err:
        print(err)
        sys.exit(1)


if __name__ == '__main__':
    main()
