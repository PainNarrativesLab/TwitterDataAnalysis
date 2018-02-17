import sys
import unittest

from ConstantsAndUtilities import *

sys.path.append('%s/TextTools/TextProcessors' % BASE)  # the directory that contains my_pkg

from ProcessingControllers import *

from TestingTools.DataAndFunctionsForTesting import *

from ConstantsAndUtilities import *
from QueueTools import *


class TweetProcessorTests(unittest.TestCase):
    def setUp(self):
        self.queue = SaveQueueHandler()
        self.object = TweetProcessingController(self.queue)

    def test_make_and_enque_result(self):
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
        self.assertEqual(result.tweet_id, tweetId)


class FunctionalTestOfTweetProcessor(unittest.TestCase):
    def test_run_functional_test(self):
        processor = initialize_processor()

        numWords = 4
        numSent = 4
        numTweets = 4

        Queue = SaveQueueHandler()

        tweets = []
        results = []

        for i in range(0, numTweets):
            # make fake tweets
            tweets.append(makeTestTweetString())
            # make what we expect the processor to output
            results.append(makeExpectedResult(numWords, numSent, TESTING_TWEET_ID))

        tp = TweetProcessingController(Queue)
        tp.load_word_processor(processor)
        tp.process(tweets)

        for result in makeExpectedResult(4, 4, TESTING_TWEET_ID):
            try:
                assert (result in Queue.queue)
            except:
                print("error finding %s in %s" % result, Queue.queue)

                # print( "Processor : PASS \n Don't forget that you haven't fixed the '.' problem yet" )


if __name__ == '__main__':
    unittest.main()
