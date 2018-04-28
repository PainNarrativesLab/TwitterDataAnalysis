"""
Created by adam on 3/28/18
"""
__author__ = 'adam'


class DBExceptions( Exception ):
    def __init__( self ):
        self.message = "DB error"


class BadPayloadException( DBExceptions ):
    """Problem with decoding and converting the payload into a Result"""

    def __init__( self ):
        super().__init__()
        self.message = "Bad payload received"


class SavingErrorException( DBExceptions ):
    """Problem with saving the result"""

    def __init__( self ):
        super().__init__()
        self.message = "Problem saving result"


class ShutdownCommanded( Exception ):

    def __init__( self, **kwargs ):
        super().__init__()
        for k in kwargs.keys():
            self[k] = kwargs[k]