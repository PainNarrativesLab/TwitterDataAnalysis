"""
Created by adam on 11/24/16
"""
__author__ = 'adam'

from environment import *

# Load cursor for tweet ids
import DataTools.TweetORM


class TweetCursor( object ):
    """Provides a generator for getting one tweet at a time from the db"""

    def __init__( self, limit=None ):
        """
        :param limit: The maximum number to retrieve. If unset, will iterate over all tweets
        """

        self.limit = limit

        # load the db connection info
        conn = DataTools.TweetORM.MySqlConnection( CREDENTIAL_FILE )

        # create the session connection to the db
        self.dao = DataTools.TweetORM.DAO( conn.engine )
        self.tweet_iterator = self._create_tweet_iterator( )

    def _create_tweet_iterator( self ):
        """Gets tweets and creates an iterator which is accessed via next_tweet"""
        if self.limit is not None:
            for t in self.dao.session.query( DataTools.TweetORM.Tweet ).limit( self.limit ).all( ):
                yield t
        else:
            for t in self.dao.session.query( DataTools.TweetORM.Tweet ).all( ):
                yield t

    def next_tweet( self ):
        """Returns the next tweet object from the db"""
        return next( self.tweet_iterator )
