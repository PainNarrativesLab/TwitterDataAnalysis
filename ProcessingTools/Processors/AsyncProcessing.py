"""
Created by adam on 5/11/18
"""
from environment import PROCESSING_ENQUE_LOG_FILE

__author__ = 'adam'

import Processors
import Tokenizers
import DataTools
from DataTools import TweetORM
from DataTools.DataStructures import make_user_result
from profiling.OptimizingTools import timestamp_writer, timestamped_count_writer

import environment


class Processor( object ):
    """Handles the text processing of the object"""

    def __init__( self ):
        self.count_of_processed = 0
        self._word_processors = [ ]
        self.sentence_tokenizer = Tokenizers.SentenceTokenizer()
        self.word_tokenizer = Tokenizers.WordTokenizer()

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
        # write the timestamp to file
        return make_user_result( sentenceIndex, wordIndex, text, objId )

    def _processSentence( self, sentenceIndex: int, sentence: str, objId: int ):
        """
        Runs word tokenization (with whatever word processors are loaded)
        on the given sentence and then enques the results.
        :param objId: The user or tweet's id
        :param sentence: The sentence to process
        :param sentenceIndex: The ordinal position of the sentence in the text
        """
        r = [ self.make_result( sentenceIndex, idx, self._run_word_processors( word ), objId ) for idx, word in enumerate( self.word_tokenizer.process( sentence ) ) ]
        return [ a for a in r if a is not None]

    def process( self, user ):
        """Runs the string processing on a user's profile and
        returns a list of results.
        It does not enque the result for saving. Something else must do that
        :param user: DataTools.TweetORM.Users A single User object
        """
        if isinstance( user, DataTools.TweetORM.Users ):
            text = str( user.description )
            userId = user.userID
        else:
            print( type( user ) )
            raise ValueError

        if environment.INTEGRITY_LOGGING:
            timestamped_count_writer( environment.PROCESSING_ENQUE_LOG_FILE, userId, 'userid')

        # Split the profile into sentences
        sentences = self.sentence_tokenizer.process( text )

        results = [ ]
        # process sentences
        for sentenceIndex, sentence in enumerate( sentences ):
            results += self._processSentence( sentenceIndex, sentence, userId )

        return results


if __name__ == '__main__':
    pass