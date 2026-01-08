#!/usr/bin/env python3
"""
Set up the logging module for the application
"""
import logging
import os
import socket
import sys

from datetime import datetime


def get_hostname() -> str:
    """
    Return the device's hostname.

    Args:
        None

    Returns:
        The device's hostname in str format.

    Raises:
        None
    """
    return socket.gethostname()


def get_pid() -> int:
    """
    Return the program's process ID.

    Args:
        None

    Returns:
        The current program's process ID in integer format.

    Raises:
        None
    """
    return os.getpid()


def configure_logger(name: str) -> None:
    """
    Configure the application's logger.

    Args:
        name: The name of the logger to configure in str format. This name
        will be used throughout the entire application.

    Returns:
        None

    Raises:
        None
    """
    logger: logging.Logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(sys.path[0] + f'/logs/{name}.log', 'a+')
    formatter = logging.Formatter(
        '%(event_date)s %(hostname)s %(program)s[%(pid)d] %(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)

    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.event_date = datetime.now().strftime('%b %d %H:%M:%S')
        record.hostname = get_hostname()
        record.program = name
        record.pid = get_pid()
        return record

    logging.setLogRecordFactory(record_factory)
