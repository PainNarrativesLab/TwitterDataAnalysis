"""
Created by adam on 4/23/18
"""
__author__ = 'adam'

import sqlite3
from collections import deque

import tornado.web
from tornado import gen, locks
from progress.spinner import MoonSpinner, Spinner

import environment
from Loggers.FileLoggers import FileWritingLogger
from Servers import Helpers
from Servers.Errors import DBExceptions, ShutdownCommanded
from profiling.OptimizingTools import time_and_log_query, log_start_stop

# instrumenting to determine if running async
from profiling.OptimizingTools import timestamp_writer, timestamped_count_writer

file_path_generator = environment.sqlite_file_connection_string_generator()

lock = locks.Lock()

class QHelper(object):

    def __init__(self, batch_size=environment.DB_QUEUE_SIZE):
        self._queryCount = 0
        self.batch_size = batch_size
        self.store = deque()

    def increment_query_count( self ):
        # increment the notification spinner
        # self.spinner2.next()
        # add to the stored request count.
        self._queryCount += 1

    @gen.coroutine
    def enqueue( self, result ):
        rt = (result.text, result.sentence_index, result.word_index, result.id)
        self.store.appendleft(rt)
        if len( self.store ) > self.batch_size:
            yield from self.save_queued()

    async def save_queued( self ):
        """Saves all the items in the queue to the db"""
        self.increment_query_count()
        async with lock:
            try:
                # We alternate between several db files to avoid locking
                # problems.
                file_path = next( file_path_generator )

                timestamped_count_writer(environment.SERVER_SAVE_LOG_FILE, self._queryCount, file_path)

                conn = sqlite3.connect( file_path )

                rs = [ self.store.pop() for i in range( 0, len( self.store ) ) ]

                userQuery = """INSERT INTO word_map_deux (word, sentence_index, word_index, user_id) 
                    VALUES (?, ?, ?, ?)"""
                conn.executemany( userQuery, rs )
                conn.commit()
                conn.close()

            except Exception as e:
                print( "error for file %s : %s" % (file_path, e) )
        # lock is now released
        return True


class UserDescriptionHandler( tornado.web.RequestHandler ):
    """Handles user description requests """

    # share the generator at the class level so that
    # we have a common count
    # file_path_generator = environment.sqlite_file_connection_string_generator()
    # Store results at class level so that any instance
    # can initiate a save for the queue
    results = deque()

    q = QHelper()

    _requestCount = 0
    _queryCount = 0

    spinner = Spinner( 'Loading ' )
    spinner2 = MoonSpinner()

    logger = FileWritingLogger( name='UserDescriptionHandler' )

    # def __init__( self, application, request, **kwargs ):
    #     super().__init__( application, request )

    @classmethod
    def increment_request_count( cls ):
        # increment the notification spinner
        cls.spinner.next()
        # add to the stored request count.
        cls._requestCount += 1

    # @classmethod
    # def increment_query_count( cls ):
    #     # increment the notification spinner
    #     cls.spinner2.next()
    #     # add to the stored request count.
    #     cls._queryCount += 1

    # @classmethod
    # @log_start_stop( [ environment.QUERY_TIME_LOG ] )
    # def save_queued( cls ):
    #     """Saves all the items in the queue to the db"""
    #     cls.increment_query_count()
    #
    #     # timestamp_writer( environment.SERVER_SAVE_LOG_FILE )
    #     try:
    #         # We alternate between several db files to avoid locking
    #         # problems.
    #         file_path = next( file_path_generator )
    #         timestamped_count_writer(environment.SERVER_SAVE_LOG_FILE, cls._queryCount, file_path)
    #
    #         conn = sqlite3.connect( file_path )
    #
    #         rs = [ cls.results.pop() for i in range( 0, len( cls.results ) ) ]
    #
    #         userQuery = """INSERT INTO word_map_deux (word, sentence_index, word_index, user_id)
    #             VALUES (?, ?, ?, ?)"""
    #         conn.executemany( userQuery, rs )
    #         conn.commit()
    #         conn.close()
    #
    #     except Exception as e:
    #         print( "error for file %s : %s" % (file_path, e) )

    # @classmethod
    # def enqueue_result( cls, result ):
    #     cls.increment_request_count()
    #
    #     try:
    #         rt = (result.text, result.sentence_index, result.word_index, result.id)
    #         cls.results.appendleft( rt )
    #         if len( cls.results ) > environment.DB_QUEUE_SIZE:
    #             cls.save_queued()
    #
    #     except Exception as e:
    #         print( "error when enquing %s" % e )

    @classmethod
    def shutdown( cls ):
        """This handles the client side command to cease all
        server operations. That involves flushing the
        queue and writing to requisite log files"""
        # flush the queue (for this handler instance!)
        # todo make the queue fully shared
        cls.save_queued()

        message = "Shutdown called. \n # requests: %s \n # queries: %s" % (cls._requestCount, cls._queryCount)
        print( message )
        cls.logger.log( message )
        # emit the command to shutdown the server
        raise ShutdownCommanded
        # (requests=cls._requestCount, queries=cls._queryCount)

    #### Actual handler methods ####

    async def get( self ):
        """Flushes any remaining results in the queue to the dbs"""
        print("Flush called on handler")
        print( "%s still in queue" % len( UserDescriptionHandler.results ) )
        await type( self ).q.save_queued()
        print( "%s in queue after flush" % len( UserDescriptionHandler.results ) )
        self.write( "success" )

    # @log_start_stop([environment.QUERY_LOG])
    @gen.coroutine
    def post( self ):
        """Handles the submision of a list of
        new user-word records.
        """
        # timestamp_writer( environment.SERVER_RECEIVE_LOG_FILE )

        type(self).increment_request_count()
        timestamped_count_writer(environment.SERVER_RECEIVE_LOG_FILE, type(self)._requestCount)

        try:
            # decode json
            payload = Helpers.decode_payload( self.request.body )

            # The payload is a list containing
            # a batch of results.
            # Thus we need to iterate over it
            for p in payload:
                # convert to a Result
                result = Helpers.make_result_from_decoded_payload( p )
                # push it into the queue
                yield from type( self ).q.enqueue(result)
                # type( self ).enqueue_result( result )

            # Send success response
            yield self.write( "success" )

        except DBExceptions as e:
            # self.logger.log_error('db error: %s' % e.message)
            self.write( "error" )

    def delete( self ):
        """closes all operations"""
        type( self ).shutdown()


if __name__ == '__main__':
    pass
