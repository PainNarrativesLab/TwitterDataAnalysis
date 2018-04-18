"""
Created by adam on 11/24/16
"""
__author__ = 'adam'

import threading

# Load cursor for tweet ids
import DataTools.TweetORM
from DataTools import DataConnections
from environment import *


class threadsafe_iter:
    """Takes an iterator/generator and makes it thread-safe by
    serializing call to the `next` method of given iterator/generator.
    """

    def __init__(self, it):
        self.it = it
        self.lock = threading.Lock()

    def __iter__(self):
        return self

    def next(self):
        with self.lock:
            return self.it.next()


def threadsafe_generator(f):
    """A decorator that takes a generator function and makes it thread-safe.
    """

    def g(*a, **kw):
        return threadsafe_iter(f(*a, **kw))

    return g


class Cursor(object):
    def __init__(self):
        self.item_iterator = None
        self.language = None
        self.limit = None
        self.valid_args = [ 'language', 'limit' ]

    def create_dao( self ):
        # load the db connection info
        conn = DataConnections.MySqlConnection( CREDENTIAL_FILE )

        # create the session connection to the db
        self.dao = DataConnections.DAO( conn.engine )

        print( 'connection ready' )

    def _process_kwargs(self, kwargs):
        """ Iterate through the strings stored in valid_args and set any values on self"""
        for key, value in kwargs.items():
            if key in self.valid_args:
                setattr(self, key, value)

    def _create_iterator(self):
        raise NotImplementedError

    def next(self):
        # with self.lock:
        return next(self.item_iterator)


class TweetCursor(Cursor):
    """Provides a generator for getting one tweet at a time from the db"""

    def __init__(self, limit=None):
        """
        :param limit: The maximum number to retrieve. If unset, will iterate over all tweets
        """
        super().__init__()
        self.limit = limit
        self.lock = threading.Lock()

        # load the db connection info
        conn = DataConnections.MySqlConnection(CREDENTIAL_FILE)

        # create the session connection to the db
        self.dao = DataConnections.DAO(conn.engine)

        # if self.tweet_iterator == None:
        #     print('creating new iterator')
        self.item_iterator = self._create_iterator()

    # @threadsafe_generator
    def _create_iterator(self):
        """Gets tweets and creates an iterator which is accessed via next_tweet"""
        if PRINT_STEPS is True: print("_create_tweet_iterator")

        q = self.dao.session.query(DataTools.TweetORM.Tweet)

        if self.limit is not None:
            q = q.limit(self.limit)

        for t in q.all():
            yield t

        # print( "_create_tweet_iterator" )
        # for t in self.dao.session.query(DataTools.TweetORM.Tweet).limit(self.limit).all():
        #     yield t
        #
        # else:
        #     for t in self.dao.session.query(DataTools.TweetORM.Tweet).all():
        #         yield t

    def next_tweet(self):
        """Returns the next tweet object from the db"""
        # return self.tweet_iterator.next()
        with self.lock:
            return self.next()
            # return next(self.item_iterator)


class UserCursor(Cursor):
    """
    Provides a generator for getting one user at a time from the db
    Usage (assuming in ipython)
        %run -i DataTools/Cursors
        u = UserCursor()
        k = u.next()
        k.userID (or whatever property we are interested in)
    """

    def __init__(self, **kwargs):
        """
        :param limit: The maximum number to retrieve. If unset, will iterate over all tweets
        """
        super().__init__()
        self.lock = threading.Lock()
        self._process_kwargs(kwargs)
        self.create_dao()

        self.item_iterator = self._create_iterator()

    # @threadsafe_generator
    def _create_iterator(self):
        """Gets users and creates an iterator which is accessed via next_tweet"""
        if PRINT_STEPS is True: print("_create_user_iterator")

        q = self.dao.session.query(DataTools.TweetORM.Users)

        if self.limit is not None:
            q.limit(self.limit)

        if self.language is not None:
            q = q.filter(DataTools.TweetORM.Users.lang == self.language)

        for t in q.all():
            yield t

            #
            # for t in self.dao.session.query(DataTools.TweetORM.Users).limit(self.limit).all():
            # for t in q.filter(DataTools.TweetORM.Users.lang == self.language) \
            #         .all():
            #
            # for t in self.dao.session\
            #         .query(DataTools.TweetORM.Users)\
            #         .filter(DataTools.TweetORM.Users.lang == self.language)\
            #         .all():
            #     yield t
        # else:
        # for t in self.dao.session.query(DataTools.TweetORM.Users).all():
        #     yield t

    def next_user(self):
        """Returns the next user object from the db"""
        # return self.tweet_iterator.next()
        # with self.lock:
        # return self.next()
        return next( self.item_iterator )


class WindowedUserCursor( Cursor ):
    def __init__( self, **kwargs ):
        super().__init__()
        # For auditing purposes
        self.callCount = 0
        self.firstId = 0
        self.limit = 4
        self.pk_attr = DataTools.TweetORM.Users.userID
        self.model = DataTools.TweetORM.Users
        # potentially override the above defaults
        self._process_kwargs( kwargs )
        self.create_dao()

        self.qry = self.dao.session.query( self.model )

        # Create the iterator object
        self.my_iter = self._create_iterator()

    def next( self ):
        self.callCount += 1
        return next( self.my_iter )

    def _create_iterator( self ):

        while True:
            q = self.qry
            if self.firstId is not None:
                # get records with ids higher than our highest current
                q = self.qry.filter( self.pk_attr > self.firstId )
            rec = None
            for rec in q.order_by( self.pk_attr ).limit( self.limit ):
                yield rec
            if rec is None:
                break
            self.firstId = self.pk_attr.__get__( rec, self.pk_attr ) if rec else None
