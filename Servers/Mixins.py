"""
Created by adam on 4/24/18
"""
__author__ = 'adam'


class ResponseStoreMixin( object ):

    def __init__( self ):
        self.taco = 'nom'
        # The store of future objects returned
        self.responses = [ ]
        super().__init__()

    def prune_responses( self ):
        """Iterate through the existing responses and remove any which are complete"""
        pre = len( self.responses )
        self.responses = [ self.responses.remove( r ) for r in self.responses if r is not None and r.done() ]
        rem = pre - len( self.responses )
        print( 'responses removed: %s' % rem )

    def add_response( self, response ):
        if type( response ) is not None:
            self.responses.append( response )
            # self.start_watcher()
            # watcher ruins the async behaviour

    @property
    def pendingResponseCount( self ):
        """The number of Futures which have not yet completed"""
        return len( self.responses )

    # def start_watcher( self ):
    #     while True:
    #         # While we're waiting for the promises to resolve
    #         # we rest a bit and then check the value again
    #         # try:
    #         self.prune_responses()
    #         if len( self.responses ) == 0:
    #             break
    #             # raise AllResponsesComplete
    #
    #         time.sleep( 1 )
    #         #
    # except AllResponsesComplete:
    #     # Now we're really done
    #     print( "Responses are complete" )
    #     break


if __name__ == '__main__':
    pass
