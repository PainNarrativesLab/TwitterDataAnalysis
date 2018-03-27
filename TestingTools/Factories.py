"""
Utilities for testing
These create fake objects

Created by adam on 3/21/18
"""
__author__ = 'adam'

import factory
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

import datetime

from ProcessingTools.Listeners import IListener
from ProcessingTools.QueueTools import IQueueHandler

fake = Faker()

import DataTools.TweetORM
import DataTools.WordORM

engine = create_engine('sqlite://')
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

Base.metadata.create_all(engine)


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = DataTools.TweetORM.Users
        sqlalchemy_session = session  # the SQLAlchemy session object

    userID = factory.Sequence(lambda n: n)
    screen_name = factory.Sequence(lambda n: u'User %d' % n)
    description = fake.text()


class TweetFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = DataTools.TweetORM.Tweets
        sqlalchemy_session = session  # the SQLAlchemy session object

    tweetID = factory.Sequence(lambda n: n)
    userID = factory.Sequence(lambda n: n)
    tweetText = fake.paragraph(nb_sentences=3, variable_nb_sentences=True, ext_word_list=None)
    lang = 'en'


class WordFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = DataTools.WordORM.Word
        sqlalchemy_session = session  # the SQLAlchemy session object

    id = factory.Sequence(lambda n: n)
    word = fake.word()
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

