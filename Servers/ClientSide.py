"""
Created by adam on 3/27/18
"""
from ProcessingTools.QueueTools import IQueueHandler

__author__ = 'adam'

from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.log import gen_log
from tornado.simple_httpclient import SimpleAsyncHTTPClient

import environment
from Servers import Helpers


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


class Client( object ):

    @classmethod
    def initialize_client( cls ):
        Client.http_client = AsyncHTTPClient()

    def __init__( self ):
        self.url = environment.DB_URL
        self.sentCount = 0
        self.errorCount = 0
        self.successCount = 0
        # self.logger = FileWritingLogger(name='Client Response ')

        if not hasattr( self, 'http_client' ):
            Client.initialize_client()

    # def handle_response(self, response):
    #     """Client side handler of the promise"""
    #     self.successCount += 1
    #     if response.error:
    #         self.logger.log_error(response.error)
    #         self.errorCount += 1
    #     else:
    #         self.successCount += 1
    #
    # # @gen.coroutine
    # def send_result(self, result):
    #     """Uses the client to make a request"""
    #     payload = Helpers.encode_payload(result)
    #     return self.client.fetch(self.url, self.handle_response, method="POST", body=payload)

    @gen.coroutine
    def send_result( self, result ):
        """Uses the client to make a request
        NOT YET WORKING
        """
        payload = Helpers.encode_payload( result )
        response = yield self.http_client.fetch( self.url, method="POST", body=payload )
        return response.body

    @gen.coroutine
    def send( self, result ):
        """Post's the result to the server, yields a future"""
        self.sentCount += 1
        # yield self.send_result(result)
        payload = Helpers.encode_payload( result )
        response = yield self.http_client.fetch( self.url, method="POST", body=payload )
        # response = yield Helpers.send_result(self.http_client, self.url, result)
        # In Python versions prior to 3.3, returning a value from
        # a generator is not allowed and you must use
        #   raise gen.Return(response.body)
        # instead.
        return response

    def close( self ):
        self.http_client.close()


class ServerQueueDropin( IQueueHandler ):

    def __init__( self ):
        super().__init__()
        self.enquedCount = 0
        self.client = Client()
        self.listeners = [ ]

    @gen.coroutine
    def enque( self, item ):
        """Send to the db server to be recorded"""
        self.enquedCount += 1
        response = yield self.client.send( item )

        # print('bingo')
        return response.body

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
