"""
Created by adam on 12/15/16
"""
import TextTools.Processors.SingleWordProcessors

__author__ = 'adam'

from threading import Thread

import ConstantsAndUtilities


# Initialize the tools for filtering and modifying the individual tweet words
import TextProcessors.Processors
from TextTools.Replacement.Modifiers import *

from deprecated import Listeners, Workers
import Queues.QueueTools as QT

import DataTools.Cursors


if __name__ == '__main__':
    Queue = QT.SaveQueueHandler( )
    Queue.register_listener( Listeners.SaveListener() )

    # Load cursor for tweet ids
    threads = []
    cursor = DataTools.Cursors.TweetCursor( )

    word_processor = TextTools.Processors.SingleWordProcessors.SingleWordProcessor()
    ignore = ConstantsAndUtilities.Ignore()
    ignore._construct( )
    merge = ConstantsAndUtilities.Merge()

    # reg filter
    ignoreListFilter = TextProcessors.Filters.IgnoreListFilter( )
    ignoreListFilter.add_to_ignorelist( ignore.get_list( ) )
    ignoreListFilter.add_to_ignorelist( nltk.corpus.stopwords.words( 'english' ) )  # or do we keep them?

    word_processor.add_filters(TextProcessors.Filters.UsernameFilter())
    word_processor.add_filters(TextProcessors.Filters.PunctuationFilter())
    word_processor.add_filters(TextProcessors.Filters.URLFilter())
    word_processor.add_filters(TextProcessors.Filters.NumeralFilter())
    word_processor.add_modifiers(TextProcessors.Modifiers.WierdBPrefixConverter())
    # processor.add_modifiers( TextProcessors.Modifiers.UnicodeConverter() )
    word_processor.add_modifiers(TextProcessors.Modifiers.CaseConverter())


    for _ in range(0, 10):
        worker = Workers.TestingWorker()
        # load tweet and stuff into worker
        worker.initialize( cursor.next_tweet( ), Queue, word_processor )
        # give the worker its own thread
        thread = Thread( target=worker.do_it )
        # start it running
        thread.start( )

    print ("%s threads running" % len(threads))
    for t in threads:
        t.join( )

    # print('-------------')
    #
    # for _ in range(0, 10):
    #     tweet = call_cursor()