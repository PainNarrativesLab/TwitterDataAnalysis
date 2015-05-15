__author__ = 'adam'

import unittest
from ConstantsAndUtilities import *


class IgnoreTest(unittest.TestCase):
    def setUp(self):
        self.object = Ignore()

    def test_check_instance_properties_set(self):
        self.assertTrue(len(self.object.word_tuple) > 0)
        self.assertIn("'re'", self.object.word_tuple)
        self.assertIn("'m", self.object.word_tuple)

    def test_check_static(self):
        self.assertTrue(len(Ignore.word_tuple) > 0)
        self.assertIn("'re'", Ignore.word_tuple)
        self.assertIn("'m", Ignore.word_tuple)

    def test_generator(self):
        result = self.object.generator()
        for i in xrange(0, len(self.object.word_tuple)):
            self.assertEqual(self.object.word_tuple[i], next(result))

    def test_get_list(self):
        self.assertIsInstance(Ignore.get_list(), list, "whether object returned is list")
        self.assertTrue(len(Ignore.get_list()) > 0)

    def test_warn(self):
        import warnings
        warnings.warn("deprecated")



if __name__ == '__main__':
    unittest.main()
