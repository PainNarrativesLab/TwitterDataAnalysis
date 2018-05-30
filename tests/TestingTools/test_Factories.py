"""
Created by adam on 3/21/18
"""
__author__ = 'adam'

import unittest


from TestingTools.Factories import *
import TweetORM
import WordORM


class UserFactoryTests(unittest.TestCase):

    def test_creation(self):
        obj = UserFactory()
        self.assertIsInstance( obj, TweetORM.Users, "Is instance of User" )
        self.assertIsNotNone(obj.userID, "User id is not None")
        self.assertIsNotNone(obj.screen_name, "Screen name is not None")
        self.assertTrue(len(obj.screen_name) > 0,  "Screen name is not None")
        self.assertTrue(len(obj.description)>0, "Description is not None")

    def test_unique_values(self):
        obj = UserFactory()
        self.assertIsInstance( obj, TweetORM.Users, "Is instance of User" )
        self.assertTrue(obj.userID > 0, "User id has incremented")


class TweetFactoryTests(unittest.TestCase):

    def test_creation(self):
        obj = TweetFactory()
        self.assertIsInstance( obj, TweetORM.Tweets, "Is instance of Tweet" )
        self.assertIsNotNone(obj.tweetID, "Tweet id is not None")
        self.assertIsNotNone(obj.userID, "User id is not None")
        self.assertIsNotNone(obj.tweetText, "Tweet text is not None")
        self.assertTrue(len(obj.tweetText) > 0,  "Tweet text is not None")

    def test_unique_values(self):
        obj = TweetFactory()
        self.assertIsInstance( obj, TweetORM.Tweets, "Is instance of Tweet" )
        self.assertTrue(obj.tweetID > 0, "Tweet id has incremented")


class WordFactoryTests(unittest.TestCase):
    def test_creation(self):
        obj = WordFactory()
        self.assertIsInstance( obj, WordORM.Word, "Is instance of Word" )
        self.assertIsNotNone(obj.id, "id")
        self.assertIsNotNone(obj.word, "text is not None")
        self.assertTrue(len(obj.word) > 0,  "Word text is not None")


