import unittest

from deprecated.ProcessingControllers import *
from TestingTools.DataAndFunctionsForTesting import *
from TestingTools.Factories import *

sys.path.append('%s/TextTools/TextProcessors' % BASE)  # the directory that contains my_pkg


class UserProcessorUnitTests(unittest.TestCase):
    def setUp(self):
        self.queue = DummyQueueFactory()
        self.object = UserProcessingController(self.queue)
        self.user = UserFactory()

    def test_make_and_enque_result(self):
        """Still need to test instance because each subclass uses different make_result"""
        sentenceIndex = 3
        wordIndex = 2
        text = 'taco'
        id = 123456789
        self.object.make_and_enque_result(sentenceIndex, wordIndex, text, id)

        result = self.queue.queue[0]
        self.assertIsInstance(result, Result)
        self.assertEqual(result.sentence_index, sentenceIndex)
        self.assertEqual(result.word_index, wordIndex)
        self.assertEqual(result.text, text)
        self.assertEqual(result.id, id)
        self.assertEqual(result.type, 'user', "Result is correct type")

    def test_processSentence(self):
        sentenceIndex = 2
        userId = 123456789
        text = "Tacoes are nom. They should be eaten!"

        # call
        self.object._processSentence(sentenceIndex, text, userId)

        expect = [
            Result(sentence_index=2, word_index=0, text='Tacoes', id=123456789, type='user'),
            Result(sentence_index=2, word_index=1, text='are', id=123456789, type='user'),
            Result(sentence_index=2, word_index=2, text='nom', id=123456789, type='user'),
            Result(sentence_index=2, word_index=3, text='.', id=123456789, type='user'),
            Result(sentence_index=2, word_index=4, text='They', id=123456789, type='user'),
            Result(sentence_index=2, word_index=5, text='should', id=123456789, type='user'),
            Result(sentence_index=2, word_index=6, text='be', id=123456789, type='user'),
            Result(sentence_index=2, word_index=7, text='eaten', id=123456789, type='user'),
            Result(sentence_index=2, word_index=8, text='!', id=123456789, type='user')
        ]

        self.assertEqual(len(self.queue.queue), len(expect), "Queue contains the right amount of objects")
        self.assertEqual(expect, self.queue.queue)


class UserProcessorFunctionalTests(unittest.TestCase):
    def setUp(self):
        self.numUsers = 4
        self.queue = DummyQueueFactory()
        self.object = UserProcessingController(self.queue)
        self.Users = [UserFactory() for i in range(0, self.numUsers)]

    def test_process_User_obj_input(self):
        self.object.process(self.Users)
        self.assertTrue(len(self.queue.queue) > 0)


if __name__ == '__main__':
    unittest.main()
