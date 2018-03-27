"""
Created by adam on 3/27/18
"""
__author__ = 'adam'

from logbook import Logger


class ILogger(object):

    def __init__(self):
        # self.name= name
        # self._process_kwargs(kwargs)
        self.logger = Logger(self.name)

    def _process_kwargs(self, kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def log(self, msg):
        self.logger.notice(msg)

    def log_error(self, msg):
        self.logger.error(msg)


