"""
Created by adam on 5/7/18
"""
__author__ = 'adam'
import asyncio
import unittest
from unittest import TestCase
from unittest.mock import Mock

import aiounittest

from ProcessingTools.Controllers import AsyncControl
from ProcessingTools.Queues import AsyncQueues
from ProcessingTools.Queues import DummyQueues
from TestingTools import DummyCursors, Factories


async def add( x, y ):
    await asyncio.sleep( 0.1 )
    return x + y


class DummyProcessor( object ):
    def process( self, item ):
        return item


class TestAsyncControlSynchronousParts( TestCase ):
    def setUp( self ):
        self.qh = DummyQueues.DummyAsyncQueueHandler()
        self.obj = AsyncControl.Control( self.qh )

    def test_is_over_limit( self ):
        self.obj.limit = 10
        self.obj.count_of_processed = 2
        self.assertFalse( self.obj.is_over_limit )

    def test_is_over_limit_true( self ):
        self.obj.limit = 10
        self.obj.count_of_processed = 12

        def c():
            return self.obj.is_over_limit

        self.assertRaises( StopIteration, c )


class TestAsyncControlAsynchronousParts( aiounittest.AsyncTestCase ):
    def setUp( self ):
        self.cursor = DummyCursors.DummyUserCursor()
        self.processor = Mock()
        self.queueHandler = DummyQueues.DummyAsyncQueueHandler()
        # self.queueHandler = Mock(wraps=AsyncQueues.AsyncServerQueueDropin)
        self.obj = AsyncControl.Control( queueHandler=self.queueHandler, processor=self.processor )

    async def test__process( self ):
        # prep
        resultsList = [ Factories.UserResultFactory() for _ in range( 0, 3 ) ]
        self.processor.process = Mock( return_value=resultsList )
        f = asyncio.Future()
        # call
        await self.obj._process(self.cursor.next(), f)
        # check
        self.obj.processor.process.assert_called()
        self.assertEqual(1, self.obj.processor.process.call_count, "Process called expected #")
        self.assertEqual(1, self.queueHandler.call_count, "Enqueue called expected #")

    async def test_process_from_cursor( self ):
        limit = 4
        # call
        r = await self.obj.process_from_cursor( self.cursor, limit )
        # check
        self.assertEqual( limit, self.obj.count_of_processed )
        self.obj.processor.process.assert_called()
        self.assertEqual(limit, self.obj.processor.process.call_count, "Process called expected #")
        self.assertEqual(limit, self.queueHandler.call_count, "Enqueue called expected #")

#
# #
# async def do_thing( i ):
#     print( "do thing %s ..." % (i) )
#     f = asyncio.future()
#     await enqueue( i, f )
#     # asyncio.sleep( 1.0 )
#     return f
#
#
# async def enqueue( item, future ):
#     print( "enqueue %s ..." % (item) )
#     await asyncio.sleep( 1.0 )
#     return future.set_result()
#
#
# async def controller( cursor, limit=4 ):
#     for _ in range( 0, limit ):
#         i = next( cursor )
#         result = await do_thing( i )
#         print( "controller %s " % (result) )
#
#
# def cursor():
#     i = 0
#     while True:
#         print( "cursor %s" % i )
#         yield i
#         i += 1
#
#
# class TestJiip( aiounittest.AsyncTestCase ):
#     def setUp( self ):
#         pass
#
#     async def test_jip( self ):
#         c = cursor()
#         limit = 4
#         await controller( c )
#

if __name__ == '__main__':
    unittest.main()
