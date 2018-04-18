"""
Created by adam on 3/27/18
"""
from Servers.Errors import DBExceptions

__author__ = 'adam'

import tornado.ioloop
import tornado.web

import tornado.httpserver

import tornado.log
import DataTools.DataRepositories
import ProcessingTools.Workers as Workers
import Helpers

import time
# from Loggers.FileLoggers import FileWritingLogger
from Loggers.CsvLoggers import log_query, log_query_timestamp
from DataConnections import session_scope
# DataTools.DataRepositories.create_global_session()


# from DataTools.WordORM import *
import environment


# from sqlalchemy.orm import sessionmaker

class DoneCommanded( Exception ):
    pass


class MainHandler( tornado.web.RequestHandler ):
    _requestCount = 0

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
            # decode json
            payload = Helpers.decode_payload( self.request.body )
            # print(payload)

            # convert to a Result
            result = Helpers.make_result_from_decoded_payload( payload )

            # save it
            Workers.SaveWorker.run( result )
            # dao.save(result)
            if type( self )._requestCount > environment.DB_QUEUE_SIZE:
                Workers.SaveWorker.repository.session.commit()
                Workers.SaveWorker.repository.session.flush()
                type( self )._requestCount = 0

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


def make_app():
    return tornado.web.Application( [
        (r"/", MainHandler),
    ] )


if __name__ == "__main__":
    # logger = FileWritingLogger(name='DB Logger')
    # # We need a single db connection instance for all of the
    # # server processes. Otherwise, we will have trouble with
    # # concurrent writes to the file.
    # # That's what we create here
    # try:
    #     if type( engine ) is not None:
    #         pass
    # except NameError:
    #     # connect to db
    #     engine = DataConnections.initialize_engine()
    #     # DataTools's handle to database at global level
    #     Session = sessionmaker( bind=engine)
    #
    # if environment.ENGINE == 'sqlite' or environment.ENGINE == 'sqlite-file':
    #     # We need to get the db into memory when start up
    #     # environmental variables will determine details of the
    #     # db
    #     create_db_tables( engine )
    #
    # session = Session()
    # #     if PLEASE_ROLLBACK is True:
    # #         session.rollback()

    with session_scope() as session:
        # dao = DataTools.DataRepositories.WordRepository(session)
        dao = DataTools.DataRepositories.MapRepository( session )
        Workers.SaveWorker.initialize_repository( dao )
    try:

        app = make_app()
        # app.listen(environment.DB_PORT)
        print( "Listening on %s" % environment.DB_PORT )

        # server = tornado.httpserver.HTTPServer( app )
        # server.bind( environment.DB_PORT )
        # server.start( 0 )  # Forks multiple sub-processes
        # tornado.ioloop.IOLoop.current().start()

        sockets = tornado.netutil.bind_sockets( environment.DB_PORT )
        tornado.process.fork_processes( 0 )
        server = tornado.httpserver.HTTPServer( app )
        server.add_sockets( sockets )
        tornado.ioloop.IOLoop.current().start()

    except DoneCommanded:
        pass
    except KeyboardInterrupt:
        pass
        # todo Try using an in memory db and then flush to file here
        print( "%s requests received" % MainHandler.i )
        print( "%s requests received" % MainHandler._requestCount )
    finally:
        session.commit()
# logger.log("Listening on %s" % environment.DB_PORT)

# channel = logging.StreamHandler(sys.stdout)
# # channel.setLevel(log_level)
# channel.setFormatter(tornado.log.LogFormatter())
#
# app_log = logging.getLogger("tornado.application")
# gen_log = logging.getLogger("tornado.general")
# app_log.addHandler(channel)

# try:
