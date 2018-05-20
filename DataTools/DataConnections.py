"""
Created by adam on 11/6/16
"""
__author__ = 'adam'

import xml.etree.ElementTree as ET
from contextlib import contextmanager

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import environment
from DataTools.WordORM import create_db_tables
from environment import *

# Base class that maintains the catalog of tables and classes in db
Base = declarative_base()

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

import MySQLdb

@contextmanager
def session_scope(engine=None):
    """
    Provide a transactional scope around a series of operations.

    We need a single db connection instance for all of the
    server processes. Otherwise, we will have trouble with
    concurrent writes to the file.
    That's what we create here

    usage:
        with sesssion_scope() as session:
            ...do stuff...
    """
    try:
        if engine is None:
            engine = initialize_engine( environment.ENGINE )
        # DataTools's handle to database at global level
        # SessionFactory = make_scoped_session_factory(engine)
        SessionFactory = make_session_factory(engine)

        if environment.ENGINE == 'sqlite' or environment.ENGINE == 'sqlite-file':
            # We need to get the db into memory when start up
            # environmental variables will determine details of the
            # db
            create_db_tables( engine )

        session = SessionFactory()
        yield session
        session.commit()

    except:
        session.rollback()
        raise

    finally:
        if session:
            session.close()


def make_scoped_session_factory(engine):
    session_factory = sessionmaker(bind=engine)
    return scoped_session(session_factory)


def make_session_factory(engine):
    return sessionmaker( bind=engine )


def initialize_engine( conn=environment.ENGINE ):
    """Creates the relevant connection engine"""
    if conn is not None:
        method = { 'sqlite': _create_sqlite_engine,
                   'sqlite-file': _create_sqlite_file_engine,
                   'mysql': _create_mysql_engine,
                   'mysql_test': _create_mysql_test_engine
                   }.get( conn )

        engine = method()
        # Base.metadata.create_all( engine )
        return engine

    raise ValueError


def _create_sqlite_engine( echo=False ):
    """Creates an in-memory sqlite db engine"""
    conn = 'sqlite:///:memory:'
    print( "creating connection: %s " % conn )
    return create_engine( conn, echo=False )

file_path_generator = environment.sqlite_file_connection_string_generator()


def _create_sqlite_file_engine( conn=next(file_path_generator), echo=True ):
    """Creates an sqlite db engine using the file defined in SQLITE_FILE"""
    print( "creating connection: %s " % conn )
    return create_engine( conn, echo=echo )


def _create_mysql_engine():
    print( "creating connection: mysql " )
    return create_engine( 'mysql://root:''@localhost:3306/%s' % DB )


def _create_mysql_test_engine():
    print( "creating connection: mysql %s" % DB )
    if DB is 'twitter_wordsTEST':
        print( "creating connection: mysql twitter_wordsTEST " )
        return create_engine( 'mysql://root:''@localhost:3306/twitter_wordsTEST' )

    return create_engine( "mysql://root:''@localhost:3306/%s" % DB )

    # return create_engine("mysql+mysqlconnector://root:@localhost/)


class Connection( object ):
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

    def __init__( self, credential_file=None ):
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

    def _load_credentials( self ):
        """
        Opens the credentials file and loads the attributes
        """
        if self._credential_file is not None:
            credentials = ET.parse( self._credential_file )
            self._server = credentials.find( 'db_host' ).text
            self._port = credentials.find( 'db_port' ).text
            if self._port is not None:
                self._port = int( self._port )
            self._username = credentials.find( 'db_user' ).text
            self._db_name = environment.DB
            # self._db_name = credentials.find( 'db_name' ).text
            self._password = credentials.find( 'db_password' ).text

    def _make_engine( self ):
        """
        Creates the sqlalchemy engine and stores it in self.engine
        """
        raise NotImplementedError


class NonOrmMySqlConnection(Connection):

    def __init__( self, credential_file ):
        self._driver = '+mysqlconnector'
        super( __class__, self ).__init__( credential_file )

    def _make_engine( self ):
        if self._port:
            server = "%s:%s" % (self._server, self._port)
        else:
            server = self._server
        self.engine = MySQLdb.connect( server, self._username, self._password, self._db_name, cursorclass=MySQLdb.cursors.DictCursor )


class MySqlConnection( Connection ):
    """
    Uses the MySQL-Connector-Python driver (pip install MySQL-Connector-Python driver)
    """

    def __init__( self, credential_file ):
        self._driver = '+mysqlconnector'
        super( __class__, self ).__init__( credential_file )

    def _make_engine( self ):
        if self._port:
            server = "%s:%s" % (self._server, self._port)
        else:
            server = self._server
        self._dsn = "mysql%s://%s:%s@%s/%s" % (self._driver, self._username, self._password, server, self._db_name)
        self.engine = create_engine( self._dsn )


class SqliteFileConnection( Connection ):
    """
    Makes a connection to a file-based sqlite database.
    Note that does not actually populate the database. That
    requires a call to: Base.metadata.create_all(SqliteConnection)
    """

    def __init__( self ):
        super().__init__()

    def _make_engine( self ):
        self.engine = create_engine( 'sqlite:%s' % SQLITE_FILE, echo=False )


class SqliteConnection( Connection ):
    """
    Makes a connection to an in memory sqlite database.
    Note that does not actually populate the database. That
    requires a call to: Base.metadata.create_all(SqliteConnection)
    """

    def __init__( self ):
        super().__init__()

    def _make_engine( self ):
        self.engine = _create_sqlite_engine()
        # create_engine( 'sqlite:///:memory:', echo=True )


class BaseDAO( object ):
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

    def __init__( self, engine ):
        assert (isinstance( engine, sqlalchemy.engine.base.Engine ))
        self.engine = engine
        if BaseDAO.global_session is None:
            BaseDAO._create_session( engine )

    @staticmethod
    def _create_session( engine ):
        """
        Instantiates the sessionmaker factory into the global_session attribute
        """
        BaseDAO.global_session = sqlalchemy.orm.sessionmaker( bind=engine )


class DAO( BaseDAO ):
    """
    example instance. Need to use metaclass to ensure that
    all instances of DAO do this
    """

    def __init__( self, engine ):
        assert (isinstance( engine, sqlalchemy.engine.base.Engine ))
        super().__init__( engine )
        self.session = BaseDAO.global_session()


if __name__ == '__main__':
    pass
    # # connect to db
    # engine = initialize_engine()
    # # DataTools's handle to database at global level
    # Session = sessionmaker( bind=engine )
