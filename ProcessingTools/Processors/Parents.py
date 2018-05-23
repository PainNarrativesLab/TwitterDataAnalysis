"""
Created by adam on 5/20/18
"""
import TextTools.Processors.Parents

__author__ = 'adam'

from TextProcessors import Tokenizers


class IAsyncProcessor( object ):
    """Handles the text processing of items like users and tweets"""

    def __init__( self ):
        self.count_of_processed = 0
        self._word_processors = [ ]
        self.sentence_tokenizer = Tokenizers.SentenceTokenizer()
        self.word_tokenizer = Tokenizers.WordTokenizer()

    def load_word_processor( self, processor: TextTools.Processors.Parents.IProcessor ):
        """
        Add something which acts on individual words
         to the stack that will run on each word from the tweet
         :type processor: TextTools.Processors.Parents.IProcessor
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

    def _processSentence( self, sentenceIndex: int, sentence: str, objId: int ):
        """
        Runs word tokenization (with whatever word processors are loaded)
        on the given sentence and then enques the results.
        :param objId: The user or tweet's id
        :param sentence: The sentence to process
        :param sentenceIndex: The ordinal position of the sentence in the text
        """
        r = [ self.make_result( sentenceIndex, idx, self._run_word_processors( word ), objId ) for idx, word in
              enumerate( self.word_tokenizer.process( sentence ) ) ]
        return [ a for a in r if a is not None ]

    def process( self, item ):
        raise NotImplementedError


if __name__ == '__main__':
    pass
