"""
Created by adam on 3/26/18
"""

__author__ = 'adam'
import os

from logbook import FileHandler

from Loggers.ILogger import ILogger

BASE = os.getenv("HOME")
# todo restore environment
# from TwitterDataAnalysis.environment import *

# Logging
LOG_FOLDER_PATH = "%s/Desktop/TwitterDataAnalysisLogs" % BASE

DEFAULT_LOG_FILE_NAME = 'twitter_log.txt'
DEFAULT_LOG_FILE_PATH = "%s/%s" % (LOG_FOLDER_PATH, DEFAULT_LOG_FILE_NAME)

log_handler = FileHandler(DEFAULT_LOG_FILE_PATH)
log_handler.push_application()


class FileWritingLogger(ILogger):

    def __init__(self, **kwargs):
        """ kwargs may contain: name """
        self.name = 'Default'
        self._process_kwargs(kwargs)
        super().__init__()

    def add_break( self ):
        self.log( "=====================================================" )



# class DBEventLogger(LogWriter):
#     """
#     Handles logging and printing information about database events
#     """
#
#     def __init__(self, client_send_log_file=DEFAULT_LOG_FILE_NAME):
#         self.log = ''
#         super().__init__()
#         self.client_send_log_file = client_send_log_file
#         # self.UPATH = os.getenv("HOME")
#         # self.client_send_log_file = '%s/Desktop/%s' % self.UPATH, client_send_log_file
#         # self.client_send_log_file = "application_search.log"
#         self.set_log_file(self.client_send_log_file)
