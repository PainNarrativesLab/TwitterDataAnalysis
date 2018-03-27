"""
This runs various string processing operations
so that we may benchmark their performance

Created by adam on 12/15/16
"""

__author__ = 'adam'
# %cd /Users/adam/Dropbox/PainNarrativesLab/TwitterDataAnalysis
# %bookmark twitteranalysis

from environment import *

# General tools
# from urllib2 import URLError
import datetime
from threading import Thread

from OptimizationTools import *


# Initialize the tools for filtering and modifying the individual tweet words
import TextProcessors.Processors
from TextProcessors.Modifiers import *
from TextProcessors.Processors import *
import TextProcessors.Filters as Filters
from ProcessingTools import Listeners
from ProcessingTools import Workers
import ProcessingTools.QueueTools as QT

import DataTools.Cursors
import ConstantsAndUtilities
from DataTools import WordORM


# Pandas
import pandas as pd
pd.options.display.max_rows = 999  # let pandas dataframe listings go long




def add_run(frame, module, threads, tweets, time, datastructure, note):
    """Adds a record to the frame holding benchmark result data"""
    d = {
        'id': frame.id.max() + 1,
        'timestamp': datetime.datetime.now(),
        'module': module,
        'numThreads': threads,
        'numTweets': tweets,
        'totalTime': time,
        'tweetTime': time / tweets,
        'dataStructure': datastructure,
        'note': note
    }
    d = pd.DataFrame([d])
    frame = pd.concat([frame, d])
    return frame


def run_tweet_processing_benchmarking_test(results_file, RUNS, MAX_THREADS, START_THREADS, DATASTRUCTURES,  NOTE,  MODULE,  NUM_TWEETS):
    # Mission Control for benchmarking text tool performance

    """

    :type NUM_TWEETS: object
    """

    # Initialize the tools for filtering and modifying the individual tweet words
    word_processor = TextProcessors.Processors.SingleWordProcessor()
    ignore = ConstantsAndUtilities.Ignore()
    ignore._construct()
    merge = ConstantsAndUtilities.Merge()

    # reg filter
    ignoreListFilter = Filters.IgnoreListFilter()
    ignoreListFilter.add_to_ignorelist(ignore.get_list())
    ignoreListFilter.add_to_ignorelist(nltk.corpus.stopwords.words('english'))  # or do we keep them?

    # dawg filter
    ignoreDawgFilter = Filters.IgnoreDawgFilter()
    ignoreDawgFilter.add_to_ignorelist(ignore.get_list())
    ignoreDawgFilter.add_to_ignorelist(nltk.corpus.stopwords.words('english'))  # or do we keep them?

    word_processor.add_filters(Filters.UsernameFilter())
    word_processor.add_filters(Filters.PunctuationFilter())
    word_processor.add_filters(Filters.URLFilter())
    word_processor.add_filters(Filters.NumeralFilter())
    word_processor.add_modifiers(TextProcessors.Modifiers.WierdBPrefixConverter())
    # processor.add_modifiers( TextProcessors.Modifiers.UnicodeConverter() )
    word_processor.add_modifiers(TextProcessors.Modifiers.CaseConverter())

    # Load past results as a dataframe. We will write our run results to this fiile
    benchmarks = pd.read_csv(results_file)

    # Run the tests
    for THREADS in range(START_THREADS, MAX_THREADS):
        for DATASTRUCTURE in DATASTRUCTURES:
            for _ in range(RUNS):
                print("\n threads: %s   datastructure: %s   run: %s" % (THREADS, DATASTRUCTURE, _))

                # Create queue and listeners for processed tokens
                Queue = QT.SaveQueueHandler()
                Queue.register_listener(Listeners.SaveListener())

                # Load cursor for tweet ids
                cursor = DataTools.Cursors.TweetCursor()

                # Add regular or dawg filter
                if DATASTRUCTURE is 'dawg':
                    print('dawg')
                    word_processor.add_filters(ignoreDawgFilter)
                else:
                    word_processor.add_filters(ignoreListFilter)

                # Initialize everything we need
                # Workers.StringProcessingWorker.initialize( cursor, Queue, word_processor )
                threads = []
                time = Timer()

                # Go!
                time.start()

                if THREADS is 0:
                    worker = Workers.StringProcessingWorker()
                    worker.initialize(cursor, Queue, word_processor)
                    worker.do_it()

                else:
                    # if this run is using threads, we go this way
                    for _ in range(THREADS):
                        worker = Workers.StringProcessingWorker()
                        worker.initialize(cursor, Queue, word_processor)

                        # if DATASTRUCTURE is 'dawg':
                        #     thread = Thread( target=worker.do_it_dawg )
                        # else:
                        thread = Thread(target=worker.do_it)
                        threads.append(thread)
                        thread.start()

                    for t in threads:
                        t.join()

                # ....and stop!
                time.stop()

                # Good job! Now, write it down and get back out there, tiger!
                benchmarks = add_run(frame=benchmarks,
                                     module=MODULE,
                                     threads=THREADS,
                                     tweets=NUM_TWEETS,
                                     time=time.elapsed_seconds,
                                     datastructure=DATASTRUCTURE,
                                     note=NOTE)
                benchmarks.set_index(['id']).to_csv(results_file)


if __name__ == '__main__':

    RESULTS_FILE_PATH = "%s/tests/benchmarks/StringProcessingWorker.csv" % TEXT_TOOLS_PATH

    WordORM.create_db_tables()

    DEFAULT_RUNS = 5
    DEFAULT_MAX_THREADS = 12
    DEFAULT_START_THREADS = 10
    DEFAULT_DATASTRUCTURES = ('tuple', 'dawg')
    DEFAULT_NOTE = 'command line programmatic run 0-2 threads'
    DEFAULT_MODULE = 'stringProcessingWorker'
    DEFAULT_NUM_TWEETS = 1181  # don't rely on other stuff

    run_tweet_processing_benchmarking_test(results_file=RESULTS_FILE_PATH,
                                           RUNS=DEFAULT_RUNS,
                                           MAX_THREADS=DEFAULT_MAX_THREADS,
                                           START_THREADS=DEFAULT_START_THREADS,
                                           DATASTRUCTURES=DEFAULT_DATASTRUCTURES,
                                           NOTE=DEFAULT_NOTE,
                                           MODULE=DEFAULT_MODULE,
                                           NUM_TWEETS=DEFAULT_NUM_TWEETS)
