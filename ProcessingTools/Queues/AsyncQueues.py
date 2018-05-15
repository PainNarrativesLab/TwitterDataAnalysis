"""
Created by adam on 5/4/18
"""
__author__ = 'adam'

import environment
from Servers import Helpers
import asyncio

from collections import deque
from Servers.ClientSide import Client
# instrumenting to determine if running async
from profiling.OptimizingTools import timestamp_writer

from ProcessingTools.Queues.Interfaces import IQueueHandler
from Servers.Mixins import ResponseStoreMixin

from tornado import gen
from ProcessingTools.Mixins import ProcessIdHaver


class AsyncServerQueueDropin( IQueueHandler, ProcessIdHaver ):

    def __init__( self, batch_size=10, client=None ):
        self.id_prefix = 'sqdi.enque'
        super().__init__()
        self.batch_size = batch_size
        self.enquedCount = 0
        self.client = Client() if client is None else client
        self.store = deque()
        self.listeners = [ ]

    async def enque( self, resultList: list, future: asyncio.Future ):
        """
        Push a result into the queue for saving to
        the db server. Once the batch size has been reached,
        it will be sent to the server
        :type resultList: list
        :param resultList:
        :type future: asyncio.Future
        """
        # write the timestamp to file
        # we aren't using the decorator for fear
        # it will mess up the async
        timestamp_writer( environment.CLIENT_ENQUE_LOG_FILE )
        resultList = [resultList] if not isinstance(resultList, list) else resultList

        [ self.store.appendleft( r ) for r in resultList ]
        # users = [ users ] if isinstance( users, DataTools.TweetORM.Users ) else users

        # if we've reached the batch size, send to the server
        # needs to be greater in case hit limit in middle of list
        if len(self.store) >= self.batch_size:
            await self.handle_send(future)
        else:
            future.set_result(True)
        return future

    async def handle_send( self, future: asyncio.Future ):
        """Passes the current queue items to the client
        and clears queue
        :type future: asyncio.Future
        """
        b = [ self.store.pop() for _ in range( 0, self.batch_size ) ]

        await self.client.send( b )

        # mark future as done
        # (we aren't waiting for the result, just the sending)
        future.set_result(True)
        return future

    def next( self ):
            pass


if __name__ == '__main__':
    pass
