"""
Created by adam on 3/26/18
"""
__author__ = 'adam'

import sys

from logbook import Logger, StreamHandler
from Loggers import ILogger

StreamHandler(sys.stdout).push_application()


class IConsoleLogger(ILogger):
    def __init__(self, name='Default', **kwargs):
        self.name = name
        self._process_kwargs(kwargs)
        super().__init__()


class StdOutLogger(object):
    """Used for logging messages to sys.stdout.
    Mostly used for testing.
    Note: cannot use this and a file logger together without
    one being wrapped in a with statement
    """

    def __init__(self, name='Default', **kwargs):
        self.name = name
        self._process_kwargs(kwargs)
        super().__init__()
