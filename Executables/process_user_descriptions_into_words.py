"""
Created by adam on 3/27/18
"""
from ProcessingTools.Errors import AllResponsesComplete

__author__ = 'adam'

import time
from time import sleep
from environment import *

import DataTools.Cursors
from Loggers.FileLoggers import FileWritingLogger
from ProcessingTools.ProcessingControllers import UserProcessingController, IProcessingController
from Servers.ClientSide import ServerQueueDropin
from TextProcessors.Filters import URLFilter, UsernameFilter, PunctuationFilter, NumeralFilter, StopwordFilter
from TextProcessors.Modifiers import WierdBPrefixConverter, CaseConverter
from TextProcessors.Processors import SingleWordProcessor

# How many users to process
# LIMIT_USERS = 500

LIMIT_USERS = None

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


def process( controller: IProcessingController, cursor: DataTools.Cursors.Cursor, limit=None ):
    """Runs the experiment
    :param controller:
    :param cursor:
    :param limit: The max number of objects to process. If None, will run until StopIteration is raised
    :return:
    """
    # number of users processed
    user_count = 0

    while True:
        try:
            user = cursor.next()
            #         Note that we're not going to add the id to the map yet
            controller.process( user )
            user_count += 1
            # print(controller.pendingResponseCount, user_count)
            if limit is not None and user_count == limit:
                # This won't get raised by the cursor
                # since we are stopping due to a user imposed limit
                raise StopIteration
        except StopIteration as e:
            print( "%s users processed (not nec done)" % user_count )
            break

    return user_count


if __name__ == '__main__':
    # Initialize logger
    logger = FileWritingLogger( name='UserProfileWords' )
    profileLogger = FileWritingLogger( name='Profile' )
    auditLogger = FileWritingLogger( name='AUDIT' )

    t1 = time.time()
    logger.add_break()

    # First set up the object which will handle applying
    # filters and modifiers to each word
    word_processor = SingleWordProcessor()
    word_processor.add_filters( filters )
    word_processor.add_modifiers( modifiers )

    # Set up the machinery for saving the
    # processed results
    queueHandler = ServerQueueDropin()

    # create the command and control
    control = UserProcessingController( queueHandler )
    control.load_word_processor( word_processor )
    control.set_notice_logger( logger )

    # create user cursor
    cursor = DataTools.Cursors.WindowedUserCursor( language='en' )
    CLIENT_MODULE = "WindowedUserCursor"
    SERVER_MODULE = 'Tornado'
    logger.log( "Start user profile --- %s %s " % (CLIENT_MODULE, SERVER_MODULE) )

    # Run it
    numberProcessed = process( control, cursor, LIMIT_USERS )

    while True:
        # While we're waiting for the promises to resolve
        # we rest a bit and then check the value again
        try:
            control.prune_responses()
            print( "%s futures pending after %s " % (control.pendingResponseCount, time.time() - t1) )
            if control.pendingResponseCount == 0:
                raise AllResponsesComplete
            sleep( 1 )

        except AllResponsesComplete:
            # Now we're really done
            print( "Responses are complete" )
            break

    # audit
    auditLogger.log( "cursor called: %s " % cursor.callCount )
    auditLogger.log( "enque called: %s" % queueHandler.enquedCount )
    auditLogger.log( "Sent count: %s" % queueHandler.sentCount )
    auditLogger.log( "Success count: %s" % queueHandler.successCount )
    auditLogger.log( "Error count: %s" % queueHandler.errorCount )

    numberProfiles = cursor.callCount

    t2 = time.time()
    logger.log( "Finish user profile words parsing " )
    elapsed = t2 - t1
    timePer = elapsed / numberProcessed
    msg = ("%s profiles (of %s) took %s seconds. That's %s seconds per profile" % (
        numberProcessed, numberProfiles, elapsed, timePer))
    logger.log( msg )
    profileMsg = "%s %s %s %s" % (CLIENT_MODULE, SERVER_MODULE, numberProcessed, elapsed)
    profileLogger.log( profileMsg )
    print( msg )
