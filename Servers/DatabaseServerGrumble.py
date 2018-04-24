"""
Created by adam on 3/27/18
"""
from Servers.Errors import DBExceptions

__author__ = 'adam'

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.log

import environment
import Helpers
from RequestHandlers import UserDescriptionHandler


class DoneCommanded( Exception ):
    pass


def make_app():
    return tornado.web.Application( [
        (r"/", UserDescriptionHandler),
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
        UserDescriptionHandler.save_queued()
        # pass
        # session.commit()

    except KeyboardInterrupt:
        # print("%s still in queue" % len(UserDescriptionHandler.results))
        # UserDescriptionHandler.save_queued()
        # print("%s in queue after flush" % len(UserDescriptionHandler.results))
        print( "%s requests received" % UserDescriptionHandler._requestCount )

    finally:
        # UserDescriptionHandler.save_queued()
        pass
        # session.commit()
