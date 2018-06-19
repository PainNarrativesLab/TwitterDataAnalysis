"""
Created by adam on 5/24/18
"""
__author__ = 'adam'

import sqlite3

import environment
from SearchTools.WordMaps import get_user_ids_for_word


class PrivationAlert( Exception ):
    pass


class DoneAlert( Exception ):
    pass


def get_by_position( user_id, word_index, sentence_index, conn ):
    query2 = """
          SELECT m.user_id, m.word_index, m.word
          FROM word_map m
          WHERE m.user_id=? AND m.word_index=? AND m.sentence_index=?"""

    r = conn.execute( query2, (user_id, word_index, sentence_index) )
    return r.fetchall()


def find_userids_for_ngram( ngram, db=environment.USER_DB_NO_STOP ):
    # split the ngram on spaces
    words = ngram.split( ' ' )

    # how far into the ngram list we are
    depth = 0

    conn = sqlite3.connect( db )
    # we get all users for whom the first word
    # of the n-gram appears in their description.
    # From here, it is just a matter of removing the
    # ones which don't have the rest of the words
    results = get_user_ids_for_word( words[ 0 ], db )

    # check that some results exist
    if len( results ) == 0:
        raise DoneAlert
    for i, record in results:
        try:
            user = record[ 0 ]
            idx = record[ 1 ]
            sent = record[ 2 ]

            for word in words[ 1: ]:
                nxt_idx = idx + 1
                r = get_by_position( user, nxt_idx, sent )
                if len( r ) == 0:
                    # The next word in the ngram is not present.
                    # So we signal that this isn't a user we are looking for
                    raise PrivationAlert
        except PrivationAlert:
            results.remove( i )

    if (len( words ) > 1):
        for record in have_first:
            user = record[ 0 ]
            idx = record[ 1 ] + 1
            sent = record[ 2 ]

            r2 = conn.execute( query2, (user, idx, sent) )

    conn.close()


if __name__ == '__main__':
    pass
