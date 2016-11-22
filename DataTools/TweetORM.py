"""
This contains classes for loading tweet data

In the process of being converted to use sqlalchemy
"""
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
            :return: sqlalchemy.create_engine Engine instance
        """
        self._credential_file = credential_file
        self._load_credentials()
        self._make_engine()

    def _load_credentials(self):
        """
        Opens the credentials file and loads the attributes
        """
        if self._credential_file is not None:
            credentials = ET.parse(self._credential_file)
            self._server = credentials.find('db_host').text
            self._port = credentials.find('db_port').text
            if self._port is not None:
                self._port = int(self._port)
            self._username = credentials.find('db_user').text
            self._db_name = credentials.find('db_name').text
            self._password = credentials.find('db_password').text

    def _make_engine(self):
        """
        Creates the sqlalchemy engine and stores it in self.engine
        """
        raise NotImplementedError


class MySqlConnection(Connection):
    """
    Uses the MySQL-Connector-Python driver (pip install MySQL-Connector-Python driver)
    """

    def __init__(self, credential_file):
        self._driver = '+mysqlconnector'
        super(__class__, self).__init__(credential_file)

    def _make_engine(self):
        if self._port:
            server = "%s:%s" % (self._server, self._port)
        else:
            server = self._server
        self._dsn = "mysql%s://%s:%s@%s/%s" % (self._driver, self._username, self._password, server, self._db_name)
        self.engine = create_engine(self._dsn)


class SqliteConnection(Connection):
    """
    Makes a connection to an in memory sqlite database.
    Note that does not actually populate the database. That
    requires a call to: Base.metadata.create_all(SqliteConnection)
    """
    def __init__(self):
        super().__init__()

    def _make_engine(self):
        self.engine = create_engine('sqlite:///:memory:', echo=True)


class BaseDAO(object):
    """
    Parent class for database interactions.
    The parent will hold the single global connection (i.e. sqlalchemy Session)
    to the db.
    Instance classes will have their own session instances
    Attributes:
        global_session: (class attribute) A sqlalchemy configurable sessionmaker factory (sqlalchemy.orm.session.sessionmaker)
            bound to the engine. Is not itself a session. Instead, it needs to be instantiated: DAO.global_session()
        engine: sqlalchemy.engine.base.Engine instance
    """
    global_session = None

    def __init__(self, engine):
        assert(isinstance(engine, sqlalchemy.engine.base.Engine))
        self.engine = engine
        if BaseDAO.global_session is None:
            BaseDAO._create_session(engine)

    @staticmethod
    def _create_session(engine):
        """
        Instantiates the sessionmaker factory into the global_session attribute
        """
        BaseDAO.global_session =  sqlalchemy.orm.sessionmaker(bind=engine)


class DAO(BaseDAO):
    """
    example instance. Need to use metaclass to ensure that
    all instances of DAO do this
    """
    def __init__(self, engine):
        assert(isinstance(engine, sqlalchemy.engine.base.Engine))
        super().__init__(engine)
        self.session = BaseDAO.global_session()


# Make engines
# sqlite_engine = create_engine('sqlite:///:memory:', echo=True)
# mysql_engine = create_engine("mysql://root:@localhost/twitter_data")
# test_mysql_engine = create_engine("mysql://root:@localhost/test_td")

#connect to db
# DataTools's handle to database at global level
# Session = sessionmaker(bind=mysql_engine)

# connect to db: Local object
# This is the object to use for db interactions
# session = Session()


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
#
# # -------------------------------------------------------------------
# import DAO
#
#
# class TwitterSQLDAO(DAO.BaseDAO):
#     """
#     Base database abstraction layer for twitter mysql database
#     """
#
#     def __init__(self, test=False, local=True):
#         if test is False:
#             databaseName = 'twitter_data'
#         else:
#             databaseName = 'twitter_dataTEST'
#         DAO.BaseDAO.__init__(self)
#         if local is False:
#             self.connectRemote(databaseName)
#         else:
#             self.connect(databaseName)
#
#
# class TweetTextGetter(TwitterSQLDAO):
#     """
#     Loads all tweetids and tweettext
#
#     Args:
#         test: Whether to use the test db
#         local: Whether to use the local or remote db
#
#     Returns:
#         List of dictionaries with keys tweetID and tweetText
#     """
#
#     def __init__(self, test=False, local=True):
#         TwitterSQLDAO.__init__(self, test=test, local=local)
#
#
#     def load_tweets(self):
#         self.query = """SELECT tweetID, tweetText FROM tweets"""
#         self.val = []
#         self.returnAll()
#         return list(self.results)


if __name__ == '__main__':
    # connect to db
    # DataTools's handle to database at global level
    Session = sessionmaker(bind=mysql_engine)