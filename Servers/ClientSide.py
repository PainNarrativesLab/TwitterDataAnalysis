"""
Created by adam on 3/27/18
"""
from ProcessingTools.QueueTools import IQueueHandler
from Servers.Mixins import ResponseStoreMixin
__author__ = 'adam'

from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.log import gen_log
from tornado.simple_httpclient import SimpleAsyncHTTPClient
from ProcessingTools.Mixins import ProcessIdHaver
import environment
from Servers import Helpers

from collections import deque

# instrumenting to determine if running async
from profiling.OptimizingTools import write_start_stop, timestamp_writer, standard_timestamp
log_file = "%s/client-send.csv" % environment.LOG_FOLDER_PATH
log_file2 = "%s/client-enque.csv" % environment.LOG_FOLDER_PATH


class NoQueueTimeoutHTTPClient( SimpleAsyncHTTPClient ):
    def fetch_impl( self, request, callback ):
        key = object()

        self.queue.append( (key, request, callback) )
        self.waiting[ key ] = (request, callback, None)

        self._process_queue()

        if self.queue:
            gen_log.debug( "max_clients limit reached, request queued. %d active, %d queued requests." % (
                len( self.active ), len( self.queue )) )


AsyncHTTPClient.configure( NoQueueTimeoutHTTPClient )


class Client( ProcessIdHaver, ResponseStoreMixin ):

    @classmethod
    def initialize_client( cls ):
        cls.http_client = AsyncHTTPClient()

    def __init__( self ):
        self.id_prefix = 'client.send'
        super().__init__()
        self.url = environment.DB_URL
        self.sentCount = 0
        self.errorCount = 0
        self.successCount = 0

        if not hasattr( self, 'http_client' ):
            type( self ).initialize_client()

    # def handle_response(self, response):
    #     """Client side handler of the promise"""
    #     self.successCount += 1
    #     if response.error:
    #         self.logger.log_error(response.error)
    #         self.errorCount += 1
    #     else:
    #         self.successCount += 1
    #

    @gen.coroutine
    def send( self, result ):
        """Post's the result to the server, yields a future"""
        self.sentCount += 1

        # write the timestamp to file
        # we aren't using the decorator for fear
        # it will mess up the async
        timestamp_writer(log_file)

        payload = Helpers.encode_payload( result )
        response = yield self.http_client.fetch( self.url, method="POST", body=payload )
        # response = yield Helpers.send_result(self.http_client, self.url, result)
        # In Python versions prior to 3.3, returning a value from
        # a generator is not allowed and you must use
        #   raise gen.Return(response.body)
        # instead.
        self.add_response(response)
        return response

    def send_flush_command( self, repeat=100 ):
        """Instructs the server to flush the queue of whichever
        handler receives it to the db. The signal thus needs to be
        sent several times to make sure all the handlers receive it
        """
        for _ in range( 0, repeat ):
            self.http_client.fetch( self.url, method="GET" )

    def send_shutdown_command( self ):
        self.http_client.fetch( self.url, method="DELETE" )

    def close( self ):
        self.http_client.close()


class ServerQueueDropin( IQueueHandler, ProcessIdHaver ):

    def __init__( self, batch_size=10 ):
        self.id_prefix = 'sqdi.enque'
        super().__init__()
        self.batch_size = batch_size
        self.enquedCount = 0
        self.client = Client()
        self.store = deque()
        self.listeners = [ ]

    @gen.coroutine
    def enque( self, item ):
        """
        Push a result into the queue for saving to
        the db server. Once the batch size has been reached,
        it will be sent to the server
        """
        # write the timestamp to file

        # write the timestamp to file
        # we aren't using the decorator for fear
        # it will mess up the async
        timestamp_writer(log_file2)

        self.enquedCount += 1
        # print(self.pid, self.enquedCount)
        self.store.appendleft( item )
        if len( self.store ) >= self.batch_size:
            b = [ self.store.pop() for i in range( 0, self.batch_size ) ]
            response = yield self.client.send( b )
            # return response.body
        # return None

    @property
    def sentCount( self ):
        return self.client.sentCount

    @property
    def successCount( self ):
        return self.client.successCount

    @property
    def errorCount( self ):
        return self.client.errorCount

    def next( self ):
        pass


if __name__ == "__main__":
    pass