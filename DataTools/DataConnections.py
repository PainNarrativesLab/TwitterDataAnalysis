"""
Created by adam on 11/6/16
"""
__author__ = 'adam'

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from environment import *


# Base class that maintains the catalog of tables and classes in db
Base = declarative_base( )


def initialize_engine( ):
    if ENGINE != None:
        method = { 'sqlite': _create_sqlite_engine,
                   'mysql': _create_mysql_engine,
                   'mysql_test': _create_mysql_test_engine
                   }.get( ENGINE )

        engine = method( )
        # Base.metadata.create_all( engine )
        return engine
    raise ValueError


def _create_sqlite_engine( ):
    print("creating connection: sqlite ")
    return create_engine( 'sqlite:///:memory:', echo=False )


def _create_mysql_engine():
    print( "creating connection: mysql " )
    return create_engine( 'mysql://root:''@localhost:3306/%s' % DB )



def _create_mysql_test_engine( ):
    if DB is 'twitter_words':
        print( "creating connection: mysql twitter_wordsTEST " )
        return create_engine( 'mysql://root:''@localhost:3306/twitter_wordsTEST' )
    print( "creating connection: mysql test_td" )
    return create_engine( "mysql+mysqlconnector://root:@localhost/test_td" )


if __name__ == '__main__':
    # connect to db
    engine = initialize_engine( )
    # DataTools's handle to database at global level
    Session = sessionmaker( bind=engine )
