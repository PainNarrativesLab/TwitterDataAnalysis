"""
Created by adam on 11/3/16
"""
__author__ = 'adam'

import os
import sys
ROOT = os.getenv("HOME")


BASE = '%s/Dropbox/PainNarrativesLab' % ROOT
DATAFOLDER = BASE + '/Data'
MAPPING_PATH = "%s/TwitterDataAnalysis/mappings" % BASE
CREDENTIAL_FILE = '%s/private_credentials/sql_local_credentials.xml' % BASE

PROJ_BASE = "%s/TwitterDataAnalysis" % ROOT

# Project folders
TEXT_TOOLS_PATH = "%s/TextTools/" % BASE
TWITTER_MINING_PATH = "%s/TwitterMining/" % BASE

# Logging
LOG_FOLDER_PATH = "%s/Desktop/TwitterDataAnalysisLogs" % ROOT

sys.path.append(PROJ_BASE)
sys.path.append("%s/ProcessingTools" % PROJ_BASE)

sys.path.append("%s/DataTools" % PROJ_BASE)
sys.path.append(TEXT_TOOLS_PATH)
sys.path.append('%s/TextTools/TextProcessors' % BASE)

# the directory that contains various common custom classes
sys.path.append('%s/Dropbox/iPythonFiles/BaseClasses' % ROOT)


DB_FOLDER = "%s/Desktop/TwitterDataAnalysisLogs/dbs" % ROOT
SQLITE_FILE = '%s/wordmapping.db' % LOG_FOLDER_PATH
SQLITE_FILE_CONNECTION_STRING = 'sqlite:////%s' % SQLITE_FILE

MASTER_DB = '%s/master.db' % LOG_FOLDER_PATH

MAX_DB_FILES = 10


def sqlite_file_connection_string_generator(folder_path=DB_FOLDER, max_files=MAX_DB_FILES):
    cnt=1
    while True:
        file = '%s/wordmapping%s.db' % (folder_path, cnt)
        yield file
        # yield 'sqlite:////%s' % file
        if cnt < max_files:
            cnt += 1
        else:
            cnt = 1


# Database server url
DB_PORT = 8599
DB_URL = "http://127.0.0.1:%s" % DB_PORT

# How many transactions to queue before
# flushing / committing to the db
DB_QUEUE_SIZE = 1000

# ENGINE = 'mysql_test'
# ENGINE = 'sqlite'
ENGINE = 'sqlite-file'

# The name of the database to connect to
DB = 'twitter_wordsTEST'
# DB = 'twitter_data'

# Whether this is a test
TEST = True

# Default: False
# Sometimes things go wrong in develoment and
# a transaction will get stuck. This flag gets picked
# up at the head of DataRespositories and calls session.rollback()
PLEASE_ROLLBACK = False

PRINT_STEPS = False

# default tweet id to use in dev
TESTING_TWEET_ID = 123456789

