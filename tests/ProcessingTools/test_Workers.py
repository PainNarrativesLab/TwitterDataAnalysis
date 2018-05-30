import unittest

import Queues.Interfaces
from deprecated.Workers import *
import TweetORM
from DataTools import Cursors
from threading import Thread


class StringProcessingWorkerTest(unittest.TestCase):
    def setUp(self):
        self.obj = StringProcessingWorker()

    # @patch( 'QueueTools.IQueueHandler' )
    def test_intializing_for_class_makes_available_to_instances(self):
        queue = Queues.Interfaces.IQueueHandler()
        self.obj.initialize('cursor', queue, 'processor')
        # create a new instance
        obj = StringProcessingWorker()
        # check whether has expected properties
        self.assertEqual(obj.cursor, 'cursor', 'cursor available to child')
        self.assertTrue( type(obj.processor) == ProcessingControllers.TweetProcessingController,
                        'processor available to child' )
    @unittest.skip
    def test_cursor_behaves_as_expected(self):
        cursor = Cursors.TweetCursor()
        queue = Queues.Interfaces.IQueueHandler()
        self.obj.initialize(cursor, queue, 'processor')
        r1 = self.obj.cursor.next_tweet()
        self.assertIsInstance( r1, TweetORM.Tweet )

        # create a new instance
        obj = StringProcessingWorker()
        r2 = obj.cursor.next_tweet()
        self.assertIsInstance( r2, TweetORM.Tweet )
        self.assertNotEqual(r1, r2, 'calls to different instances return different results. The generator is advancing')

    @unittest.skip
    def test_threaded_cursor_behaves_as_expected(self):
        # Load cursor for tweet ids
        threads = []
        cursor = Cursors.TweetCursor()
        queue = Queues.Interfaces.IQueueHandler()
        self.obj.initialize(cursor, queue, 'processor')
        r1 = []
        r2 = []

        def t1():
            print('t1')
            obj = StringProcessingWorker()
            r = obj.cursor.next()
            r1.append(r)
            # self.assertIsInstance( r, TweetORM.Tweet )

        def t2():
            print('t2')
            obj = StringProcessingWorker()
            r = obj.cursor.next()
            r2.append(r)

        for i in range(0, 10):
            if (i % 2 == 0):  # even
                thread = Thread(target=t1)
            else:
                thread = Thread(target=t2)
            thread.start()
            threads.append(thread)

        for t in threads:
            t.join()

        self.assertTrue(len(r1) > 1)
        self.assertTrue(len(r2) > 1)
        [ self.assertIsInstance( r, TweetORM.Tweet ) for r in r1 ]
        [ self.assertIsInstance( r, TweetORM.Tweet ) for r in r2 ]
        # self.assertNotEqual( r1, r2, 'calls to different instances return different results. The generator is advancing' )


if __name__ == '__main__':
    unittest.main()
