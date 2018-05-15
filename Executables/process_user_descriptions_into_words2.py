"""
Created by adam on 3/27/18
"""

__author__ = 'adam'
import asyncio
import environment
import Servers.ServerControlCommander as Commander

async def run(future):
    import time

    import DataTools.Cursors
    from Loggers.FileLoggers import FileWritingLogger
    # from Controllers.ProcessingControllers import UserProcessingController, IProcessingController
    from ProcessingTools.Controllers.AsyncControl import Control
    from ProcessingTools.Processors.Processing import AsyncProcessor
    from ProcessingTools.Queues.AsyncQueues import AsyncServerQueueDropin

    # from Servers.ClientSide import ServerQueueDropin
    from TextProcessors.Filters import URLFilter, UsernameFilter, PunctuationFilter, NumeralFilter, StopwordFilter
    from TextProcessors.Modifiers import WierdBPrefixConverter, CaseConverter
    from TextProcessors.Processors import SingleWordProcessor

    # How many users to process
    LIMIT_USERS = None
    # LIMIT_USERS = 500

    filters = [
        UsernameFilter(),
        PunctuationFilter(),
        URLFilter(),
        NumeralFilter(),
        StopwordFilter()
    ]

    modifiers = [
        WierdBPrefixConverter(),
        CaseConverter()
    ]


    # First set up the object which will handle applying
    # filters and modifiers to each word
    word_processor = SingleWordProcessor()
    word_processor.add_filters( filters )
    word_processor.add_modifiers( modifiers )

    processor = AsyncProcessor()
    processor.load_word_processor(word_processor)

    # Set up the machinery for saving the
    # processed results
    queueHandler = AsyncServerQueueDropin()

    # create the command and control
    control = Control( queueHandler=queueHandler, processor=processor )

    # create user cursor
    cursor = DataTools.Cursors.WindowedUserCursor( language='en' )

    # Run it
    print('about to process')
    await control.process_from_cursor(cursor, LIMIT_USERS)
    print('done processing')
    future.set_result('Done')


def main():
    print('ready to run')

    loop = asyncio.get_event_loop()
    future = asyncio.Future()
    # wraps as a task (i.e., with a future)
    asyncio.ensure_future(run(future))
    # future.add_done_callback( Commander.flush_and_shutdown_server )
    loop.run_until_complete(future)
    Commander.flush_and_shutdown_server()
    print(future.result())
    loop.close()
    # exit()


if __name__ == '__main__':
    main()
    # print('ready to run')
    #
    # loop = asyncio.get_event_loop()
    # future = asyncio.Future()
    # # wraps as a task (i.e., with a future)
    # asyncio.ensure_future(main(future))
    # loop.run_until_complete(future)
    # print(future.result())
    # loop.close()
    # exit()
