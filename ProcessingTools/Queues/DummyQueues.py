"""
Used for testing or development

Created by adam on 5/7/18
"""
from Queues.Interfaces import IQueueHandler, ILockingQueue

__author__ = 'adam'


class DummySaveQueueHandler( IQueueHandler, ILockingQueue ):
    def __init__( self ):
        self.queue = [ ]

    def enque( self, result ):
        self.queue.append( result )

    def next( self ):
        return self.queue.pop()



class DummyAsyncQueueHandler( IQueueHandler, ILockingQueue ):
    def __init__( self ):
        self.queue = [ ]
        self.call_count = 0

    async def enque( self, result, future ):
        self.call_count += 1
        self.queue.append( result )
        return future.set_result(True)

    def next( self ):
        return self.queue.pop()



if __name__ == '__main__':
    pass
