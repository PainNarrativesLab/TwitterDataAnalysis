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

from NonOrmModels import WordMapDeuxDAO

class DoneCommanded( Exception ):
    pass

# engine = initialize_engine(environment.ENGINE)

# session_factory = make_scoped_session_factory(engine)
# Workers.SaveWorker.initialize_repository( dao )


class MainHandler( tornado.web.RequestHandler ):
    _requestCount = 0
    dao = WordMapDeuxDAO()

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

    # @tornado.gen.coroutine
    def post( self ):
        t1 = time.time()

        self.increment_request_count()

        try:
            # session = session_factory()

            # with session_scope() as session:
            # Initialize the shared database repository object
            # which will handle saving to the db
            # dao = DataTools.DataRepositories.MapRepository( session )

            # decode json
            payload = Helpers.decode_payload( self.request.body )
            # print(payload)

            # convert to a Result
            result = Helpers.make_result_from_decoded_payload( payload )

            # save it
            type( self ).dao.add(result.text, result.sentence_index, result.word_index, tweetId=None, userId=result.id)
            # dao.db.close()
            # dao.save(result)
            # Workers.SaveWorker.run( result )
            #
            # # If we've received enough requests,
            # # flush the changes to the db
            # if type( self )._requestCount % environment.DB_QUEUE_SIZE == 0:
            #     session.commit()
            #     session.flush()

            t2 = time.time()
            elapsed = t2 - t1
            log_query( elapsed )
            log_query_timestamp()
            # print('took %s seconds' % elapsed)
            # Send success response
            self.write( "success" )

        except DBExceptions as e:
            # self.logger.log_error('db error: %s' % e.message)
            self.write( "error" )

        finally:
            pass
            # session.commit()


def make_app():
    return tornado.web.Application( [
        (r"/", MainHandler),
    ] )


if __name__ == "__main__":

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
