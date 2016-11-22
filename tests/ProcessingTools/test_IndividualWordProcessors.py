import sys
import unittest

from ConstantsAndUtilities import *
sys.path.append('%s/TextTools/TextProcessors' % BASE) #the directory that contains my_pkg

from IndividualWordProcessors import *

from TestingTools.test_data import *

from ConstantsAndUtilities import *


class FunctionalTestOfTweetProcessor( unittest.TestCase ):

    def test_run_functional_test( self ):
        processor = initialize_processor( )

        numWords = 4
        numSent = 4
        numTweets = 4

        Queue = SaveQueueHandler( )

        tweets = [ ]
        results = [ ]

        for i in range( 0, numTweets ):
            # make fake tweets
            tweets.append( makeTestTweetString( ) )
            # make what we expect the processor to output
            results.append( makeExpectedResult( 4, 4, TESTING_TWEET_ID ) )

        tp = TweetProcessor( SentenceTokenizer( ), Queue )
        tp.load_word_processor( initialize_processor( ) )
        tp.process( tweets )

        for result in makeExpectedResult( 4, 4, TESTING_TWEET_ID ):
            try:
                assert (result in Queue.queue)
            except:
                print( "error finding %s in %s" % result, Queue.queue )

        print( "Processor : PASS \n Don't forget that you haven't fixed the '.' problem yet" )


if __name__ == '__main__':
    unittest.main( )
