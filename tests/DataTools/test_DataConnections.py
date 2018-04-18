import unittest

import sqlalchemy

from DataTools import DataConnections


class ConnectionMock( DataConnections.Connection ):
    def _make_engine( self ):
        pass

    def __init__( self, credential_file ):
        self.engine = None
        super().__init__( credential_file )


class ConnectionTest( unittest.TestCase ):
    def setUp( self ):
        self.cred_file = 'tests/sql_test_credentials.xml'
        self.server = 'testhost'
        self.port = 3000
        self.db_name = 'testdbname'
        self.password = 'testpassword'
        self.username = 'testusername'

    def test_load_credentials( self ):
        conn = ConnectionMock( self.cred_file )
        self.assertEqual( conn._server, self.server )
        self.assertEqual( conn._port, self.port )
        self.assertEqual( conn._db_name, self.db_name )
        self.assertEqual( conn._password, self.password )
        self.assertEqual( conn._username, self.username )


class SqliteConnectionTest( unittest.TestCase ):
    def setUp( self ):
        pass

    def test_make_engine( self ):
        conn = DataConnections.SqliteConnection()
        self.assertIsInstance( conn.engine, sqlalchemy.engine.base.Engine, 'created engine' )
        self.assertIsInstance( conn.engine, sqlalchemy.engine.base.Engine, 'created engine' )


class MySqlConnectionTest( unittest.TestCase ):
    def setUp( self ):
        self.cred_file = 'tests/sql_test_credentials.xml'

    def test_make_engine( self ):
        """
        NB., test dsn string doesn't use the port
        """
        conn = DataConnections.MySqlConnection( self.cred_file )
        self.assertIsInstance( conn.engine, sqlalchemy.engine.base.Engine, 'created engine' )
        self.assertEqual( conn._dsn, "mysql+mysqlconnector://testusername:testpassword@testhost:3000/testdbname",
                          "Correct dsn created" )


class DAO_family_test( unittest.TestCase ):
    def setUp( self ):
        self.engine1 = sqlalchemy.create_engine( 'sqlite:///:memory:', echo=True )
        self.engine2 = sqlalchemy.create_engine( 'sqlite:///:memory:', echo=True )
        self.object1 = DataConnections.DAO( self.engine1 )
        self.object2 = DataConnections.DAO( self.engine2 )

    def test_class_inheritance( self ):
        self.assertEqual( type( self.object1.global_session ), sqlalchemy.orm.session.sessionmaker,
                          "object1 has correct session factory" )
        self.assertEqual( type( self.object2.global_session ), sqlalchemy.orm.session.sessionmaker,
                          "object2 has correct session factory" )
        self.assertEqual( self.object1.global_session, self.object2.global_session,
                          "One global_session shared btwn objects " )
        self.assertNotEqual( self.object1.session, self.object2.session, "Objects have distinct sessions" )


if __name__ == '__main__':
    unittest.main()
