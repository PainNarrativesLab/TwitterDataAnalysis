"""
Created by adam on 11/3/16
"""
__author__ = 'adam'

import os
import sys

# Whether this is a test
TEST = True

############## Locations of code
ROOT = os.getenv( "HOME" )
BASE = '%s/Dropbox/PainNarrativesLab' % ROOT
DATAFOLDER = BASE + '/Data'
MAPPING_PATH = "%s/TwitterDataAnalysis/mappings" % BASE
CREDENTIAL_FILE = '%s/private_credentials/sql_local_credentials.xml' % BASE
SLACK_CREDENTIAL_FILE = "%s/private_credentials/slack-credentials.xml" % BASE
PROJ_BASE = "%s/TwitterDataAnalysis" % ROOT

# Project folder paths
TEXT_TOOLS_PATH = "%s/TextTools/" % BASE
TWITTER_MINING_PATH = "%s/TwitterMining/" % BASE

# Logging folder paths
LOG_FOLDER_PATH = "%s/Desktop/TwitterDataAnalysisLogs" % ROOT
PROFILING_LOG_FOLDER_PATH = "%s/profiling" % LOG_FOLDER_PATH
INTEGRITY_LOG_FOLDER_PATH = "%s/integrity" % LOG_FOLDER_PATH

# add everyone to path explicitly
sys.path.append( PROJ_BASE )
sys.path.append( TEXT_TOOLS_PATH )
sys.path.append( "%s/DataTools" % PROJ_BASE )
sys.path.append( "%s/Executables" % PROJ_BASE )
sys.path.append( "%s/Loggers" % PROJ_BASE )
sys.path.append( '%s/TextTools/TextProcessors' % BASE )
sys.path.append( "%s/ProcessingTools" % PROJ_BASE )
sys.path.append( "%s/profiling" % PROJ_BASE )
sys.path.append( '%s/Servers' % BASE )

# the directory that contains various common custom classes
sys.path.append( '%s/Dropbox/iPythonFiles/BaseClasses' % ROOT )

############################## Queues ###############################
# How many transactions to queue before
# flushing / committing
DB_QUEUE_SIZE = 1000
CLIENT_QUEUE_SIZE = 700

####################### DB files ##################################
# sqlite db files
DB_FOLDER = "%s/Desktop/TwitterDataAnalysisLogs/dbs" % ROOT
SQLITE_FILE = '%s/wordmapping.db' % LOG_FOLDER_PATH
SQLITE_FILE_CONNECTION_STRING = 'sqlite:////%s' % SQLITE_FILE
MASTER_DB = '%s/master.db' % LOG_FOLDER_PATH  # the file things get compiled into
MAX_DB_FILES = 10  # the maximum number of db files to create.


def sqlite_file_connection_string_generator( folder_path=DB_FOLDER, max_files=MAX_DB_FILES ):
    cnt = 1
    while True:
        file = '%s/wordmapping%s.db' % (folder_path, cnt)
        yield file
        # yield 'sqlite:////%s' % file
        if cnt < max_files:
            cnt += 1
        else:
            cnt = 1


################################# Database ############################
# Database server url
DB_PORT = 8691
DB_URL = "http://127.0.0.1:%s" % DB_PORT

# ENGINE = 'mysql_test'
# ENGINE = 'sqlite'
ENGINE = 'sqlite-file'

# The name of the database to connect to
if TEST:
    DB = 'twitter_wordsTEST'
else:
    DB = 'twitter_users'
# DB = 'twitter_data'


# Sometimes things go wrong in develoment and
# a transaction will get stuck. This flag gets picked
# up at the head of DataRespositories and calls session.rollback()
PLEASE_ROLLBACK = False
PRINT_STEPS = False

####################### Logging #################################
############ Whether to log
# Log the id of each user or tweet as they pass through each
# stage of processing. This is used for ensuring accuracy.
INTEGRITY_LOGGING = False
# Record a timestamp for various stages for use in tuning
TIME_LOGGING = False
# Whether to send result to Slack webhook
SLACK_NOTIFY = True

############ Files
######## User flow logging (tracking progress of user)
PROCESSING_ENQUE_LOG_FILE = "%s/processing-enque.csv" % PROFILING_LOG_FOLDER_PATH
# records timestamp every time a list of results from a user are pushed into the
# client side queue from the processor
CLIENT_ENQUE_LOG_FILE = "%s/client-enque.csv" % INTEGRITY_LOG_FOLDER_PATH
CLIENT_SEND_LOG_FILE = "%s/client-send.csv" % INTEGRITY_LOG_FOLDER_PATH
SERVER_RECEIVE_LOG_FILE = "%s/server-receive.csv" % INTEGRITY_LOG_FOLDER_PATH
SERVER_SAVE_LOG_FILE = "%s/server-save.csv" % INTEGRITY_LOG_FOLDER_PATH

####### Time logging
CLIENT_ENQUE_TIMESTAMP_LOG_FILE = "%s/client-enque.csv" % PROFILING_LOG_FOLDER_PATH
CLIENT_SEND_TIMESTAMP_LOG_FILE = "%s/client-send.csv" % PROFILING_LOG_FOLDER_PATH
SERVER_RECEIVE_TIMESTAMP_LOG_FILE = "%s/server-receive.csv" % PROFILING_LOG_FOLDER_PATH
SERVER_SAVE_TIMESTAMP_LOG_FILE = "%s/server-save.csv" % PROFILING_LOG_FOLDER_PATH
QUERY_LOG = '%s/QUERY_LOG.csv' % LOG_FOLDER_PATH
QUERY_TIME_LOG = '%s/QUERY_TIME_LOG.csv' % LOG_FOLDER_PATH

########## Permanent logs
# semi-permanent log of how long it takes to run user processing
# this gets written to regardless of whether TIME_LOGGING is True
RUN_TIME_LOG = '%s/user-processing-run-time-log.csv' % LOG_FOLDER_PATH
