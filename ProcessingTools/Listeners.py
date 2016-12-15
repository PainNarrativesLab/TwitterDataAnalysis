"""
This contains the objects which control the processing of twets
This is where all the observers and listeners are
Created by adam on 11/7/16
"""
__author__ = 'adam'

import QueueTools
import DataTools.DataRepositories

from Workers import *
from environment import *

class IListener(object):
    def handle(self, handler): raise NotImplementedError


class SaveListener(IListener):
    """Listens for a result to be ready for saving and then dispatches
    a save processor to handle it
    """

    def __init__(self):
        SaveWorker._initialize_repository( DataTools.DataRepositories.WordRepository( ) )

    def handle(self, queue):
        if PRINT_STEPS is True: print("SaveListener.handle called")
        assert(isinstance(queue, QueueTools.IQueueHandler))

        # pull a result off the queue
        result = queue.next()

        # save it
        SaveWorker.run(result)


class LogListener(IListener):

    def __init__(self):
        SaveWorker._initialize_repository( DataTools.DataRepositories.WordRepository( ) )

    def handle(self, handler):
        if PRINT_STEPS is True: print("SaveListener.handle called")
        assert(isinstance(handler, QueueTools.IQueueHandler))
        # pull a result off the queue
        result = handler.next()

        # save it
        LogWorker.run(result)
