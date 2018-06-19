"""
Contains tools for accessing and assessing data in sqlite databases

Tools for  initializing, deleting and otherwise
administering sqlite databases are in SqliteTools


Created by adam on 5/31/18
"""
__author__ = 'adam'

import sqlite3

import environment


def _run_query( query, db=environment.MASTER_DB ):
    conn = sqlite3.connect( db )
    with conn:
        r2 = conn.execute( query )
        amt = r2.fetchone()
        return amt[ 0 ]


def count_words( db=environment.MASTER_DB ):
    query = "select count( distinct word) from word_map"
    amt = _run_query( query, db )
    print( "%s distinct words in master.db" % amt )
    return amt


def count_rows( db=environment.MASTER_DB ):
    query = "select count( *) from word_map"
    amt = _run_query( query, db )
    print( "%s rows in %s" % (amt, db) )
    return amt


def count_tweets( db=environment.MASTER_DB ):
    query = "select count(distinct tweet_id) from word_map"
    amt = _run_query( query, db )
    print( "%s tweets in master.db" % amt )
    return amt


# Distinct users
def count_users( db=environment.MASTER_DB ):
    conn = sqlite3.connect( db )
    r = conn.execute( "select count(distinct user_id) from word_map" )
    n = r.fetchone()
    print( "%s unique user ids in %s" % (n[ 0 ], db) )
    conn.close()


def master_row_generator():
    """Creates a generator which returns one row at a time"""
    conn = sqlite3.connect(environment.MASTER_DB)
    r = conn.execute("select * from word_map")
    while True:
        yield r.fetchone()


def db_row_generator(filepath):
    conn = sqlite3.connect(filepath)
    r = conn.execute("select * from word_map")
    while True:
        yield r.fetchone()


if __name__ == '__main__':
    pass
