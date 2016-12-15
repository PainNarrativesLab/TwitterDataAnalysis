import unittest

from DataTools.DataRepositories import *


class WordRespositoriesTest( unittest.TestCase ):
    def setUp(self):
        self.object = WordRepository()

    def test_get_word_happy_modify_existing( self ):
        w = self.object.get_word( 'taco1' )
        w.word = 'taco taco'
        result = self.object.write_to_db( w )
        self.assertTrue( result )


if __name__ == '__main__':
    unittest.main( )
