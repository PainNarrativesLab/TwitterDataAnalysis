"""
Created by adam on 7/5/17
"""
from unittest import TestCase
from DataTools.Cursors import TweetCursor
from TweetORM import Tweet
__author__ = 'adam'

if __name__ == '__main__':
    pass


class TestTweetCursor(TestCase):
    def test__create_iterator(self):
        limit = 50

        t = TweetCursor(limit=limit)
        self.assertEqual(t.limit, limit)

    def test_next_tweet(self):
        t = TweetCursor()
        obj = t.next_tweet()
        self.assertIsInstance(obj, Tweet )

    def test_next(self):
        t = TweetCursor()
        obj = t.next()
        self.assertIsInstance(obj, Tweet )

    def test_limit_on(self):
        limit = 5
        t = TweetCursor(limit=limit)
        for i in range(0, limit):
            obj = t.next()
            self.assertIsInstance(obj, Tweet )
        #
        # obj = t.next()
        # self.assertNotIsInstance(obj, Tweet )