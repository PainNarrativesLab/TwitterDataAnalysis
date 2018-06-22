"""
Created by adam on 5/11/18
"""


__author__ = 'adam'
import environment

from DataTools.DataStructures import make_tweet_result
from profiling import timestamped_count_writer
# from DataTools.Models.TweetORM import Users
from ProcessingTools.Processors import Parents


class Processor( Parents.IAsyncProcessor ):
    """Handles the text processing of the object"""

    def __init__( self ):
        super().__init__()

    def make_result( self, sentenceIndex: int, wordIndex: int, text: str, objId: int ):
        """Since the older version wants tweet ids, this is the default
        for all new uses to inherit.
        :param objId: The tweet or tweet's id
        :param text: The profile or tweet text
        :param wordIndex: The ordinal position of the word in the sentence
        :param sentenceIndex: The ordinal position of the sentence in the profile
      """
        # write the timestamp to file
        return make_tweet_result( sentenceIndex, wordIndex, text, objId )

    def process( self, tweet ):
        """Runs the string processing on a tweet's profile and
        returns a list of results.
        It does not enque the result for saving. Something else must do that
        :param tweet: DataTools.TweetORM.Users A single User object
        """
        if tweet.item_type() == 'tweet':
            text = str( tweet.tweetText )
            tweetId = tweet.tweetID
        else:
            print( type( tweet ) )
            raise ValueError

        if environment.INTEGRITY_LOGGING:
            timestamped_count_writer( environment.PROCESSING_ENQUE_LOG_FILE, tweetId, 'tweetid')

        # Split the profile into sentences
        sentences = self.sentence_tokenizer.process( text )

        results = [ ]
        # process sentences
        for sentenceIndex, sentence in enumerate( sentences ):
            results += self._processSentence( sentenceIndex, sentence, tweetId )

        return results


if __name__ == '__main__':
    pass