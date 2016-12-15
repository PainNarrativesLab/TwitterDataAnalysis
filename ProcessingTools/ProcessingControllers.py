"""
Created by adam on 11/6/16
"""
__author__ = 'adam'

from ConstantsAndUtilities import *
from DataTools.DataStructures import *
import DataTools.TweetORM

from QueueTools import *
from TextProcessors import Tokenizers



class TweetProcessingController( object ):
    """Handles processing of one tweet object at a time."""

    def __init__( self, SaveQueueHandler ):
        """
        SentenceTokenizer: Utility class with a process method which takes a tweet text and returns a list of sentences
        DbQueueHandler: Service class which puts the word in the queue to be saved, so that's not a bottleneck
        """
        self.sentence_tokenizer = Tokenizers.SentenceTokenizer()
        self.word_tokenizer = Tokenizers.WordTokenizer()
        self.QueueHandler = SaveQueueHandler
        self._word_processors = []

    def load_word_processor(self, processor):
        """Add something which acts on individual words to the stack that will run on each word from the tweet"""
        self._word_processors.append(processor)
        self._word_processors = list(set(self._word_processors))

    def _add_result_to_queue(self, result):
        """Enques the result"""
        assert(isinstance(result, Result))
        self.QueueHandler.enque( result )

    def make_and_enque_result( self, sentenceIndex, wordIndex, text, tweetId ):
        """Makes the result and hands it off to the queue handler"""
        if text is not None:
            result = make_result(sentenceIndex, wordIndex, text, tweetId )
            # print(result)
            self._add_result_to_queue(result)

    def process( self, tweets ):
        """Runs the string processing on a single tweet or list of tweets and enques the result for saving"""

        # wrap a single object in a list
        tweets = [tweets] if isinstance( tweets, DataTools.TweetORM.Tweet ) else tweets

        for tweet in tweets:
            # This way we can use either a list of strings or tweet objects
            if isinstance( tweet, DataTools.TweetORM.Tweet) or isinstance(tweet, DataTools.TweetORM.Tweets):
                text = str( tweet.tweetText )
                tweetId = tweet.tweetID
            else:
                raise ValueError

            # Split the tweet into sentences
            sentences = self.sentence_tokenizer.process( text )

            # process sentences
            [ self._processSentence( sentenceIndex, sentence, tweetId ) for sentenceIndex, sentence in enumerate( sentences ) ]

    def _run_word_processors(self, word):
        """Runs each processor in the stack on the string"""
        if len(self._word_processors) > 0:
            for wp in self._word_processors:
                word = wp.process(word)
        return word

    def _processSentence( self, sentenceIndex, sentence, tweetId ):
        # word tokenize
        [ self.make_and_enque_result( sentenceIndex, idx, self._run_word_processors( word ), tweetId ) for idx, word in enumerate( self.word_tokenizer.process( sentence ) ) ]
