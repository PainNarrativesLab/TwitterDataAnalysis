"""
Created by adam on 4/23/18
"""
__author__ = 'adam'

import sqlite3
from collections import deque

import Helpers
import tornado.web
from progress.spinner import Spinner

import environment
from Servers.Errors import DBExceptions
from profiling.OptimizingTools import time_and_log_query, time_and_log_request


class DoneCommanded( Exception ):
    pass


class UserDescriptionHandler( tornado.web.RequestHandler ):
    """Handles user description requests """

    # share the generator at the class level so that
    # we have a common count
    file_path_generator = environment.sqlite_file_connection_string_generator()
    # Store results at class level so that any instance
    # can initiate a save for the queue
    results = deque()

    _requestCount = 0

    spinner = Spinner( 'Loading ' )

    def __init__( self, application, request, **kwargs ):
        super().__init__( application, request )

    @property
    def i( self ):
        return type( self )._requestCount

    @i.setter
    def i( self, val ):
        type( self )._requestCount = val

    def increment_request_count( self ):
        self.i += 1

    def get( self ):
        print( "%s still in queue" % len( UserDescriptionHandler.results ) )
        type( self ).save_queued()
        print( "%s in queue after flush" % len( UserDescriptionHandler.results ) )
        self.write( "Hello, world" )

    @classmethod
    @time_and_log_query
    def save_queued( cls ):
        """Saves all the items in the queue to the db"""
        try:
            # We alternate between several db files to avoid locking
            # problems.
            # todo Replace with more formal mutex
            file_path = next( cls.file_path_generator )

            conn = sqlite3.connect( file_path )

            rs = [ cls.results.pop() for i in range( 0, len( cls.results ) ) ]

            userQuery = """INSERT INTO word_map_deux (word, sentence_index, word_index, user_id) 
                VALUES (?, ?, ?, ?)"""
            conn.executemany( userQuery, rs )
            conn.commit()
            conn.close()

        except Exception as e:
            print( "error for file %s : %s" % (file_path, e) )

    @classmethod
    def enqueue_result( cls, result ):
        try:
            rt = (result.text, result.sentence_index, result.word_index, result.id)
            cls.results.appendleft( rt )
            if len( cls.results ) > environment.DB_QUEUE_SIZE:
                cls.save_queued()

        except Exception as e:
            print( "error when enquing %s" % e )

    @time_and_log_request
    def post( self ):

        self.increment_request_count()

        try:
            # decode json
            payload = Helpers.decode_payload( self.request.body )

            for p in payload:
                # convert to a Result
                result = Helpers.make_result_from_decoded_payload( p )
                type( self ).enqueue_result( result )

            # increment the notification spinner
            type( self ).spinner.next()

            # Send success response
            self.write( "success" )

        except DBExceptions as e:
            # self.logger.log_error('db error: %s' % e.message)
            self.write( "error" )


if __name__ == '__main__':
    pass
