"""
Contains tools for initializing, deleting and otherwise
administering sqlite databases

Tools for accessing the data are in SqliteDataTools


Created by adam on 5/15/18
"""
__author__ = 'adam'

import os
import sqlite3

import environment
from CommonTools.Loggers import delete_files


word_map_table_creation_query = """CREATE TABLE `word_map` (
`tweet_id` int(20) DEFAULT NULL,
  `user_id` int(20) DEFAULT NULL,
  `word` varchar(200) DEFAULT NULL,
  `sentence_index` int(11) DEFAULT NULL,
  `word_index` int(11) DEFAULT NULL)
  """


# make individual tables
def initialize_working_tables():
    for i in range( 0, environment.MAX_DB_FILES + 1 ):
        try:
            f = '%s/wordmapping%s.db' % (environment.DB_FOLDER, i)
            conn = sqlite3.connect( f )
            conn.execute( word_map_table_creation_query )
            conn.commit()
            conn.close()
        except:
            pass


def initialize_word_map_db(filepath):
    try:
        conn = sqlite3.connect( filepath )
        with conn:
            conn.execute( word_map_table_creation_query )
            conn.commit()
            conn.close()
    except:
        pass


def initialize_master_db():
    try:
        initialize_word_map_db(environment.MASTER_DB)
    except:
        pass


def delete_master_db():
    os.remove( environment.MASTER_DB )


def delete_working_files():
    delete_files( environment.DB_FOLDER )


if __name__ == '__main__':
    pass
