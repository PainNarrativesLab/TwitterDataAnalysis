import unittest

from SearchTools.SearchTools import *

class FunctionTests( unittest.TestCase ):

    def test_isRetweet( self ):
        retweet = "RT @Raymond_Norman: Asking for #assistance w deposit 4 #disabled #access apt. #homeless 3/22 #disability #pain #braininjury #neuropathy"
        nonRetweet = "Smashing your kneecap on the sink getting into the shower is NOT the one...thought the fooker was broke...#pain #breathe #ice #MrBump"
        assert (isRetweet( retweet ) is True)
        assert (isRetweet( nonRetweet ) is False)



if __name__ == '__main__':

    unittest.main( )
