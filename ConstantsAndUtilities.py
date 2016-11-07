import string

from CsvTools import ListLoader as Loader
from UtilityDecorators import *

from environment import *

class Ignore( object ):
    """
    This contains all the terms to be ignored from hashtags etc. It is inherited by other classes which do cleaning
    
    Attributes:
        fragments: (Class attribute) String fragments which should be filtered out
        words: (Class attribute) Dictionary with categories of irrelevant terms as keys (placenames, smallwords, socialmediaterms, irrelevant)
        word_tuple: (Class attribute and instance attribute) Tuple with everything to ignore
    """
    FRAGMENTS_FILE = '%s/ignore.fragments.csv' % MAPPING_PATH
    PUNCTUATION_FILE = '%s/ignore.punctuation.csv' % MAPPING_PATH
    WORDS_PLACENAMES_FILE = '%s/ignore.words.placenames.csv' % MAPPING_PATH
    WORDS_SMALLWORDS_FILE = '%s/ignore.words.smallwords.csv' % MAPPING_PATH
    WORDS_SOCIALMEDIA_FILE = '%s/ignore.words.socialmediaterms.csv' % MAPPING_PATH
    WORDS_IRRELEVANT_FILE = '%s/ignore.words.irrelevant.csv' % MAPPING_PATH

    fragments = [ ]
    punctuation = [ ]
    words = {
        'placenames': (),
        'smallwords': (),
        'socialmediaterms': (),
        'irrelevant': ()
    }

    def __init__( self ):
        self._construct( )
        self.word_tuple = Ignore.word_tuple

    @staticmethod
    def iterable( self ):
        """
        Unused / deprecated
        Iterable object for all the contents of the ignore list
        """
        raise NotImplementedError

    def generator( self ):
        """
        Generator which returns ignore words
        Example:
            generator = Ignore.generator()
            next(generator)
        """
        for word in self.word_tuple:
            yield word

    @classmethod
    def get_list( cls ):
        """
        Returns a list of everything to ignore
        """
        cls._construct( )
        return list( cls.word_tuple )

    @classmethod
    def _construct( cls ):
        """
        Constructs the list of things to ignore at the class level from
        various sources.
        Note: This uses the string built in list of punctuation
        """
        cls._load( )
        word_list = [ ]
        word_list += cls.fragments
        word_list += cls.punctuation
        [ word_list.append( x ) for x in string.punctuation ]
        [ word_list.append( word ) for k in list( Ignore.words.keys( ) ) for word in Ignore.words[ k ] ]
        cls.word_tuple = tuple( word_list )

    @classmethod
    def _load( cls ):
        """Populates the lists with valus from the stored data"""
        if len( cls.fragments ) == 0:
            cls.fragments = cls._process_single( cls.FRAGMENTS_FILE )
        if len( cls.punctuation ) == 0:
            cls.punctuation = cls._process_single( cls.PUNCTUATION_FILE )
        if len( cls.words[ 'placenames' ] ) == 0:
            cls.words[ 'placenames' ] = cls._process_single( cls.WORDS_PLACENAMES_FILE )
        if len( cls.words[ 'smallwords' ] ) == 0:
            cls.words[ 'smallwords' ] = cls._process_single( cls.WORDS_SMALLWORDS_FILE )
        if len( cls.words[ 'socialmediaterms' ] ) == 0:
            cls.words[ 'socialmediaterms' ] = cls._process_single( cls.WORDS_SOCIALMEDIA_FILE )
        if len( cls.words[ 'irrelevant' ] ) == 0:
            cls.words[ 'irrelevant' ] = cls._process_single( cls.WORDS_IRRELEVANT_FILE )

    @classmethod
    def _process_single( cls, filePath ):
        """If received a list of 1-tuples, extract the item from the tuples, make a list, then convert it to a tuple
        :rtype: tuple
        """
        listOfStuff = [ i[ 0 ] for i in Loader.read_csv( filePath ) ]
        return tuple( listOfStuff )


class Merge( object ):
    """
    This holds terms which are to be merged together in analyzing graphs
    
    Attributes:
        toMerge: Dictionary with the master term as key and values to be merged in list as values
    """
    TO_MERGE_FILE = '%s/merge.mapping.csv' % MAPPING_PATH

    toMerge = {}

    """This has the direction reversed so can look up the general term from the specific using find"""
    toMergeLookup = {}

    @classmethod
    def _load(cls):
        if len(cls.toMergeLookup.keys()) is 0:
            #read the file intro the simple 1-1 lookup dictionary
            cls.toMergeLookup =  Loader.read_csv_mapping( cls.TO_MERGE_FILE, False )
            #make the key-lists dictionary with empty lists as the values
            cls.toMerge = dict({ v: [] for k, v in cls.toMergeLookup.items( ) })
            #populate this lists
            { cls.toMerge[v].append(k) for k, v in cls.toMergeLookup.items( ) }

    @classmethod
    def get_map(cls, item):
        """Wrapper around toMergeLookup.get().
        Using this just in case so we won't be wedded
        to the dictionary storing the mapping
        """
        cls._load()
        return cls.toMergeLookup.get(item, None)


if __name__ == '__main__':
    Ignore._construct()

