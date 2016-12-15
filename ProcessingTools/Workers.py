"""
Created by adam on 11/23/16
"""
__author__ = 'adam'

from environment import *
import ProcessingControllers

class IWorker(object):
    """Base for workers which carry out a specified task, sometimes in their own
    processes or threads"""
    @classmethod
    def run(cls, item): raise NotImplementedError


class SaveWorker(IWorker):
    """Handles saving items from a queue using a repository"""

    @classmethod
    def _initialize_repository(cls, repository):
        """Loads one copy of the data repository for all instances to use"""
        cls.repository = repository

    @classmethod
    def run(cls, item):
        if PRINT_STEPS is True: print("SaveWorker.run()")
        cls.repository.save(item)


class LogWorker( IWorker ):

    @classmethod
    def run( cls, item ):
        """Log the result"""
        print("TODO add logging")


class StringProcessingWorker(IWorker):
    def __init__(self):
    # def __init__(self, cursor, queue, word_processor):
        super().__init__()
        self.totalProcessed = 0
        # StringProcessingWorker.initialize(cursor, queue, word_processor)

    @classmethod
    def initialize(cls, cursor, queue, word_processor):
        cls.cursor = cursor
        # cls.queue = queue
        cls.processor = ProcessingControllers.TweetProcessingController(queue)
        cls.processor.load_word_processor(word_processor)

    @classmethod
    def run(cls, item):
        if PRINT_STEPS is True: print("StringProcessingWorker.run()")
        return cls.processor.process(item)


    def do_it(self):
        keepGoing = True

        while keepGoing:
            try:
                # Get a tweet from the stack
                tweet = self.cursor.next_tweet( )

                #Run the string processing tasks on it
                # Push the result into the queue
                StringProcessingWorker.run(tweet)

                self.totalProcessed += 1

            except Exception as e:
                print( e )
                keepGoing = False

    def do_it_dawg(self):
        """Same as do it, just calls a method on the to use a dawg datastructure"""
        keepGoing = True

        while keepGoing:
            try:
                # Get a tweet from the stack
                tweet = self.cursor.next_tweet( )

                #Run the string processing tasks on it
                # Push the result into the queue
                StringProcessingWorker.run(tweet)

                self.totalProcessed += 1

            except Exception as e:
                print( e )
                keepGoing = False


