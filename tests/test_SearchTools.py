import unittest


class MyTestCase( unittest.TestCase ):
    def test_something( self ):
        self.assertEqual( True, False )

def test_isRetweet( ):
    retweet = "RT @Raymond_Norman: Asking for #assistance w deposit 4 #disabled #access apt. #homeless 3/22 #disability #pain #braininjury #neuropathy"
    nonRetweet = "Smashing your kneecap on the sink getting into the shower is NOT the one...thought the fooker was broke...#pain #breathe #ice #MrBump"
    assert (isRetweet( retweet ) is True)
    assert (isRetweet( nonRetweet ) is False)


test_isRetweet( )


if __name__ == '__main__':

    unittest.main( )
