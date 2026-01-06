#!/usr/bin/env python3
"""
Owencraft Weather - Control the weather on the Owencraft Minecraft Server

Owencraft Weather - Get the weather forecast from the OpenWeatherMap API
for the given zip code, translate the weather forecast into the available
Minecraft Weather commands, and then set the weather on the target server.
"""
import sys

from mcrcon.mcrcon import Mcrcon
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
    mcrcon: Mcrcon = Mcrcon()
    try:
        mcrcon.set_weather('clear')
    except ValueError as err:
        print(err)
        sys.exit(1)


if __name__ == '__main__':
    main()
