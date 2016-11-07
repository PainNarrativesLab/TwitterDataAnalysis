"""
These are for the database which holds individual words

Created by adam on 11/4/16
"""
__author__ = 'adam'

import os
import sys
import xml.etree.ElementTree as ET

import sqlalchemy
from sqlalchemy import Table, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
# connecting to db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Base class that maintains the catalog of tables and classes in db
Base = declarative_base()

class Connection(object):
    """
    Parent class for creating sqlalchemy engines, session objects,
    and other db interaction stuff behind the scenes from a file
    holding credentials

    Attributes:
        engine: sqlalchemy engine instance
        session: sqlalchemy local session object. This is the property that should do most work
        _credential_file: String path to file with db connection info
        _username: String db username
        _password: String db password
        _server: String db server
        _port: db port
        _db_name: String name of db
    """

    def __init__(self, credential_file=None):
        """
        Loads db connection credentials from file and returns a mysql sqlalchemy engine
        Args:
            :param credential_file: String path to the credential file to use
        Returns:
    """

class Word(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String(225))
    inserted_at = Column(String(225))
    updated_at = Column(String(225))
    relationship( "WordMapping", backref="words" )
    relationship( "StandardizedWordMapping", backref="words" )

class StandardizedWord(Base):
    """Correctly spelled, English words"""
    __tablename__ = 'std_words'
    id = Column( Integer, primary_key=True, autoincrement=True )
    word = Column( String( 225 ) )
    inserted_at = Column( String( 225 ) )
    updated_at = Column( String( 225 ) )


class WordMapping(Base):
    """Mapping of the word's position within the tweet"""
    __tablename__ = 'word_map'
    tweet_id =Column( Integer, primary_key=True, autoincrement=False )
    word_id =Column( Integer,  ForeignKey('words.id'), primary_key=True, autoincrement=False )
    sentence_index =Column( Integer, primary_key=False, autoincrement=False )
    word_index=Column( Integer, primary_key=False, autoincrement=False )


class StandardizedWordMapping(Base):
    """Mapping from twitter words to correctly spelled, English words
    Note, only word_id needs to be primary since it is one word_id will have one mapping to standard id
     """
    __tablename__ = 'std_words_map'
    word_id = Column( Integer, ForeignKey('words.id'), primary_key=True, autoincrement=False )
    standardized_word_id = Column( Integer, primary_key=False, autoincrement=False )
    inserted_at = Column( String( 225 ) )
    updated_at = Column( String( 225 ) )


if __name__ == '__main__':
    pass
    # connect to db
     # ORM's handle to database at global level
    # Session = sessionmaker(bind=mysql_en)