"""
Created by adam on 11/6/16
"""
__author__ = 'adam'

from environment import *
from WordDAOs import *
from ConstantsAndUtilities import *
from DataStructures import *

# tt = "%s/WordBagMakers" % TEXT_TOOLS_PATH
# import TextTools.WordBagMakers

from TweetDAOs import *
from nltk.tokenize import word_tokenize, sent_tokenize


class IOperation:
    """Perform operations on the item and return the result"""

    def process( self, item ): return NotImplementedError


class ITokenizer:
    def process( self, item ): return NotImplementedError


class IQueueHandler:
    def enque( self ): return NotImplementedError


class SentenceTokenizer( ITokenizer ):
    def __init__( self ):
        super( ).__init__( )

    def process( self, item ):
        #         print('\n ----- sentence tokenizing ----- \n', item)
        return sent_tokenize( item )


class WordOperations( IOperation ):
    """Perform all operations that need to be performed on a single word"""

    def __init__( self ):
        super( ).__init__( )
        self.Operations = [ ]

    def load( self, callableOperation ):
        """Adds a callable operation to the queue"""
        self.Operations.append( callableOperation )

    def process( self, word ):
        # missing filter for punt
        return word.strip( )


# for operation in self.Operations:
#             word = operation(word)
#         return word

class WordOperationsTest:
    def __init__( self ):
        pass

    def test_load( self ):
        # function case
        pass

        # method case


class SaveQueueHandler( IQueueHandler ):
    def __init__( self ):
        super( ).__init__( )
        self.queue = [ ]

    def enque( self, item ):
        self.queue.append( item )


class TweetProcessor( object ):
    """Handles processing of one tweet object at a time."""

    def __init__( self, SentenceTokenizer, DbQueueHandler ):
        """SentenceTokenizer: Utility class with a process method which takes a tweet text and returns a list of sentences
        DbQueueHandler: Service class which puts the word in the queue to be saved, so that's not a bottleneck
        """
        self.Tokenizer = SentenceTokenizer
        self.QueueHandler = DbQueueHandler

    def boom( self, sentenceIndex, wordIndex, text, tweetId ):
        """Makes the result and hands it off to the queue handler"""
        result = Result( sentenceIndex, wordIndex, text, tweetId )
        self.QueueHandler.enque( result )

    def process( self, tweets ):
        """Runs the process on the entire set of tweets and returns the result"""

        for tweet in tweets:
            # This way we can use either a list of strings or tweet objects
            if type( tweet ) is Tweet or type( tweet ) is Tweets:
                text = str( tweet.tweetText )
                tweetId = tweet.tweetID
            else:
                if TEST is True:
                    # In development we can just give it a value
                    tweetId = TESTING_TWEET_ID
                    text = tweet
                else:
                    raise ValueError

            # Split the tweet into sentences
            sentences = self.Tokenizer.process( text )

        # process sentences
        [ self._processSentence( sentenceIndex, sentence, tweetId ) for sentenceIndex, sentence in
          enumerate( sentences ) ]

    def _processSentence( self, sentenceIndex, sentence, tweetId ):
        # word tokenize
        operations = WordOperations( )
        [ self.boom( sentenceIndex, idx, operations.process( word ), tweetId ) for idx, word in
          enumerate( word_tokenize( sentence ) ) ]


