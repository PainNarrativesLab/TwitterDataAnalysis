"""
This contains various simple datastructures which the various tools use.
It does not contain ORM classes.

Created by adam on 11/6/16
"""
__author__ = 'adam'

from collections import namedtuple
Result = namedtuple('Result', ['sentence_index', 'word_index', 'text', 'tweet_id'])

