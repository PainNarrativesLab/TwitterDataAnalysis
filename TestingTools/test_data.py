"""
Created by adam on 11/6/16
"""
__author__ = 'adam'
from environment import *
from DataStructures import *
# Testing tools

import random
from faker import Faker

fake = Faker()


def makeTestTweetString( numWords=4, numSent=4 ):
    text = ''
    for s in range( 0, numSent ):
        for w in range( 0, numWords ):
            text += " s%sw%s" % (s, w)
        text += '. '
    return text.strip( )


def makeExpectedResult( numWords=4, numSent=4, tweetId=None ):
    results = [ ]
    for s in range( 0, numSent ):
        for w in range( 0, numWords ):
            text = "s%sw%s" % (s, w)

            tweetid = tweetId if tweetId != None else TESTING_TWEET_ID
            # len( results ) * 10 + (s + w)
            results.append( Result( s, w, text, tweetid ) )

    return results


def makeTestResult( sentenceIndex=None, wordIndex=None, text=None, tweetId=None ):
    """Makes a single Result with random values"""
    sentenceIndex = sentenceIndex if sentenceIndex is not None else random.randint( 1, 99999 )
    wordIndex = wordIndex if wordIndex is not None else random.randint( 1, 99999 )
    text = text if text is not None else fake.word( )
    tweetId = tweetId if tweetId is not None else random.randint( 1, 99999 )
    return Result( sentenceIndex, wordIndex, text, tweetId )


def functionalTestOfProcessor( numWords=4, numSent=4, numTweets=4 ):
    tweets = [ ]
    results = [ ]

    for i in range( 0, numTweets ):
        # make fake tweets
        tweets.append( makeTestTweetString( ) )
        # make what we expect the processor to output
        results.append( makeExpectedResult( 4, 4, TESTING_TWEET_ID ) )

