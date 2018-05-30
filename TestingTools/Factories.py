"""
Utilities for testing
These create fake objects

Created by adam on 3/21/18
"""
__author__ = 'adam'

import datetime
import random

import factory
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

import DataTools.DataStructures
import TweetORM
import WordORM
from deprecated.Listeners import IListener
from Queues.Interfaces import IQueueHandler

engine = create_engine('sqlite://')
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

Base.metadata.create_all(engine)


def fake_text():
    return Faker().paragraph(nb_sentences=3, variable_nb_sentences=True, ext_word_list=None)


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = TweetORM.Users
        sqlalchemy_session = session  # the SQLAlchemy session object

    userID = factory.Sequence(lambda n: n)
    screen_name = factory.Sequence(lambda n: u'User %d' % n)
    description = factory.Sequence(lambda n: fake_text())

    # description = factory.Sequence(lambda n: fake.text())


class TweetFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = TweetORM.Tweets
        sqlalchemy_session = session  # the SQLAlchemy session object

    tweetID = factory.Sequence(lambda n: n)
    userID = factory.Sequence(lambda n: n)
    tweetText =  factory.Sequence(lambda n: fake_text())
    lang = 'en'


class WordFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = WordORM.Word
        sqlalchemy_session = session  # the SQLAlchemy session object

    id = factory.Sequence(lambda n: n)
    inserted_at = datetime.datetime.now()
    updated_at = datetime.datetime.now()



class DummyQueueFactory(IQueueHandler):
    def __init__(self):
        super().__init__()
        self.queue = []
        self.next_call_count = 0
        self.enque_call_count = 0

    def enque(self, item):
        self.enque_call_count += 1
        self.queue.append(item)

    def next(self):
        self.next_call_count += 1
        return True


class DummyIListenerFactory(IListener):
    def __init__(self):
        self.handle_call_count = 0
        self.queue = []

    def handle(self, handler):
        self.handle_call_count += 1
        self.queue.append(handler)


def TweetResultFactory():
    return DataTools.DataStructures.make_tweet_result( random.randint( 0, 10 ), random.randint( 0, 10 ), Faker().word(),
                                                       random.randint( 0, 99999999999 ) )


def UserResultFactory():
    return DataTools.DataStructures.make_user_result( random.randint( 0, 10 ), random.randint( 0, 10 ), Faker().word(),
                                                      random.randint( 0, 99999999999 ) )
