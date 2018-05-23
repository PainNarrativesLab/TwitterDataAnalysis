"""
Various tools which may be useful in lots of places

Created by adam on 5/20/18
"""
__author__ = 'adam'

import warnings
from functools import wraps


def deprecated( deprecated_function, *args, **kwargs ):
    """
    Wrapper for deprecated functions which ensures that
    the user gets a warning that the function is deprecated
    when they call it.

    Use:
        @deprecated
        def fun(j):
            print(j)

    Output:
        DataTools/Cursors.py:14: DeprecationWarning: deprecated class threadsafe_iter:

    """

    @wraps( deprecated_function )
    def wrapper( *args, **kwargs ):
        warnings.filterwarnings( 'always' )
        warnings.warn( "deprecated", DeprecationWarning )
        deprecated_function( *args, **kwargs )

    return wrapper


if __name__ == '__main__':
    pass