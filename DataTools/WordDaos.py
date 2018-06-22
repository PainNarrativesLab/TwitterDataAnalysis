"""
Created by adam on 4/12/18
"""
__author__ = 'adam'

import MySQLdb as msq
import MySQLdb.cursors

DB_HOST = '127.0.0.1'
DB_NAME = 'twitter_wordsTEST'
DB_USER = 'root'
DB_PASS = ''


class NonAutocommittingBaseDAO:
    """
    Base data access object.
    Inherited by all classes that need to access the mysql database
    """

    def __init__( self, batchSize=100 ):
        self.mysqlError = MySQLdb.Error
        self.batchSize = batchSize
        self.cnt = 0

        try:

            self.db = msq.connect( DB_HOST, DB_USER, DB_PASS, DB_NAME,
                                   cursorclass=MySQLdb.cursors.DictCursor )
            self.db.autocommit( False )
            self.dbc = self.db.cursor()
            print( 'connected to: ', DB_NAME )
        except MySQLdb.Error as e:
            print( "Connection error: %s " % e )

    def check_flush( self ):
        if self.batchSize <= self.cnt:
            self.db.commit()
            self.cnt = 0
            print( 'committed', self.cnt )

    def executeQuery( self, query, val ):
        """
        Prepares and executes the word_map_table_creation_query stored in self.word_map_table_creation_query with the variables in self.val
        Usually used for insert, update, and other functions which don't require a return
        """
        if type( val ) is not tuple:
            val = (val,)

        try:
            self.dbc.execute( query, val )
            self.cnt += 1
            self.check_flush()

        except MySQLdb.Error as e:
            self.handleError( e )

    def returnOne( self, query, val ):
        """
        Executes the word_map_table_creation_query stored in self.word_map_table_creation_query with the vals in self.val.
        Returns the first row in an array called self.results
        """
        try:
            self.dbc.execute( query, val )
            self.results = self.dbc.fetchone()
        except MySQLdb.Error as e:
            self.handleError( e )

    def handleError( self, error ):
        print( "Query failed: %s " % error )

    def returnAll( self, query, val ):
        """
        Executes the word_map_table_creation_query stored in self.word_map_table_creation_query with the vals in self.val.
        Return the results in an array called self.results
        """
        try:
            self.dbc.execute( query, val )
            self.results = self.dbc.fetchall()
        except MySQLdb.Error as e:
            self.handleError( e )


class WordDAO( NonAutocommittingBaseDAO ):
    def __init__( self, batchsize=100 ):
        super().__init__( batchsize )

    def get_word_id( self, word ):
        """Returns the id of the word if it already exists"""
        try:
            self.executeQuery( """SELECT id FROM words WHERE word = %s""", word )
            r = self.dbc.fetchone()
            return r[ 'id' ]
        except:
            return self.add_word( word )

    def add_word( self, word ):
        """
        Adds a new word to the words table
        Will return the id of the newly inserted word
        """
        q = """INSERT INTO words (word) VALUES (%s)"""
        self.executeQuery( q, word )
        self.db.commit()
        self.dbc.execute( """SELECT LAST_INSERT_ID() AS id""" )
        r = self.dbc.fetchone()
        return r[ 'id' ]


class WordMapDAO( NonAutocommittingBaseDAO ):

    def __init__( self, batchsize=100 ):
        super().__init__( batchsize )

    def add( self, wordId, sentenceIndex, wordIndex, tweetId=None, userId=None ):
        tweetQuery = """INSERT INTO word_map (word_id, sentence_index, word_index, tweet_id) 
            VALUES (%s, %s, %s, %s)"""

        userQuery = """INSERT INTO word_map (word_id, sentence_index, word_index, user_id) 
            VALUES (%s, %s, %s, %s)"""

        if tweetId is not None:
            q = tweetQuery
            oid = tweetId

        if userId is not None:
            q = userQuery
            oid = userId

        return self.executeQuery( q, (wordId, sentenceIndex, wordIndex, oid) )


if __name__ == '__main__':
    pass
