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
from Servers import Helpers
from Servers.Errors import DBExceptions, ShutdownCommanded

# Loggers and instrumentation
from Loggers.FileLoggers import FileWritingLogger
from profiling.OptimizingTools import timestamp_writer, timestamped_count_writer


lock = locks.Lock()


class QHelper( object ):
    spinner = MoonSpinner()

    def __init__( self, batch_size=environment.DB_QUEUE_SIZE, file_path=environment.MASTER_DB ):
        self._queryCount = 0
        self.batch_size = batch_size
        self.store = deque()
        self.file_path = file_path

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
        """Saves all the items in the queue to the db
        To help with isolation levels From https://www.sqlite.org/lang_transaction.html
        Transactions can be deferred, immediate, or exclusive. The
        default transaction behavior is deferred. Deferred means that no locks are acquired on the database until the
        database is first accessed. Thus with a deferred transaction, the BEGIN statement itself does nothing to the
        filesystem. Locks are not acquired until the first read or write operation. The first read operation against
        a database creates a SHARED lock and the first write operation creates a RESERVED lock. Because the
        acquisition of locks is deferred until they are needed, it is possible that another thread or process could
        create a separate transaction and write to the database after the BEGIN on the current thread has executed.
        If the transaction is immediate, then RESERVED locks are acquired on all databases as soon as the BEGIN
        command is executed, without waiting for the database to be used. After a BEGIN IMMEDIATE, no other database
        connection will be able to write to the database or do a BEGIN IMMEDIATE or BEGIN EXCLUSIVE. Other processes
        can continue to read from the database, however. An exclusive transaction causes EXCLUSIVE locks to be
        acquired on all databases. After a BEGIN EXCLUSIVE, no other database connection except for read_uncommitted
        connections will be able to read the database and no other connection without exception will be able
        to write  the database until the transaction is complete.
        """
        self.increment_query_count()
        async with lock:
            try:
                if environment.TIME_LOGGING:
                    timestamp_writer( environment.SERVER_SAVE_TIMESTAMP_LOG_FILE )

                # create a new connection so not sharing across threads (which is not allowed)
                conn = sqlite3.connect( self.file_path, isolation_level="EXCLUSIVE" )
                # wrap in a transaction so that other processess can play nice
                with conn:
                    rs = [ self.store.pop() for i in range( 0, len( self.store ) ) ]

                    userQuery = """INSERT INTO word_map (word, sentence_index, word_index, user_id) 
                        VALUES (?, ?, ?, ?)"""
                    conn.executemany( userQuery, rs )

            except Exception as e:
                print( "error for file %s : %s" % (self.file_path, e) )


class UserDescriptionHandler( tornado.web.RequestHandler ):
    """Handles user description requests """

    # Queue results at class level so that any instance
    # can initiate a save for the queue. Also prevents losing
    # the queue if the batch size has not been reached when a handler
    # instance is done
    q = QHelper()

    _requestCount = 0
    _queryCount = 0

    spinner = Spinner( 'Loading ' )

    logger = FileWritingLogger( name='UserDescriptionHandler' )

    # def __init__( self, application, request, **kwargs ):
    #     super().__init__( application, request )

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
        cls.q.save_queued()

        message = "Shutdown called. \n # requests: %s \n # queries: %s" % (cls._requestCount, cls._queryCount)
        print( message )
        cls.logger.log( message )
        # emit the command to shutdown the server
        raise ShutdownCommanded
        # (requests=cls._requestCount, queries=cls._queryCount)

    #### Actual handler methods ####

    @gen.coroutine
    def get( self ):
        """Flushes any remaining results in the queue to the dbs"""
        # print( "%s in queue; flushing now" % self.queue_length)
        # ql = self.queue_length
        yield from type( self ).q.save_queued()
        self.write( 'success' )

    @gen.coroutine
    def post( self ):
        """Handles the submision of a list of
        new user-word records.
        """
        if environment.TIME_LOGGING:
            timestamp_writer( environment.SERVER_RECEIVE_TIMESTAMP_LOG_FILE )

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

                if environment.INTEGRITY_LOGGING:
                    timestamped_count_writer(environment.SERVER_RECEIVE_LOG_FILE, result.id, 'userid')

                # push it into the queue
                yield from type( self ).q.enqueue( result )

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
