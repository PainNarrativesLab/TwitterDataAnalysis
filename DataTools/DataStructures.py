"""
This contains various simple datastructures which the various tools use.
It does not contain ORM classes.

Created by adam on 11/6/16
"""
__author__ = 'adam'

from collections import namedtuple

Result = namedtuple('Result', ['sentence_index', 'word_index', 'text', 'id', 'type'])
#
# # This should become the default result since it can
# # be used for tweets or users
# GeneralResult = namedtuple('GeneralResult', ['sentence_index', 'word_index', 'text', 'obj_id'])


def is_result(r):
    """Tests for whether the item is either a Result or GeneralResult"""
    if isinstance(r, Result): # or isinstance(r, GeneralResult):
        return True
    return False


def make_tweet_result(sentenceIndex, wordIndex, text, tweetId):
    """Creates and returns a Result object"""
    if text is not None:
        if tweetId is not None:
            return Result(sentenceIndex, wordIndex, text, tweetId, 'tweet')


def make_user_result(sentenceIndex, wordIndex, text, userId):
    """Creates and returns a Result object"""
    if text is not None:
        return Result(sentenceIndex, wordIndex, text, userId, 'user')
