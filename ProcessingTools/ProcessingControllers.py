"""
Each of these tools handles manages the process of
taking a stored tweet or user object and storing its constituent words
(from content and description, respectively) in the
 database.

 Each can apply various filters and transformations.
 These do not directy saving results. That is the
  job of the que handler

Created by adam on 11/6/16
"""
__author__ = 'adam'

import DataTools.TweetORM
import environment
from DataTools.DataStructures import make_tweet_result, make_user_result
from ProcessingTools.QueueTools import IQueueHandler
from Servers.Mixins import ResponseStoreMixin
from TextProcessors import Tokenizers, Processors
# instrumenting to determine if running async
from profiling.OptimizingTools import timestamp_writer

log_file = "%s/processing-enque.csv" % environment.LOG_FOLDER_PATH


def response_complete( responses, response ):
    if response in responses:
        responses.remove( response )


class IProcessingController( ResponseStoreMixin ):

    def __init__( self, saveQueueHandler: IQueueHandler ):
        """
        :type saveQueueHandler: Service class which puts the word in the queue to be saved, so that's not a bottleneck
        """
        self.count_of_processed = 0
        self.sentence_tokenizer = Tokenizers.SentenceTokenizer()
        self.word_tokenizer = Tokenizers.WordTokenizer()
        self.QueueHandler = saveQueueHandler
        self._word_processors = [ ]
        super().__init__()

    def load_word_processor( self, processor: Processors.IProcessor ):
        """
        Add something which acts on individual words
         to the stack that will run on each word from the tweet
         :type processor: Processors.IProcessor
         """
        self._word_processors.append( processor )
        self._word_processors = list( set( self._word_processors ) )

    def _run_word_processors( self, word: str ):
        """Runs each processor in the stack on the string"""
        if len( self._word_processors ) > 0:
            for wp in self._word_processors:
                word = wp.process( word )
        return word

    def make_result( self, sentenceIndex: int, wordIndex: int, text: str, objId: int ):
        """Since the older version wants tweet ids, this is the default
        for all new uses to inherit.
        :param objId: The user or tweet's id
        :param text: The profile or tweet text
        :param wordIndex: The ordinal position of the word in the sentence
        :param sentenceIndex: The ordinal position of the sentence in the profile
      """
        raise NotImplementedError

    def make_and_enque_result( self, sentenceIndex: int, wordIndex: int, text: str, objId: int ):
        """Makes the result and hands it off to the queue handler
        :param objId: The user or tweet's id
        :param text: The profile or tweet text
        :param wordIndex: The ordinal position of the word in the sentence
        :param sentenceIndex: The ordinal position of the sentence in the profile
        """
        if text is not None:
            result = self.make_result( sentenceIndex, wordIndex, text, objId )
            # write the timestamp to file
            timestamp_writer( log_file )

            response = self.QueueHandler.enque( result )
            # self.add_response(response)

            # response.add_done_callback(response_complete(self.responses, response))
            # response.add_done_callback(self.prune_responses)
            # response.add_done_callback(lambda x : self.remove_response(response))
            # if type(response) is not None:
            #     self.responses.append( response )

    #
    # def prune_responses( self ):
    #     print( 'pruning: %s responses' % len( self.responses ) )
    #     self.responses = [ self.responses.remove( r ) for r in self.responses if r is not None and r.done() ]
    #     print( 'pruning complete: %s responses' % len( self.responses ) )

    def _processSentence( self, sentenceIndex: int, sentence: str, objId: int ):
        """
        Runs word tokenization (with whatever word processors are loaded)
        on the given sentence and then enques the results.
        :param objId: The user or tweet's id
        :param sentence: The sentence to process
        :param sentenceIndex: The ordinal position of the sentence in the text
        """
        [ self.make_and_enque_result( sentenceIndex, idx, self._run_word_processors( word ), objId ) for idx, word in
          enumerate( self.word_tokenizer.process( sentence ) ) ]

    def set_notice_logger( self, logger ):
        self.notice_logger = logger

    def set_error_logger( self, logger ):
        self.error_logger = logger

    def log_event( self, message ):
        try:
            self.notice_logger.log( message )
        except:
            print( message )


class TweetProcessingController( IProcessingController ):
    """Handles processing of one tweet object at a time."""

    def __init__( self, saveQueueHandler: IQueueHandler ):
        """
        :type saveQueueHandler: Service class which puts the word in the queue to be saved, so that's not a bottleneck
        """
        super().__init__( saveQueueHandler )

    def make_result( self, sentenceIndex: int, wordIndex: int, text: str, objId: int ):
        """Overwrites parent so that used old version for tweet id having Result"""
        return make_tweet_result( sentenceIndex, wordIndex, text, objId )

    def process( self, tweets: list ):
        """Runs the string processing on a single tweet or list of tweets and enques the result for saving"""

        # wrap a single object in a list
        tweets = [ tweets ] if isinstance( tweets, DataTools.TweetORM.Tweet ) else tweets

        for tweet in tweets:
            # This way we can use either a list of strings or tweet objects
            if isinstance( tweet, DataTools.TweetORM.Tweet ) or isinstance( tweet, DataTools.TweetORM.Tweets ):
                text = str( tweet.tweetText )
                tweetId = tweet.tweetID
            else:
                raise ValueError( "Non tweet object passed to processor" )

            # Split the tweet into sentences
            sentences = self.sentence_tokenizer.process( text )

            # process sentences
            [ self._processSentence( sentenceIndex, sentence, tweetId ) for sentenceIndex, sentence in
              enumerate( sentences ) ]

    # def _processSentence(self, sentenceIndex, sentence, tweetId):
    #     # word tokenize
    #     [self.make_and_enque_result(sentenceIndex, idx, self._run_word_processors(word), tweetId) for idx, word in
    #      enumerate(self.word_tokenizer.process(sentence))]


class UserProcessingController( IProcessingController ):
    """Handles processing of one user at a time."""

    def __init__( self, saveQueueHandler: IQueueHandler ):
        """
        :type saveQueueHandler: Service class which puts the word in the queue to be saved, so that's not a bottleneck
        """
        super().__init__( saveQueueHandler )

    def make_result( self, sentenceIndex: int, wordIndex: int, text: str, objId: int ):
        return make_user_result( sentenceIndex, wordIndex, text, objId )

    def process( self, users: list ):
        """Runs the string processing on a user's profile and
        enques the result for saving
        :param users: list of DataTools.TweetORM.Users or single User
        """
        # wrap a single object in a list
        users = [ users ] if isinstance( users, DataTools.TweetORM.Users ) else users
        for user in users:
            if isinstance( user, DataTools.TweetORM.Users ):
                text = str( user.description )
                userId = user.userID
            else:
                print( type( user ) )
                raise ValueError

            # Split the profile into sentences
            sentences = self.sentence_tokenizer.process( text )

            # process sentences
            [ self._processSentence( sentenceIndex, sentence, userId ) for sentenceIndex, sentence in
              enumerate( sentences ) ]

            self.count_of_processed += 1

        # self.log_event("Processed %s users" % self.count_of_processed)
