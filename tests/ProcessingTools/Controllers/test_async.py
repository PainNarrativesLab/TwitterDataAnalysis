"""
Created by adam on 5/7/18
"""
__author__ = 'adam'
import unittest
from unittest import TestCase


import asyncio

import aiounittest


async def add( x, y ):
    await asyncio.sleep( 0.1 )
    return x + y


class MyTest( aiounittest.AsyncTestCase ):

    async def test_async_add( self ):
        ret = await add( 5, 6 )
        self.assertEqual( ret, 11 )


async def do_thing( i ):
    print( "do thing %s ..." % (i) )
    f = asyncio.Future()
    await enqueue(i, f)
    return f

async def enqueue(item, future):
    print( "enqueue %s ..." % (item) )
    await asyncio.sleep( 1.0 )
    return future.set_result(True)

async def controller(cursor, limit=4):
    cnt = 0
    while True:
        try:
            cnt += 1
            check(cnt, limit)
        # for _ in range(0, limit):
            i = next(cursor)
            result = await do_thing( i )
            print( "controller %s " % (result) )
        except StopIteration:
            break
    return cnt


def check(cnt, limit):
    if cnt >= limit:
        raise StopIteration

def cursor():
    i = 0
    while True:
        print("cursor %s" % i)
        yield i
        i+= 1

class TestJiip( aiounittest.AsyncTestCase ):
    def setUp( self ):
        pass

    async def test_jip( self ):
        c = cursor()
        limit = 4
        r = await controller(c, limit)
        self.assertEqual(r, limit)


if __name__ == '__main__':
    unittest.main()
