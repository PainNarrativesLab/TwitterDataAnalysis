"""
Created by adam on 7/6/17
"""
import unittest

from unittest import TestCase

from DataTools.Cursors import UserCursor
from TweetORM import Users

__author__ = 'adam'

language = 'abc'
limit = 50

t = UserCursor(limit=limit, language=language)


class TestUserCursor(TestCase):
    def test__create_iterator(self):
        self.assertEqual(t.limit, limit)
        self.assertEqual(t.language, language)
        # del t

    def test_next_user(self):
        # t = UserCursor()
        obj = t.next_user()
        # del t
        self.assertIsInstance(obj, Users )

    def test_next(self):
        # t = UserCursor()
        obj = t.next()
        # del t
        self.assertIsInstance(obj, Users )


if __name__ == '__main__':
    unittest.main()
