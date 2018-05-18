"""
Created by adam on 5/4/18
"""

__author__ = 'adam'

import asyncio

from ProcessingTools.Queues import AsyncQueues
from Servers.Mixins import ResponseStoreMixin
from ProcessingTools.Processors.AsyncProcessing import Processor


class Control( ResponseStoreMixin ):

    def __init__( self, queueHandler=None, processor=None ):
        """
        :type queueHandler: Service class which puts the word in the queue to be saved, so that's not a bottleneck
        """
        self.count_of_processed = 0
        self.queueHandler = AsyncQueues.AsyncServerQueueDropin() if queueHandler is None else queueHandler
        self.processor = Processor() if processor is None else processor
        super().__init__()

    @property
    def is_over_limit( self ):
        """Check if we are over limit. Issues StopIteration since
        this won't get raised by the cursor
        given that we are stopping due to a user imposed limit
        """
        if self.limit is not None and self.count_of_processed >= self.limit:
            raise StopIteration

        return False

    async def _process( self, user, future ):
        """Calls the processor on the user and
        returns a list of results from the object.
        """
        # Process the item and return
        # a list of result objects
        resultsList = self.processor.process( user )
        # create a future which will control when we
        # go on to the next item from the cursor
        # Now we push it into the queue along with a future,
        # when the future
        await self.queueHandler.enque( resultsList, future )
        return future

    async def process_from_cursor( self, cursor, limit=None ):
        """This is the main method which sets the entire
        processing process in motion.
        It iterates over the objects returned by the cursor
        :param cursor: DB cursor object
        :type limit: int
        """
        self.cursor = cursor
        self.limit = limit
        overall_future = asyncio.Future()

        while True:
            try:
                if self.is_over_limit:
                    overall_future.set_result( True )
                    return overall_future

                # we're good to go. Processing user
                future = asyncio.Future()
                user = self.cursor.next()
                self.count_of_processed += 1
                await self._process( user, future )

            except StopIteration as e:
                print( "%s users processed" % self.count_of_processed )
                future = asyncio.Future()
                await self.queueHandler.flush_queue(future)
                return overall_future.set_result( True )

    # async def process_next( self, *args, **kwargs ):
    #     """Runs the processing on the next item in the cursor
    #     This runs synchronously.
    #     """
    #     print('process next called')
    #
    #     try:
    #         # while True:
    #         # if self.is_over_limit:
    #         #     self.overall_future.set_result(True)
    #         #     return self.overall_future
    #         #
    #         # future = asyncio.Future()
    #         #
    #         # user = self.cursor.next()
    #         # self.count_of_processed += 1
    #         # # First process the item into a list of results objects
    #         resultsList = self.processor.process( user )
    #         # create a future which will control when we
    #         # go on to the next item from the cursor
    #         future.add_done_callback( self.process_next() )
    #         # Process the next item in the queue and return
    #         # a list of result objects
    #         # Now we push it into the queue along with a future,
    #         # when the future
    #         # r = await j( self.queueHandler, resultsList, future )
    #         await self.queueHandler.enque( resultsList, future )
    #         return future
    #     except StopIteration as e:
    #         print( "%s users processed (not nec done)" % self.count_of_processed )
    #         return future.set_result(True)

    # loop = asyncio.get_event_loop()
    #
    # loop = asyncio.get_event_loop()
    # self.overall_future = asyncio.Future()
    # asyncio.ensure_future(self.process_next(future))
    # future.add_done_callback(got_result)
    # try:
    #     loop.run_forever()
    # finally:
    #     loop.close()

    # while True:
    #     try:
    #         await self.process_next()
    #         # loop.close()
    #         # create a future which will control when we
    #         # go on to the next item from the cursor
    #         # future = asyncio.Future()
    #         # future.add_done_callback( self.process_next  )
    #         # # Process the next item in the queue and return
    #         # # a list of result objects
    #         # resultsList = self.process_next()
    #         # # Now we push it into the queue along with a future,
    #         # # when the future
    #         # self.queueHandler.enque( resultsList, future )
    #
    #     except StopIteration as e:
    #         print( "%s users processed (not nec done)" % self.count_of_processed )
    #
    #         return self.count_of_processed


if __name__ == '__main__':
    pass
