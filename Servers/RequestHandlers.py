"""
Created by adam on 4/23/18
"""
__author__ = 'adam'

import sqlite3
from collections import deque

import tornado.web
from progress.spinner import MoonSpinner, Spinner
from tornado import gen, locks

import environment
from Loggers.FileLoggers import FileWritingLogger
from Servers import Helpers
from Servers.Errors import DBExceptions, ShutdownCommanded
# instrumenting to determine if running async
from profiling.OptimizingTools import timestamp_writer, timestamped_count_writer

file_path_generator = environment.sqlite_file_connection_string_generator()

lock = locks.Lock()


class QHelper( object ):
    spinner = MoonSpinner()

    def __init__( self, batch_size=environment.DB_QUEUE_SIZE ):
        self._queryCount = 0
        self.batch_size = batch_size
        self.store = deque()
        self.file_path = environment.MASTER_DB  # next( file_path_generator )

    def increment_query_count( self ):
        # increment the notification spinner
        type(self).spinner.next()
        # add to the stored request count.
        self._queryCount += 1

    @gen.coroutine
    def enqueue( self, result ):
        rt = (result.text, result.sentence_index, result.word_index, result.id)
        with (yield lock.acquire()):
            self.store.appendleft( rt )
        if len( self.store ) > self.batch_size:
            yield from self.save_queued()

    async def save_queued( self ):
        """Saves all the items in the queue to the db"""
        self.increment_query_count()
        async with lock:
            try:
                # We alternate between several db files to avoid locking
                # problems.
                # file_path = next( file_path_generator )
                timestamp_writer( environment.SERVER_SAVE_LOG_FILE )
                # timestamped_count_writer(environment.SERVER_SAVE_LOG_FILE, self._queryCount, self.file_path)

                conn = sqlite3.connect( self.file_path, isolation_level="EXCLUSIVE" )
                # wrap in a transaction so that other processess can play nice
                with conn:
                    rs = [ self.store.pop() for i in range( 0, len( self.store ) ) ]

                    userQuery = """INSERT INTO word_map_deux (word, sentence_index, word_index, user_id) 
                        VALUES (?, ?, ?, ?)"""
                    conn.executemany( userQuery, rs )

            except Exception as e:
                print( "error for file %s : %s" % (self.file_path, e) )


class UserDescriptionHandler( tornado.web.RequestHandler ):
    """Handles user description requests """

    # share the generator at the class level so that
    # we have a common count
    # file_path_generator = environment.sqlite_file_connection_string_generator()
    # Store results at class level so that any instance
    # can initiate a save for the queue

    q = QHelper()

    _requestCount = 0
    _queryCount = 0

    spinner = Spinner( 'Loading ' )

    logger = FileWritingLogger( name='UserDescriptionHandler' )

    def __init__( self, application, request, **kwargs ):
        self.q = QHelper()
        super().__init__( application, request )

    @classmethod
    def increment_request_count( cls ):
        # increment the notification spinner
        cls.spinner.next()
        # add to the stored request count.
        cls._requestCount += 1

    @property
    def queue_length( self ):
        return len( type( self ).q.store )

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
        # print( "%s in queue; flushing now" % self.queue_length)
        # ql = self.queue_length
        await type( self ).q.save_queued()
        self.write( 'success' )

    @gen.coroutine
    def post( self ):
        """Handles the submision of a list of
        new user-word records.
        """
        timestamp_writer( environment.SERVER_RECEIVE_LOG_FILE )

        type( self ).increment_request_count()

        try:
            # decode json
            payload = Helpers.decode_payload( self.request.body )

            # The payload is a list containing
            # a batch of results.
            # Thus we need to iterate over it
            for p in payload:
                # convert to a Result
                result = Helpers.make_result_from_decoded_payload( p )
                f = '%s/server-received-userids.csv' % environment.PROFILING_LOG_FOLDER_PATH
                timestamped_count_writer(f, result.id, 'userid')

                # push it into the queue
                yield from type( self ).q.enqueue( result )
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
