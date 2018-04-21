"""
Created by adam on 3/27/18
"""
from Servers.Errors import DBExceptions

__author__ = 'adam'

import tornado.ioloop
import tornado.web

import tornado.httpserver

import tornado.log
import Helpers

import time
# from Loggers.FileLoggers import FileWritingLogger
from Loggers.CsvLoggers import log_query, log_query_timestamp
import environment

import sqlite3
import sys

from collections import deque
from profiling.OptimizingTools import time_and_log

class DoneCommanded( Exception ):
    pass


from progress.spinner import Spinner


def write_progress_indicator( to_write ):
    # setup toolbar
    sys.stdout.write( "[%s]" % (to_write) )
    sys.stdout.flush()
    sys.stdout.write( "\b" * 2 )  # return to start of line, after '['
    # if on == 0:
    #     on += 1
    # else:
    #     on = 0


#
# for i in xrange(toolbar_width):
#     time.sleep(0.1) # do real work here
#     # update the bar
#     sys.stdout.write("-")
#     sys.stdout.flush()


class MainHandler( tornado.web.RequestHandler ):
    _requestCount = 0
    # share the generator at the class level so that
    # we have a common count
    file_path_generator = environment.sqlite_file_connection_string_generator()
    # Store results at class level so that any instance
    # can initiate a save for the queue
    results = deque()

    spinner = Spinner( 'Loading ' )

    def __init__( self, application, request, **kwargs ):
        super().__init__( application, request )
        type( self ).spinner.next()
        # print(request)
        # self.engine = _create_sqlite_file_engine(conn=self.file_path)
        # print('j')

    @property
    def i( self ):
        return type( self )._requestCount

    @i.setter
    def i( self, val ):
        type( self )._requestCount = val

    def increment_request_count( self ):
        self.i += 1

    @tornado.gen.coroutine
    def get( self ):
        raise DoneCommanded
        # self.write( "Hello, world" )

    def save_queued( self ):
        """Saves all the items in the queue to the db
        todo consider making this a class method. That may help with saving the last remining results when the batch size has not been met
        """
        try:
            # We alternate between several db files to avoid locking
            # problems.
            # todo Replace with more formal mutex
            self.file_path = next( type( self ).file_path_generator )
            # print(self.file_path)
            conn = sqlite3.connect( self.file_path )

            rs = [ type( self ).results.pop() for i in range( 0, len( type( self ).results.pop() ) ) ]

            userQuery = """INSERT INTO word_map_deux (word, sentence_index, word_index, user_id) 
                VALUES (?, ?, ?, ?)"""
            conn.executemany( userQuery, rs )
            conn.commit()
            conn.close()

        except:
            print( "error for file %s " % self.file_path )

    def enqueue_result( self, result ):
        try:
            rt = (result.text, result.sentence_index, result.word_index, result.id)
            type( self ).results.appendleft( rt )

            if len( type( self ).results ) > environment.DB_QUEUE_SIZE:
                self.save_queued()
        except Exception as e:
            print( "error when enquing %s" % e )

        finally:
            pass
            # self.save_queued()

    # @time_and_log
    def post( self ):

        # t1 = time.time()

        self.increment_request_count()

        try:
            # decode json
            payload = Helpers.decode_payload( self.request.body )

            for p in payload:
                # convert to a Result
                result = Helpers.make_result_from_decoded_payload( p )

                self.enqueue_result( result )
                # type( self ).bar.next()

                # if type( self )._requestCount % environment.DB_QUEUE_SIZE == 0:
                #     print( '%s requests processed' % type( self )._requestCount )

            # t2 = time.time()
            # elapsed = t2 - t1
            # log_query( elapsed )
            # log_query_timestamp()
            # print('took %s seconds' % elapsed)
            # Send success response
            self.write( "success" )

        except DBExceptions as e:
            # self.logger.log_error('db error: %s' % e.message)
            self.write( "error" )


def make_app():
    return tornado.web.Application( [
        (r"/", MainHandler),
    ] )


if __name__ == "__main__":

    # with session_scope() as session:
    # Initialize the shared database repository object
    # which will handle saving to the db
    # dao = DataTools.DataRepositories.MapRepository( session )
    # Workers.SaveWorker.initialize_repository( dao )

    try:
        app = make_app()

        sockets = tornado.netutil.bind_sockets( environment.DB_PORT )
        tornado.process.fork_processes( 0 )  # Forks multiple sub-processes
        server = tornado.httpserver.HTTPServer( app )
        server.add_sockets( sockets )
        print( "Listening on %s" % environment.DB_PORT )
        # Enter loop and listen for requests
        tornado.ioloop.IOLoop.current().start()

    except DoneCommanded:
        pass
        # session.commit()

    except KeyboardInterrupt:
        print( "%s requests received" % MainHandler._requestCount )

    finally:
        pass
        # session.commit()
