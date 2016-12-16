"""
Created by adam on 11/24/16
"""
__author__ = 'adam'

from environment import *

# Load cursor for tweet ids
import DataTools.TweetORM
import threading

class threadsafe_iter:
    """Takes an iterator/generator and makes it thread-safe by
    serializing call to the `next` method of given iterator/generator.
    """

    def __init__( self, it ):
        self.it = it
        self.lock = threading.Lock( )

    def __iter__( self ):
        return self

    def next( self ):
        with self.lock:
            return self.it.next( )


def threadsafe_generator( f ):
    """A decorator that takes a generator function and makes it thread-safe.
    """
    def g( *a, **kw ):
        return threadsafe_iter( f( *a, **kw ) )

    return g


class TweetCursor( object ):
    """Provides a generator for getting one tweet at a time from the db"""

    def __init__( self, limit=None ):
        """
        :param limit: The maximum number to retrieve. If unset, will iterate over all tweets
        """
        self.limit = limit
        self.tweet_iterator = None
        self.lock = threading.Lock( )

        # load the db connection info
        conn = DataTools.TweetORM.MySqlConnection( CREDENTIAL_FILE )

        # create the session connection to the db
        self.dao = DataTools.TweetORM.DAO( conn.engine )

        # if self.tweet_iterator == None:
        #     print('creating new iterator')
        self.tweet_iterator = self._create_tweet_iterator( )

    # @threadsafe_generator
    def _create_tweet_iterator( self ):
        """Gets tweets and creates an iterator which is accessed via next_tweet"""
        if PRINT_STEPS is True: print ("_create_tweet_iterator")
        if self.limit is not None:
            # print( "_create_tweet_iterator" )
            for t in self.dao.session.query( DataTools.TweetORM.Tweet ).limit( self.limit ).all( ):
                yield t
        else:
            for t in self.dao.session.query( DataTools.TweetORM.Tweet ).all( ):
                yield t

    def next(self):
        with self.lock:
            return next( self.tweet_iterator )
        # return self.tweet_iterator.next()

    def next_tweet( self ):
        """Returns the next tweet object from the db"""
        # return self.tweet_iterator.next()
        with self.lock:
            return next( self.tweet_iterator )
