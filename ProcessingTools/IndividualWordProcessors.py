"""
Created by adam on 11/6/16
"""
__author__ = 'adam'

from nltk.tokenize import word_tokenize, sent_tokenize

from ConstantsAndUtilities import *
from DataTools.DataStructures import *
from DataTools.TweetORM import *


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
        self._word_processors = []

    def load_word_processor(self, processor):
        """Add something which acts on individual words to the stack that will run on each word from the tweet"""
        self._word_processors.append(processor)
        self._word_processors = list(set(self._word_processors))

    def boom( self, sentenceIndex, wordIndex, text, tweetId ):
        """Makes the result and hands it off to the queue handler"""
        if text is not None:
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

    def _run_word_processors(self, word):
        """Runs each processor in the stack on the string"""
        if len(self._word_processors) > 0:
            for wp in self._word_processors:
                word = wp.process(word)
        return word

    def _processSentence( self, sentenceIndex, sentence, tweetId ):
        # word tokenize
        [ self.boom( sentenceIndex, idx, self._run_word_processors(word ), tweetId ) for idx, word in
          enumerate( word_tokenize( sentence ) ) ]


