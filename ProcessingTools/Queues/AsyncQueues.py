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
from profiling.OptimizingTools import timestamp_writer, timestamped_count_writer

from ProcessingTools.Queues.Interfaces import IQueueHandler
from Servers.Mixins import ResponseStoreMixin

from tornado import gen, locks
from ProcessingTools.Mixins import ProcessIdHaver

lock = locks.Lock()

client_enque_log_file = "%s/client-enque.csv" % environment.PROFILING_LOG_FOLDER_PATH


class AsyncServerQueueDropin( IQueueHandler, ProcessIdHaver ):

    def __init__( self, batch_size=environment.CLIENT_QUEUE_SIZE, client=None ):
        self.id_prefix = 'sqdi.enque'
        super().__init__()
        self.batch_size = batch_size
        self.enquedCount = 0
        self.client = Client() if client is None else client
        self.store = deque()
        self.listeners = [ ]

    @gen.coroutine
    def enque( self, resultList: list, future: asyncio.Future ):
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

        [timestamped_count_writer(client_enque_log_file, r.id, 'userid') for r in resultList]

        with (yield lock.acquire()):
            [ self.store.appendleft( r ) for r in resultList ]

        # users = [ users ] if isinstance( users, DataTools.TweetORM.Users ) else users

        # if we've reached the batch size, send to the server
        # needs to be greater in case hit limit in middle of list
        if len(self.store) >= self.batch_size:
            yield from self.handle_send(future)
        else:
            future.set_result(True)
        return future

    async def handle_send( self, future: asyncio.Future ):
        """Passes the current queue items to the client
        and clears queue.
        This bastard not being async wasted a week of my life
        :type future: asyncio.Future
        """
        b = [ self.store.pop() for _ in range( 0, self.batch_size ) ]

        await self.client.send( b )

        # mark future as done
        # (we aren't waiting for the result, just the sending)
        future.set_result(True)
        return future

    async def flush_queue( self, future ):
        """Sends everything in queue to server"""
        b = [ self.store.pop() for _ in range( 0, len(self.store )) ]

        await self.client.send( b )

        # mark future as done
        # (we aren't waiting for the result, just the sending)
        future.set_result(True)
        return future


def next( self ):
            pass


if __name__ == '__main__':
    pass
