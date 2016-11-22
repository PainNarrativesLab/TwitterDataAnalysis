"""
Created by adam on 11/6/16
"""
__author__ = 'adam'

from DataTools.DataStructures import *
from DataTools.WordORM import *

if type(Session) is not None:
    # connect to db
    engine = DataConnections.initialize_engine( )
    # DataTools's handle to database at global level
    Session = sessionmaker( bind=engine )
    # connect to db: Local object
    session = Session( )


class IRepository( object ):
    def save( self, listOfResults ): raise NotImplementedError

class ISessionHaver(object):
    """Common class for objects which have access to the sqalchemy session.
    Loads and initalizes on object construction. """
    def __init__(self):
        self.start_session()

    def start_session(self):
        """Loads the sqlalchemy Session object in as self.session"""
        if Session:
            self.session = session


class WordRepository( IRepository, ISessionHaver ):
    """Allows asynchronously updating the database with the items.
    todo If going to eventually use in multithreaded actions, there could be race conditions w/r/t creating and retrieving words
    """

    def __init__( self ):
        super( ).__init__( )


    def get_word( self, result ):
        """
        Look up whether word exists already
        If not, create a new entry and return the object
        Should not save yet so that the map can be flushed too
        """
        text = result.text if type( result ) is Result else result

        # Get if already exists
        word = self.session.query( Word ).filter( Word.word == text ).first( )

        # Handle word not found case
        if not isinstance( word, Word ):
            word = Word( )
            word.word = text

        return word

    def get_map( self, result, word ):
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

    def save( self, listOfResults ):
        """
        For each word contained in the list, this retreiveds the object if it already exists or
        creates a new word object. It then writes the word and mapping to the db before firing
        various notifications
        """
        for result in listOfResults:
            assert (type( result ) is Result)
            # get a Word object for the result
            word = self.get_word( result )
            # create a mapping object and attach word
            wordMap = self.get_map( result, word )
            if self.write_to_db( word, wordMap ) is True:
                # fire a save complete event
                self._fire_save_notification( wordMap )
            else:
                self._fire_error_saving_notification( wordMap )

    def write_to_db( self, *args ):
        """Takes a list of objects and flushes them to the database"""
        try:
            toSave = [ a for a in args ]
            print( toSave )
            # save them
            self.session.add_all( toSave )
            self.session.commit( )
            return True
        except Exception as e:
            print( e )
            return False
