"""
Created by adam on 3/26/18
"""
import datetime

__author__ = 'adam'
import os

import csv

BASE = os.getenv( "HOME" )
# todo restore environment
# from TwitterDataAnalysis.environment import *

# Logging
LOG_FOLDER_PATH = "%s/Desktop/TwitterDataAnalysisLogs" % BASE

query_log = '%s/query_log.csv' % LOG_FOLDER_PATH
query_time_log = '%s/query_time_log.csv' % LOG_FOLDER_PATH

DEFAULT_LOG_FILE_NAME = 'twitter_log.txt'
DEFAULT_LOG_FILE_PATH = "%s/%s" % (LOG_FOLDER_PATH, DEFAULT_LOG_FILE_NAME)


def log_query( seconds, logFile=query_log ):
    with open( logFile, 'a' ) as csvfile:
        writer = csv.writer( csvfile )
        # writer.writerow([seconds])
        # ts = datetime.datetime.isoformat(datetime.datetime.now())
        # ts = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")
        writer.writerow( [ seconds ] )


def log_query_timestamp( logFile=query_time_log ):
    with open( logFile, 'a' ) as csvfile:
        writer = csv.writer( csvfile )
        # writer.writerow([seconds])
        ts = datetime.datetime.isoformat( datetime.datetime.now() )
        # ts = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")
        writer.writerow( [ ts ] )
