"""
These are for the database which holds individual words

Created by adam on 11/4/16
"""
__author__ = 'adam'

import environment

import datetime

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# import DataConnections

# Base class that maintains the catalog of tables and classes in db
Base = declarative_base()


class Word(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(UnicodeText)
    inserted_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.datetime.now())
    relationship("WordMapping", back_populates="word")
    relationship("StandardizedWordMapping", backref="word")


class StandardizedWord(Base):
    """Correctly spelled, English words"""
    __tablename__ = 'std_words'
    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String(225))
    inserted_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.datetime.now())


class WordMapping(Base):
    """Mapping of the word's position within the tweet or user description"""
    __tablename__ = 'word_map'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tweet_id = Column(BigInteger)
    user_id = Column(BigInteger)
    word_id = Column(Integer, ForeignKey('words.id'))
    word = relationship("Word")
    sentence_index = Column(Integer, primary_key=False, autoincrement=False)
    word_index = Column(Integer, primary_key=False, autoincrement=False)

    # tweet_id =Column( BigInteger, primary_key=True, autoincrement=False )
    # word_id = Column( Integer, ForeignKey('words.id') )
    # word = relationship("Word")
    # sentence_index =Column( Integer, primary_key=True )
    # word_index=Column( Integer, primary_key=True)


class WordMappingDeux( Base ):
    """Mapping of the word's position within the tweet or user description"""
    __tablename__ = 'word_map_deux'
    id = Column( Integer, primary_key=True, autoincrement=True )
    tweet_id = Column( BigInteger )
    user_id = Column( BigInteger )
    word = Column( UnicodeText )
    sentence_index = Column( Integer, primary_key=False, autoincrement=False )
    word_index = Column( Integer, primary_key=False, autoincrement=False )


class StandardizedWordMapping(Base):
    """Mapping from twitter words to correctly spelled, English words
    Note, only word_id needs to be primary since it is one word_id will have one mapping to standard id
     """
    __tablename__ = 'std_words_map'
    word_id = Column(Integer, ForeignKey('words.id'), primary_key=True, autoincrement=False)
    standardized_word_id = Column(Integer, primary_key=False, autoincrement=False)
    inserted_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.datetime.now())


def create_db_tables( engine=None, seed=False ):
    """Creates tables in the database"""
    # if engine is None:
    #     engine = DataConnections.initialize_engine()

    # create the tables
    Base.metadata.create_all(engine)
    # metadata = MetaData( )
