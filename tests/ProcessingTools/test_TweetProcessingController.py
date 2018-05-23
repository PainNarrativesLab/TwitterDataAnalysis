import unittest

from ConstantsAndUtilities import *

sys.path.append('%s/TextTools/TextProcessors' % BASE)  # the directory that contains my_pkg

from deprecated.ProcessingControllers import *

from TestingTools.DataAndFunctionsForTesting import *
from TestingTools.Factories import *


class TweetProcessorUnitTests(unittest.TestCase):
    def setUp(self):
        self.queue = DummyQueueFactory()
        self.object = TweetProcessingController(self.queue)

    def test_make_and_enque_result(self):
        """Still need to test instance because each subclass uses different make_result"""
        sentenceIndex = 3
        wordIndex = 2
        text = 'taco'
        tweetId = 123456789
        self.object.make_and_enque_result(sentenceIndex, wordIndex, text, tweetId)

        result = self.queue.queue[0]
        self.assertIsInstance(result, Result)
        self.assertEqual(result.sentence_index, sentenceIndex)
        self.assertEqual(result.word_index, wordIndex)
        self.assertEqual(result.text, text)
        self.assertEqual(result.id, tweetId)
        self.assertEqual(result.type, 'tweet', "Result is correct type")

    def test_processSentence(self):
        sentenceIndex = 2
        userId = 123456789
        text = "Tacoes are nom. They should be eaten!"

        # call
        self.object._processSentence(sentenceIndex, text, userId)

        expect = [
            Result(sentence_index=2, word_index=0, text='Tacoes', id=123456789, type='tweet'),
            Result(sentence_index=2, word_index=1, text='are', id=123456789, type='tweet'),
            Result(sentence_index=2, word_index=2, text='nom', id=123456789, type='tweet'),
            Result(sentence_index=2, word_index=3, text='.', id=123456789, type='tweet'),
            Result(sentence_index=2, word_index=4, text='They', id=123456789, type='tweet'),
            Result(sentence_index=2, word_index=5, text='should', id=123456789, type='tweet'),
            Result(sentence_index=2, word_index=6, text='be', id=123456789, type='tweet'),
            Result(sentence_index=2, word_index=7, text='eaten', id=123456789, type='tweet'),
            Result(sentence_index=2, word_index=8, text='!', id=123456789, type='tweet')
        ]

        self.assertEqual(len(self.queue.queue), len(expect), "Queue contains the right amount of objects")
        self.assertEqual(expect, self.queue.queue)


class TweetProcessorFunctionalTests(unittest.TestCase):
    def setUp(self):
        self.numTweets = 4
        self.queue = DummyQueueFactory()
        self.object = TweetProcessingController(self.queue)
        self.tweets = [TweetFactory() for i in range(0, self.numTweets)]

    def test_process_tweet_obj_input(self):
        # self.object.load_word_processor(processor)
        self.object.process(self.tweets)
        self.assertTrue(len(self.queue.queue) > 0)


if __name__ == '__main__':
    unittest.main()
