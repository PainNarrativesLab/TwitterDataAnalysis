"""
Created by adam on 5/4/18
"""

__author__ = 'adam'

import asyncio

from ProcessingTools.Queues import AsyncQueues
from Servers.Mixins import ResponseStoreMixin
from ProcessingTools.Processors.UserProcessing import Processor


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

    async def _process( self, item, future ):
        """Calls the processor on the item and
        returns a list of results from the object.
        """
        # Process the item and return
        # a list of result objects
        resultsList = self.processor.process( item )
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

                # we're good to go. Processing item
                future = asyncio.Future()
                # get a user or tweet item
                item = self.cursor.next()
                self.count_of_processed += 1
                await self._process( item, future )

            except StopIteration as e:
                print( "%s item processed" % self.count_of_processed )
                # Some items may still be in the queue, thus
                # we need to send them all to the server
                # before we exit
                future = asyncio.Future()
                await self.queueHandler.flush_queue(future)
                return overall_future.set_result( True )


if __name__ == '__main__':
    pass
