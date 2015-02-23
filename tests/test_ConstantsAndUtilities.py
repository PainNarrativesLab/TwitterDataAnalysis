__author__ = 'adam'

import unittest
from ConstantsAndUtilities import *


class IgnoreTest(unittest.TestCase):
    def setUp(self):
        self.object = Ignore()

    def test_generator(self):
        pass
        # # expect = Ignore.words[0][0]
        # expect = 'recordstoreday'
        # result = self.object.generator()
        # self.assertEqual(expect, result)


if __name__ == '__main__':
    unittest.main()
