"""
Created by adam on 7/6/17
"""
from unittest import TestCase

from DataTools.Cursors import UserCursor
from DataTools.TweetORM import Users

__author__ = 'adam'

if __name__ == '__main__':
    pass


class TestUserCursor(TestCase):
    def test__create_iterator(self):
        language = 'abc'
        limit = 50
        t = UserCursor(limit=limit, language=language)
        self.assertEqual(t.limit, limit)
        self.assertEqual(t.language, language)

    def test_next_user(self):
        t = UserCursor()
        obj = t.next_user()
        self.assertIsInstance(obj, Users )

    def test_next(self):
        t = UserCursor()
        obj = t.next()
        self.assertIsInstance(obj, Users )

