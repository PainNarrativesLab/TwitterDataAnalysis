"""
Created by adam on 3/27/18
"""
__author__ = 'adam'

from DataTools.Cursors import UserCursor
from Loggers.FileLoggers import FileWritingLogger
from ProcessingTools.Listeners import SaveListener
from ProcessingTools.ProcessingControllers import UserProcessingController
from ProcessingTools.QueueTools import SaveQueueHandler
from TextProcessors.Filters import URLFilter, UsernameFilter, PunctuationFilter, NumeralFilter, StopwordFilter
from TextProcessors.Modifiers import WierdBPrefixConverter, CaseConverter
from TextProcessors.Processors import SingleWordProcessor

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


def run_test(controller, cursor, number):
    us = []
    for i in range(0, number):
        us.append(cursor.next())
    [controller.process(u) for u in us]


def process(controller, cursor):
    # all users
    user_count = 0

    while True:
        try:
            user = cursor.next()
            #         Note that we're not going to add the id to the map yet
            controller.process(user)
            user_count += 1
        except StopIteration as e:
            print("%s users processed" % user_count)
            break

    return control


if __name__ == '__main__':
    # Initialize logger
    logger = FileWritingLogger(name='UserProfileWords')

    # First set up the object which will handle applying
    # filters and modifiers to each word
    word_processor = SingleWordProcessor()
    word_processor.add_filters(filters)
    word_processor.add_modifiers(modifiers)

    # Set up the machinery for saving the
    # processed results
    queueHandler = SaveQueueHandler()
    listener = SaveListener()
    queueHandler.register_listener(listener)

    # Finally create the command and control
    control = UserProcessingController(queueHandler)
    control.load_word_processor(word_processor)
    control.set_notice_logger(logger)

    # create user cursor
    cursor = UserCursor(language='en')

    logger.log("Starting user profile words parsing ")
    run_test(control, cursor, 3)
    logger.log("Finished user profile words parsing ")
    # run
    # process(control, cursor)
