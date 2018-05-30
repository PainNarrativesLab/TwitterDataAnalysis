"""
Created by adam on 3/27/18
"""

__author__ = 'adam'
import asyncio
import environment

from profiling.OptimizingTools import log_start_stop
from Servers.ClientSide import Client
from DataTools.SqliteTools import initialize_master_db, delete_master_db
from Loggers.Helpers import delete_files


async def run(future):
    import DataTools.Cursors
    from ProcessingTools.Controllers.AsyncControl import Control
    from ProcessingTools.Processors.TweetProcessing import Processor
    from ProcessingTools.Queues.AsyncQueues import AsyncServerQueueDropin

    from TextTools.Filtration.Filters import URLFilter, UsernameFilter, PunctuationFilter, NumeralFilter, StopwordFilter
    from TextTools.Replacement.Modifiers import WierdBPrefixConverter, CaseConverter
    from TextTools.Processors.SingleWordProcessors import SingleWordProcessor

    filters = [
        UsernameFilter(),
        PunctuationFilter(),
        URLFilter(),
        NumeralFilter(),
        # StopwordFilter()
    ]

    modifiers = [
        WierdBPrefixConverter(),
        # need to run in this order so that the new front
        # of the word will be converted
        CaseConverter()
    ]

    # First set up the object which will handle applying
    # filters and modifiers to each word
    word_processor = SingleWordProcessor()
    word_processor.add_filters( filters )
    word_processor.add_modifiers( modifiers )

    processor = Processor()
    processor.load_word_processor(word_processor)

    # Set up the machinery for saving the
    # processed results
    c = Client()
    queueHandler = AsyncServerQueueDropin(client=c)
    # future.add_done_callback( c.async_send_flush_command )

    # create the command and control
    control = Control( queueHandler=queueHandler, processor=processor )

    # create user cursor
    cursor = DataTools.Cursors.WindowedTweetCursor( language='en' )

    # Run it
    print('Starting processing ')
    await control.process_from_cursor(cursor, environment.LIMIT)
    print('Processing complete. Processed %s tweets' % control.count_of_processed)
    await c.async_send_flush_command()
    # return the number processed as the value of the future
    future.set_result(control.count_of_processed)


@log_start_stop( [ environment.RUN_TIME_LOG ], text='no stopwords'  )
def main():
    print('Starting run')
    # create a clean db and instrumenation logs
    delete_files(environment.PROFILING_LOG_FOLDER_PATH)
    delete_files(environment.INTEGRITY_LOG_FOLDER_PATH)
    delete_master_db()
    initialize_master_db()

    # start the event loop which will schedule all tasks
    loop = asyncio.get_event_loop()
    future = asyncio.Future()
    # wraps as a task (i.e., with a future)
    asyncio.ensure_future(run(future))
    loop.run_until_complete(future)
    loop.close()
    print('done')
    return future.result()


if __name__ == '__main__':
    main()
