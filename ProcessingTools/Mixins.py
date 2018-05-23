"""
Various mixins which may be helpful in myriad places
Created by adam on 4/24/18
"""
__author__ = 'adam'


def process_id_generator(  ):
    v = 0
    while True:
        yield v
        v += 1


class ProcessIdHaver( object ):
    """Adds a process id (self.pid) upon intialization.
    If a prefix has been defined in self.id_prefix before
    the mixin is initialized, initialization will add the prefix
    separated by a dash"""

    id_generator = process_id_generator()

    def __init__( self ):
        v = next( type( self ).id_generator )
        if type( self.id_prefix ) is not None:
            self.pid = '%s-%s' % (self.id_prefix, v)
        else:
            self.pid = v
        super().__init__()


if __name__ == '__main__':
    pass
