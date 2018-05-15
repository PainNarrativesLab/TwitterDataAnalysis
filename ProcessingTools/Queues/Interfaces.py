"""
Created by adam on 5/4/18
"""
from queue import Queue

__author__ = 'adam'


class IQueueHandler( object ):
    """Objects which contain a queue and registered listeners"""

    def enque( self, result ):
        """Push the item onto the queue and call listeners"""
        return NotImplementedError

    def next( self ):
        """Return the next item in the queue, removing it from the queue"""
        return NotImplementedError


class ILockingQueue( object ):
    """
    Uses a mutex lock to prevent the queue from being simultaneously
    accessed from multiple threads, as well as other features to handle
    problems with multi-thread access
    """

    def __init__( self ):
        self.queue = Queue()

    def _push_onto_queue( self, item ):
        self.queue.put( item )

    def _get_next_from_queue( self ):
        return self.queue.get()


if __name__ == '__main__':
    pass
