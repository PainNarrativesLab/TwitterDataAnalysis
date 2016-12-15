"""
This contains classes for loading tweet data

In the process of being converted to use sqlalchemy
"""
import os
import sys

import sqlalchemy
from sqlalchemy import Table, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
# connecting to db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from DataTools.DataConnections import *

# Base class that maintains the catalog of tables and classes in db
Base = declarative_base()



class Hashtags(Base):
    __tablename__ = 'hashtags'
    # Here we define columns for the table hashtags
    # Notice that each column is also a normal Python instance attribute.
    tagID = Column(Integer, primary_key=True)
    hashtag = Column(String(100), nullable=False)

class Tweets(Base):
    __tablename__ = 'tweets'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    tweetID = Column(Integer, primary_key=True, autoincrement=False)
    userID = Column(Integer, ForeignKey('users.userID'))
    tweetText = Column(String(250))
    favorite_count = Column(Integer)
    source = Column(String(250), nullable=False)
    retweeted = Column(String(10))
    retweet_count = Column(Integer)
    in_reply_to_screen_name = Column(String(100))
    favorited = Column(String(10))
    lang = Column(String(100))
    created_at = Column(String(100))
    profile_background_tile = Column(String(100))
    is_translation_enabled = Column(String(100))
    profile_location = Column(String(100))

class Users(Base):
    __tablename__ = 'users'
    indexer = Column(Integer, unique=True)
    userID = Column(Integer, primary_key=True, autoincrement=False)
    screen_name = Column(String(225))
    id_str = Column(String(225))
    name = Column(String(225))
    description = Column(String(250))
    lang = Column(String(100))
    utc_offset = Column(String(100))
    verified = Column(String(100))
    followers_count = Column(Integer)
    friends_count = Column(Integer)
    url = Column(String(100))
    time_zone = Column(String(100))
    created_at = Column(String(100))
    entities = Column(String(225))
    favourites_count = Column(Integer)
    statuses_count = Column(Integer)
    id = Column(String(225))
    location = Column(String(225))
    is_translation_enabled = Column(String(10))

class Tweet(Tweets):
    def __init__(self):
        super().__init__()

tweetsXtags = Table('tweetsXtags', Base.metadata,
    Column('tweetID', Integer, ForeignKey('tweets.tweetID')),
    Column('tagID', Integer, ForeignKey('hashtags.tagID'))
)

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
# Base.metadata.create_all(sqlite_engine)

#
