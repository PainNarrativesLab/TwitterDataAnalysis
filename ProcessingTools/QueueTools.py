"""
Created by adam on 11/22/16
"""
__author__ = 'adam'

from queue import Queue

from DataTools.DataStructures import is_result
from ProcessingTools.Errors import NonResultEnqueued
from environment import *


# import Listeners
# from threading import Lock
# from collections import deque


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


class IQueueHandler( object ):
    """Objects which contain a queue and registered listeners"""

    def enque( self, result ):
        """Push the item onto the queue and call listeners"""
        return NotImplementedError

    def next( self ):
        """Return the next item in the queue, removing it from the queue"""
        return NotImplementedError


class SaveQueueHandler( IQueueHandler, ILockingQueue ):
    """
    This queue holds processed tokens ready to be saved.
    After a token is processed it gets pushed onto this queue. When
    that happens, the handler calls handle on all registered listeners
    and passes itself as the argument"""

    def __init__( self ):
        super().__init__()
        self.listeners = [ ]

    def enque( self, item ):
        """Push the item onto the queue and call listeners"""
        if PRINT_STEPS is True: print( "SaveQueueHandler.enque()" )
        self._push_onto_queue( item )
        self.notify_new_item_in_queue()

    def next( self ):
        """Return the next item in the queue, removing it from the queue"""
        # print("SaveQueueHandler.next()")
        return self._get_next_from_queue()

    def is_result_obj( self, obj ):
        if is_result( obj ):
            return True
        else:
            raise NonResultEnqueued

    def register_listener( self, listener ):
        """
        Add a new listener object to the list which will have their
        handle method called every time a new item is pushed onto the queue
        """
        if PRINT_STEPS is True: print( "SaveQueueHandler.register_listener()" )
        # check type
        # assert(isinstance(listener, Listeners.IListener))
        self.listeners.append( listener )

    def notify_new_item_in_queue( self ):
        """Call the handle methnd on each registered listener, passing
        the queueHandler as the argument"""
        if PRINT_STEPS is True: print( "SaveQueueHandler.notify_new_item_in_queue()" )
        [ l.handle( self ) for l in self.listeners ]
