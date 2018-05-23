"""
Created by adam on 5/11/18
"""

__author__ = 'adam'
import environment

from DataTools.DataStructures import make_user_result
from profiling.OptimizingTools import timestamped_count_writer
from DataTools.Models import TweetORM
# from DataTools.Models.TweetORM import Users
from ProcessingTools.Processors import Parents


class Processor( Parents.IAsyncProcessor ):
    """Handles the text processing of the object"""

    def __init__( self ):
        super().__init__()

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

    def process( self, user ):
        """Runs the string processing on a user's profile and
        returns a list of results.
        It does not enque the result for saving. Something else must do that
        :param user: DataTools.TweetORM.Users A single User object
        """
        if user.item_type() == 'user':
            # if isinstance( user, Users ):
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