"""
Created by adam on 11/3/16
"""
__author__ = 'adam'

import os, sys
ROOT = os.getenv("HOME")
BASE = '%s/Dropbox/PainNarrativesLab' % ROOT

sys.path.append('%s/Dropbox/iPythonFiles/BaseClasses' % ROOT) #the directory that contains various common custom classes
# sys.path.append('%s/TextTools/ProcessingTools' % BASE) #the directory that contains tools for filtering and manipulating text
sys.path.append('%s/TextTools/' % BASE) #the directory that contains my_pkg

DATAFOLDER = BASE + '/Data'
MAPPING_PATH = "%s/TwitterDataAnalysis/mappings" % BASE
CREDENTIAL_FILE = '%s/private_credentials/sql_local_credentials.xml' % BASE

#Project folders
TEXT_TOOLS_PATH = "%s/TextTools/" % BASE
TWITTER_MINING_PATH = "%s/TwitterMining/" % BASE


# import importlib.util
# spec = importlib.util.spec_from_file_location("WordBagMakers.WordBagMaker", TEXT_TOOLS_PATH)
# wbm = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(wbm)
# from importlib.machinery import SourceFileLoader
# WBM = SourceFileLoader("WordBagMakers.WordBagMaker", "%s/WordBagMakers.py" % TEXT_TOOLS_PATH).load_module()

ENGINE = 'mysql_test' #'sqlite'
DB = 'twitter_words'
# DB = 'twitter_data'

# Whether this is a test
TEST = True

PRINT_STEPS = False

# default tweet id to use in dev
TESTING_TWEET_ID = 123456789


