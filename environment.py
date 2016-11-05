"""
Created by adam on 11/3/16
"""
__author__ = 'adam'

import os

BASE = os.getenv( "HOME" ) + '/Dropbox/PainNarrativesLab'
DATAFOLDER = BASE + '/Data'
MAPPING_PATH = "%s/TwitterDataAnalysis/mappings" % BASE

CREDENTIAL_FILE = '%s/private_credentials/sql_local_credentials.xml' % BASE