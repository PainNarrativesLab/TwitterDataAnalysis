"""
Created by adam on 5/7/18
"""
__author__ = 'adam'
import asyncio
import unittest
from unittest.mock import MagicMock

import aiounittest

from ProcessingTools.Queues import AsyncQueues


def cursor():
    i = 0
    while True:
        # print( "cursor %s" % i )
        yield i
        i += 1


class DummyClient( object ):
    def __init__( self ):
        self.send = MagicMock()


class TestAsyncQueue( aiounittest.AsyncTestCase ):
    def setUp( self ):
        self.obj = AsyncQueues.AsyncServerQueueDropin()
        client = DummyClient()
        # client.send = MagicMock()
        self.obj.client = client

    async def test_enqueue_less_than_batch( self ):
        length = 5
        resultList = [ i for i in range( 0, length ) ]
        future = asyncio.Future()
        # call
        r = await self.obj.enque( resultList, future )
        # check
        self.assertTrue( r.result )
        self.assertEqual( length, len( self.obj.store ) )
        self.assertEqual( 0, self.obj.client.send.call_count )

    async def test_enqueueGreaterThanBatch( self ):
        length = 15
        expectedRemainder = length - self.obj.batch_size
        resultList = [ i for i in range( 0, length ) ]
        future = asyncio.Future()

        # call
        r = await self.obj.enque( resultList, future )

        # check
        self.assertTrue( r.result )
        self.assertEqual( expectedRemainder, len( self.obj.store ) )
        self.obj.client.send.assert_called()
        self.assertEqual( 1, self.obj.client.send.call_count, "Send called the expected # times" )

    async def test_handleSend( self ):
        length = 15
        expectedRemainder = length - self.obj.batch_size
        resultList = [ i for i in range( 0, length ) ]
        self.obj.store = resultList
        future = asyncio.Future()

        # call
        r = await self.obj.handle_send( future )

        # check
        self.assertTrue( r.result )
        self.assertEqual( expectedRemainder, len( self.obj.store ) )
        self.obj.client.send.assert_called()
        self.assertEqual( 1, self.obj.client.send.call_count, "Send called the expected # times" )


#
# async def do_thing( i ):
#     print( "do thing %s ..." % (i) )
#     f = asyncio.Future()
#     await enqueue(i, f)
#     # asyncio.sleep( 1.0 )
#     return f
#
# async def enqueue(item, future):
#     print( "enqueue %s ..." % (item) )
#     await asyncio.sleep( 1.0 )
#     return future.set_result()
#
# async def controller(cursor, limit=4):
#     for _ in range(0, limit):
#         i = next(cursor)
#         result = await do_thing( i )
#         print( "controller %s " % (result) )
#
# class TestJiip( aiounittest.AsyncTestCase ):
#     def setUp( self ):
#         pass
#
#     async def test_jip( self ):
#         c = cursor()
#         limit = 4
#         await controller(c)


if __name__ == '__main__':
    unittest.main()
