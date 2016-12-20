"""
Created by adam on 12/15/16
"""
__author__ = 'adam'

#General tools
# from urllib2 import URLError
import datetime
from threading import Thread

import ConstantsAndUtilities
from DataTools import WordORM
from OptimizationTools import *
from environment import *
WordORM.create_db_tables()

#%cd /Users/adam/Dropbox/PainNarrativesLab/TwitterDataAnalysis
#%bookmark twitteranalysis

# Initialize the tools for filtering and modifying the individual tweet words
import TextProcessors.Processors
from TextProcessors.Modifiers import *
from TextProcessors.Processors import *

from ProcessingTools import Listeners
from ProcessingTools import Workers
import ProcessingTools.QueueTools as QT


import DataTools.Cursors

# Pandas
import pandas as pd
pd.options.display.max_rows = 999 #let pandas dataframe listings go long


if __name__ == '__main__':
    #Mission Control
    RUNS = 5
    MAX_THREADS = 12
    START_THREADS = 10
    DATASTRUCTURES = ('tuple', 'dawg')
    NOTE = 'command line programmatic run 0-2 threads'
    MODULE = 'stringProcessingWorker'
    NUM_TWEETS = 1181  # don't rely on other stuff

    # Initialize the tools for filtering and modifying the individual tweet words
    word_processor = TextProcessors.Processors.SingleWordProcessor( )
    ignore = ConstantsAndUtilities.Ignore( )
    ignore._construct()
    merge = ConstantsAndUtilities.Merge( )

    #reg filter
    ignoreListFilter = TextProcessors.Filters.IgnoreListFilter( )
    ignoreListFilter.add_to_ignorelist( ignore.get_list( ) )
    ignoreListFilter.add_to_ignorelist( nltk.corpus.stopwords.words( 'english' ) ) # or do we keep them?

    #dawg filter
    ignoreDawgFilter = TextProcessors.Filters.IgnoreDawgFilter()
    ignoreDawgFilter.add_to_ignorelist( ignore.get_list( ) )
    ignoreDawgFilter.add_to_ignorelist( nltk.corpus.stopwords.words( 'english' ) ) # or do we keep them?

    word_processor.add_to_filters( TextProcessors.Filters.UsernameFilter( ) )
    word_processor.add_to_filters( TextProcessors.Filters.PunctuationFilter( ) )
    word_processor.add_to_filters( TextProcessors.Filters.URLFilter( ) )
    word_processor.add_to_filters( TextProcessors.Filters.NumeralFilter( ) )
    word_processor.add_to_modifiers( TextProcessors.Modifiers.WierdBPrefixConverter() )
    # processor.add_to_modifiers( TextProcessors.Modifiers.UnicodeConverter() )
    word_processor.add_to_modifiers( TextProcessors.Modifiers.CaseConverter( ) )


    def add_run( frame, module, threads, tweets, time, datastructure, note ):
        """Adds a record to benchmarks"""
        d = {
            'id': frame.id.max( ) + 1,
            'timestamp': datetime.datetime.now( ),
            'module': module,
            'numThreads': threads,
            'numTweets': tweets,
            'totalTime': time,
            'tweetTime': time / tweets,
            'dataStructure': datastructure,
            'note': note
        }
        d = pd.DataFrame( [ d ] )
        frame = pd.concat( [ frame, d ] )
        return frame

    benchmarks = pd.read_csv( "%s/tests/benchmarks/StringProcessingWorker.csv" % TEXT_TOOLS_PATH )

    for THREADS in range( START_THREADS, MAX_THREADS ):
        for DATASTRUCTURE in DATASTRUCTURES:
            for _ in range( RUNS ):
                print( "\n threads: %s   datastructure: %s   run: %s" % (THREADS, DATASTRUCTURE, _) )

                # Create queue and listeners for processed tokens
                Queue = QT.SaveQueueHandler( )
                Queue.register_listener( Listeners.SaveListener( ) )

                # Load cursor for tweet ids
                cursor = DataTools.Cursors.TweetCursor( )

                # Add regular or dawg filter
                if DATASTRUCTURE is 'dawg':
                    print( 'dawg' )
                    word_processor.add_to_filters( ignoreDawgFilter )
                else:
                    word_processor.add_to_filters( ignoreListFilter )

                # Initialize everything we need
                # Workers.StringProcessingWorker.initialize( cursor, Queue, word_processor )
                threads = [ ]
                time = Timer( )

                # Go!
                time.start( )

                if THREADS is 0:
                    worker = Workers.StringProcessingWorker( )
                    worker.initialize( cursor, Queue, word_processor )
                    worker.do_it( )

                else:
                    # if this run is using threads, we go this way
                    for _ in range( THREADS ):
                        worker = Workers.StringProcessingWorker( )
                        worker.initialize( cursor, Queue, word_processor )

                        # if DATASTRUCTURE is 'dawg':
                        #     thread = Thread( target=worker.do_it_dawg )
                        # else:
                        thread = Thread( target=worker.do_it )
                        threads.append( thread )
                        thread.start( )

                    for t in threads:
                        t.join( )

                # ....and stop!
                time.stop( )

                # Good job! Now, write it down and get back out there, tiger!
                benchmarks = add_run( frame=benchmarks,
                                      module=MODULE,
                                      threads=THREADS,
                                      tweets=NUM_TWEETS,
                                      time=time.elapsed_seconds,
                                      datastructure=DATASTRUCTURE,
                                      note=NOTE )
                benchmarks.set_index( [ 'id' ] ).to_csv(
                    "%s/tests/benchmarks/StringProcessingWorker.csv" % TEXT_TOOLS_PATH )
