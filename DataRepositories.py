"""
Created by adam on 11/6/16
"""
__author__ = 'adam'

from environment import *
from WordDAOs import *
from ConstantsAndUtilities import *
from DataStructures import *

# if type(Session) is not None:
#     # connect to db: Local object
#     session = Session( )


class IRepository( object ):
    def save( self, listOfResults ): raise NotImplementedError


class WordRepository( IRepository ):
    """Allows asynchronously updating the database with the items.
    todo If going to eventually use in multithreaded actions, there could be race conditions w/r/t creating and retrieving words
    """

    def __init__( self ):
        super( ).__init__( )

    def save( self, listOfResults ):
        for result in listOfResults:
            assert (type( result ) is Result)
            # get a Word object for the result
            word = self._get_word( result )
            # create a mapping object and attach word
            wordMap = self._get_map( result, word )
            if self._write_to_db( word, wordMap ) is True:
                # fire a save complete event
                self._fire_save_notification( wordMap )
            else:
                self._fire_error_saving_notification( wordMap )

    def _get_word( self, result ):
        """
        todo: make this work
        Look up whether word exists already
        If not, create a new entry and return the object
        Should not save yet so that the map can be flushed too
        """
        word = Word( )
        word.text = result.text if type( result ) is Result else result
        return word

    def _get_map( self, result, word ):
        """Creates a mapping object from the result"""
        assert (type( result ) is Result)
        assert (type( word ) is Word)
        wordMap = WordMapping( )
        wordMap.sentence_index = result.sentence_index
        wordMap.word_index = result.word_index
        # todo these should be objects loaded in
        wordMap.tweet_id = result.tweet_id
        wordMap.word_id = word.id  # update to use sqlalchemy relationship
        return wordMap

    def _fire_save_notification( self, wordMap ):
        print( "TODO: Replace this with an event firing" )

    def _fire_error_saving_notification( self, wordMap ):
        print( "TODO Replace this with an error event firing" )

    def _write_to_db( self, *args ):
        try:
            toSave = [ a for a in args ]
            print( toSave )
            # save them
            session.add_all( toSave )
            session.commit( )
            return True
        except Exception as e:
            print( e )
            return False

if __name__ == '__main__':
    pass