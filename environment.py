"""
Created by adam on 11/3/16
"""
__author__ = 'adam'

import os

BASE = os.getenv( "HOME" ) + '/Dropbox/PainNarrativesLab'
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

ENGINE = 'sqlite'
TEST = True

# default tweet id to use in dev
TESTING_TWEET_ID = 123456789