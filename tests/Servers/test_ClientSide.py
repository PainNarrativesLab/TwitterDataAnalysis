import unittest
from aiounittest import futurized, AsyncTestCase
from unittest.mock import Mock, patch


class ClientSideTests( unittest.TestCase ):
    def test_something( self ):
        self.assertEqual( True, False )


if __name__ == '__main__':
    unittest.main()
