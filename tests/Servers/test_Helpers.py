import unittest

from DataTools.DataStructures import Result
from Factories import UserResultFactory, TweetResultFactory
from Servers.Helpers import *


class PayloadHelpers( unittest.TestCase ):
    def test_encode_payload( self ):
        p = UserResultFactory()
        r = encode_payload( p )
        self.assertIsInstance( r, str )

    def test_decode_payload_for_user( self ):
        r = UserResultFactory()
        p = encode_payload( r )
        d = decode_payload( p )

        self.assertEqual( r.sentence_index, d[ 0 ] )
        self.assertEqual( r.word_index, d[ 1 ] )
        self.assertEqual( r.text, d[ 2 ] )
        self.assertEqual( r.id, d[ 3 ] )
        self.assertEqual( r.type, d[ 4 ] )

    def test_decode_payload_for_tweet( self ):
        r = TweetResultFactory()
        p = encode_payload( r )
        d = decode_payload( p )

        self.assertEqual( r.sentence_index, d[ 0 ] )
        self.assertEqual( r.word_index, d[ 1 ] )
        self.assertEqual( r.text, d[ 2 ] )
        self.assertEqual( r.id, d[ 3 ] )
        self.assertEqual( r.type, d[ 4 ] )

    def test_make_result_from_decoded_payload_for_tweet( self ):
        r = TweetResultFactory()
        p = encode_payload( r )
        d = decode_payload( p )
        # call
        a = make_result_from_decoded_payload( d )
        # check
        self.assertIsInstance( a, Result )
        self.assertEqual( r, a )

    def test_make_result_from_decoded_payload_for_user( self ):
        r = UserResultFactory()
        p = encode_payload( r )
        d = decode_payload( p )
        # call
        a = make_result_from_decoded_payload( d )
        # check
        self.assertIsInstance( a, Result )
        self.assertEqual( r, a )


if __name__ == '__main__':
    unittest.main()
