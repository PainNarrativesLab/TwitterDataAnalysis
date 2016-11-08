"""
Created by adam on 11/8/16
"""
__author__ = 'adam'

from environment import *
import TextTools.TextCleaningTools as T
import TweetDAOs

# Pandas
from pandas import DataFrame, Series
import pandas as pd
pd.options.display.max_rows = 999 #let pandas dataframe listings go long


#SqlAlchemy
import sphinxapi
from sphinxapi import SphinxClient

# Create your connection.

def isRetweet( text ):
    """
    Classifies whether a tweet is a retweet based on how it starts
    """
    if text[ :4 ] == "RT @":
        return True
    if text[ :4 ] == "MT @":
        return True
    return False

def isReply( tweetObject ):
    if tweetObject.in_reply_to_screen_name != None:
        return True
    if tweetObject.text[ 0 ] == '@':
        return True
    return False


search_terms = [ 'Spoonie',
                 'CRPS',
                 'Migraine',
                 'RSD',
                 'Fibro',
                 'Fibromyalgia',
                 'Vulvodynia',
                 'ChronicPain',
                 'pain',
                 'endometriosis',
                 'neuropathy',
                 'arthritis',
                 'neuralgia' ]



class Searcher( SphinxClient ):
    def __init__( self ):
        SphinxClient.__init__( self )
        self.index = 'user_idx'
        self.SetLimits( 0, 100000, 100000 )
        # self._limit = 1000
        # self._maxmatches = 1000
        # self.SetMatchMode(6)

    def search( self, term ):
        """
        Searches indext for term
        Args:
            term: The term to search for
        Returns:
            Dictionary with:
                'userids': list of user ids
                'indexer_ids': list of indexer ids
                'total_found': searchd's report of how many results found
                'info': searchd's dictionary of word frequency
        """
        result = self.Query( term, self.index )
        out = { 'term': term,
                'total_found': result[ 'total_found' ],
                'info': result[ 'words' ][ 0 ],
                'indexer_ids': [ ],
                'userids': [ ] }
        for r in result[ 'matches' ]:
            out[ 'userids' ].append( r[ 'attrs' ][ 'userid' ] )
            out[ 'indexer_ids' ].append( r[ 'id' ] )
        print
        "%s results: %s maxid: %s" % (term, out[ 'total_found' ], max( out[ 'indexer_ids' ] ))
        return out

    def search_complicated( self, term ):
        """
        Searches index for term. Created for use when searchd is limited
        to 1000 results.
        Args:
            term: The term to search for
        Returns:
            List of user ids
        """
        self.results = [ ]
        self.total_found = 0
        self.words = ''
        self.done = False
        while self.done is False:
            maxid = self._call_query( term )
            self._min_id = maxid
        return self.results

    def _call_query( self, term ):
        """
        Handles the actual search so can loop when necessary.
        """
        result = self.Query( term, self.index )
        ids = [ ]
        self.total_found = result[ 'total_found' ]
        self.words = result[ 'words' ]
        print( '%s total found: %s \n' % (term, self.total_found))
        for r in result[ 'matches' ]:
            self.results.append( r[ 'attrs' ][ 'userid' ] )
        ids.append( r[ 'id' ] )
        maxid = max( ids )
        print("%s results: %s maxid: %s" % (term, len( ids ), maxid) )
        if len( result[ 'matches' ] ) < 1000:
            self.done = True
        return maxid


def condition_searcher( search_term, condition, index='user_idx' ):
    """
    Runs search then adds to the result dict passed in
    Args:
        term: Term to search
        condition: Condition object to load with results
    """
    searcher = sphinxapi.SphinxClient( )
    searcher.SetLimits( 0, 100000, 100000 )
    result = searcher.Query( search_term, index )
    for r in result[ 'matches' ]:
        condition.add_userid( r[ 'attrs' ][ 'userid' ] )
        condition.add_indexer_id( r[ 'id' ] )
    print
    "%s results: %s maxid: %s" % (condition.name, condition.get_total( ), condition.get_maxid( ))
    return condition


class Condition( object ):
    """
    Data holder
    """

    def __init__( self, name, filepath=DATAFOLDER ):
        self.name = name
        self.datafile = "%s/%s.csv" % (filepath, self.name)
        self.indexer_ids = set( [ ] )
        self.userids = set( [ ] )
        self.users = ''

    def get_total( self ):
        """
        Returns the total number of users
        """
        return len( self.userids )

    def get_maxid( self ):
        """
        Returns the highest indexerid
        """
        return max( list( self.indexer_ids ) )

    def add_userid( self, userid ):
        """
        Add userid to list
        """
        self.userids.update( [ userid ] )

    def add_indexer_id( self, indexer_id ):
        """
        Add indexerid
        """
        self.indexer_ids.update( [ indexer_id ] )


class UserGetter( object ):
    """
    Retrieves user info and builds dataframe of users when given list of ids
    """

    def __init__( self, sql_alchemy_engine ):
        self.engine = sql_alchemy_engine

    def _get_user( self, searchterm, userid ):
        query = "SELECT userID, indexer, '%s' AS term, description AS profile FROM users WHERE userid = %s" % (
        searchterm, userid)
        return pd.read_sql_query( query, self.engine )

    def get_from_list( self, searchterm, userids ):
        """
        Args:
            searchterm: String that was searched for
            userids: List of userids to retrieve
        Returns:
            Dataframe with labels userID, indexer, term, profile
        """
        frames = [ ]
        for uid in userids:
            frames.append( self._get_user( searchterm, uid ) )
        return pd.concat( frames )

    def get_from_condition_object( self, condition_object ):
        """
        Reads userids etc from a Condition object and stores users in the object
        """
        assert (isinstance( condition_object, Condition ))
        result = self.get_from_list( condition_object.name, condition_object.userids )
        condition_object.users = result
        return condition_object

if __name__ == '__main__':

    # engine = create_engine('mysql://root:''@localhost:3306/twitter_data')
    # engine = create_engine('mysql://testuser:testpass@localhost/twitter_data')

    ## run indexer
    # searchd -c /usr/localsearchd -c /usr/local/etc/sphinx.conf --stop
    # cd /usr/local/etc/
    # /usr/local/Cellar/sphinx/2.1.9/bin/indexer --all
    # searchd -c /usr/local/etc/sphinx.conf

    s = dao.session.query( TweetDAOs.Users ).filter( TweetDAOs.Users.userID == 5981342 ).one( )
    print( s.screen_name )


    def tweetids( ):
        for t in dao.session.query( TweetDAOs.Tweets ).limit( 10 ):
            yield (t.tweetID)


    t = tweetids( )

    next( t )

    ug = UserGetter( engine )

    fibro_search = """'((Fibromyalgia) | (Fibro) | (fibro*) | (fm) | (fms))"""
    fibro = Condition( 'fibromyalgia' )
    condition_searcher( fibro_search, fibro )
    ug.get_from_condition_object( fibro )
    len( fibro.users )

    crps_search = """((crps) | (RSD) | (r.s.d.) |
            (c.r.p.s.) | (complex regional pain syndrome) |
            (chronic regional pain syndrome) | (reflex sympathetic dystrophy))"""
    crps = Condition( 'crps' )
    condition_searcher( crps_search, crps )
    ug.get_from_condition_object( crps )

    migraine_search = """((migraine) | (Migraineur) | (migr*))"""
    migraine = Condition( 'migraine' )
    condition_searcher( migraine_search, migraine )
    ug.get_from_condition_object( migraine )

    spoonie_search = """Spoonie"""
    spoonie = Condition( 'spoonie' )
    spoonie = condition_searcher( spoonie_search, spoonie )
    spoonie = ug.get_from_condition_object( spoonie )

    vulvodynia_search = """Vulvodynia | Vulvadynia"""
    vulvodynia = Condition( 'vulvodynia' )
    vulvodynia = condition_searcher( vulvodynia_search, vulvodynia )
    vulvodynia = ug.get_from_condition_object( vulvodynia )

    endo_search = """endometriosis | endo"""
    endo = Condition( 'endo' )
    endo = condition_searcher( endo_search, endo )
    endo = ug.get_from_condition_object( endo )

    neuropathy_search = """neuropathy"""
    neuropathy = Condition( 'neuropathy' )
    neuropathy = condition_searcher( neuropathy_search, neuropathy )
    neuropathy = ug.get_from_condition_object( neuropathy )

    arthritis_search = """((arthritis) | (*arthritis) | (oa) | (ra))"""
    arthritis = Condition( 'arthritis' )
    arthritis = condition_searcher( arthritis_search, arthritis )
    arthritis = ug.get_from_condition_object( arthritis )

    neuralgia_search = """(neuralgia) | (*neuralgia)"""
    neuralgia = Condition( 'neuralgia' )
    neuralgia = condition_searcher( neuralgia_search, neuralgia )
    neuralgia = ug.get_from_condition_object( neuralgia )

    shingles_search = """((shingles) | (post-herpetic neuralgia) | (PHN))"""
    shingles = Condition( 'shingles' )
    shingles = condition_searcher( shingles_search, shingles )
    shingles = ug.get_from_condition_object( shingles )

    backpain_search = """(back pain | backpain)"""
    backpain = Condition( 'backpain' )
    backpain = condition_searcher( backpain_search, backpain )
    backpain = ug.get_from_condition_object( backpain )

    headache_search = """(headache)"""
    headache = Condition( 'headache' )
    headache = condition_searcher( headache_search, headache )
    headache = ug.get_from_condition_object( headache )

