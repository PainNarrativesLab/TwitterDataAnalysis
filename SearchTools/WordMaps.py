"""
These are tools for finding data in the word_map
tables
Created by adam on 5/23/18
"""
__author__ = 'adam'
import sqlite3

import environment


def attach_id_map(connection):
    query = """ATTACH DATABASE '%s' as id_map;""" % (environment.ID_MAP_DB)
    connection.execute(query)


def get_adjacent_word_counts( word: str, offset: int, cutoff: int = None, db: str = environment.USER_DB_NO_STOP ):
    """Returns a list of tuples containing counts of the words which
    are in the offset position relative to the string.

    For example, given "Cats smell much better than dogs"
    calling this for 'smell', we get
        offset= -1:  counts of words in the position of 'Cats';
        offset= 1: counts words in the position of 'better'

    The result has the form: [('acute', 37), ('advanced', 15),....]
    :param offset: The relative position to tabulate count of words
    :param db: The filepath to the sqlite db to search
    :param word: The string to search for in word_map
    :param cutoff: If None, returns all results. Otherwise, returns only results with counts >= the cutoff
 """
    if offset >= 0:
        # negative numbers will bring the subtraction sign w them
        offset = '+ %s' % offset
    query = """
    SELECT a.word, count(a.word)
          FROM word_map a
          JOIN (
              SELECT m.user_id AS uid, 
              m.word_index %s AS wix
              FROM word_map m
              WHERE m.word=?
              ) AS b
            ON (a.user_id = b.uid)
            WHERE a.word_index = b.wix
            group by a.word
        """ % offset
    conn = sqlite3.connect( db )
    s = (word,)
    r = conn.execute( query, s )

    if cutoff is None:
        return r.fetchall()
    return [ x for x in r if x[ 1 ] >= cutoff ]


def get_adjacent_word_counts_in_tweets( word: str, offset: int, cutoff: int = None, db: str = environment.TWEET_DB_MASTER ):
    """Returns a list of tuples containing counts of the words which
    are in the offset position relative to the string.

    For example, given "Cats smell much better than dogs"
    calling this for 'smell', we get
        offset= -1:  counts of words in the position of 'Cats';
        offset= 1: counts words in the position of 'better'

    The result has the form: [('acute', 37), ('advanced', 15),....]
    :param offset: The relative position to tabulate count of words
    :param db: The filepath to the sqlite db to search
    :param word: The string to search for in word_map
    :param cutoff: If None, returns all results. Otherwise, returns only results with counts >= the cutoff
 """
    if offset >= 0:
        # negative numbers will bring the subtraction sign w them
        offset = '+ %s' % offset
    query = """
    SELECT a.word, count(a.word)
          FROM word_map a
          JOIN (
              SELECT m.tweet_id AS tid, 
              m.word_index %s AS wix
              FROM word_map m
              WHERE m.word=?
              ) AS b
            ON (a.tweet_id = b.tid)
            WHERE a.word_index = b.wix
            group by a.word
        """ % offset
    conn = sqlite3.connect( db )
    s = (word,)
    r = conn.execute( query, s )

    if cutoff is None:
        return r.fetchall()
    return [ x for x in r if x[ 1 ] >= cutoff ]



def get_adjacent_words( word: str, offset: int, db: str = environment.USER_DB_NO_STOP ):
    """
    Returns a list of tuples containing the immediately
    preceeding word and the user/ tweet ids.
    There will be many tuples with the same string.

    The result has the form:
    [ (word, user_id, tweet_id), ...]
     For example:
        [('el', 93937824, 837824), ('el', 213937824, 5213937824),
        ('y', 213937824, 5213937824), ...]

    :param offset:
    :param word:
    :param db:
    :return:
    """
    if offset >= 0:
        # negative numbers will bring the subtraction sign w them
        offset = '+ %s' % offset

    query = """
          SELECT a.word 
          a.user_id,
          a.tweet_id
          FROM word_map a
          JOIN (
              SELECT m.user_id AS uid, 
              m.word_index %s AS wix
              FROM word_map m
              WHERE m.word=?
              ) AS b
            ON (a.user_id = b.uid)
            WHERE a.word_index = b.wix
        """ % offset
    conn = sqlite3.connect( db )
    s = (word,)
    r = conn.execute( query, s )
    return r.fetchall()
    conn.close()


def get_user_ids_for_word( word, db=environment.USER_DB_NO_STOP ):
    """Returns the ids of users who use the word in their profiles"""
    query = """
          SELECT m.user_id, m.word_index, m.sentence_index
          FROM word_map m
          WHERE m.word=?
    """
    conn = sqlite3.connect( db )
    s = (word,)
    r = conn.execute( query, s )
    return r.fetchall()
    conn.close()


def get_tweet_ids_for_word( word, db=environment.TWEET_DB_MASTER):
    """Returns the ids of tweets containing  the word """
    query = """
              SELECT m.tweet_id, m.word_index, m.sentence_index
              FROM word_map m
              WHERE m.word=?
        """
    conn = sqlite3.connect( db )
    s = (word,)
    r = conn.execute( query, s )
    return r.fetchall()
    conn.close()

# word_map_table_creation_query = """
#           SELECT m.tweet_id, idm.user_id, m.word_index, m.sentence_index
#           FROM word_map m
#           JOIN idm
#           ON(m.tweet_id = idm.tweet_id)
#           WHERE m.word=?
#     """
#     conn = sqlite3.connect( db )
#     with conn:
#         curs = conn.cursor()  # Attach cursor
#         query0 = """ATTACH DATABASE %s as idm ;""" % environment.ID_MAP_DB
#         curs.execute(query0)
#
#         # attach_id_map(conn)
#         s = (word,)
#         r = curs.execute( word_map_table_creation_query, s )
#         return r.fetchall()


if __name__ == '__main__':
    pass
