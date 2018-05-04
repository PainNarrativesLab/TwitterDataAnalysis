"""
Created by adam on 4/28/18
"""
__author__ = 'adam'

import contextlib
import os


def delete_files( folder_path ):
    """Removes all files from the specified folder path"""
    for root, dirs, files in os.walk( folder_path ):
        with contextlib.suppress( FileNotFoundError ):
            for name in files:
                print( 'removing %s' % name )
                filename = os.path.join( root, name )
                os.remove( filename )
