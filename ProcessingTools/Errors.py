"""
Created by adam on 3/23/18
"""
__author__ = 'adam'


class ProcessingError(Exception):
    pass


class NonResultEnqueued(ProcessingError):
    def __init__(self):
        super().__init__()
        self.text = """A type of object other than Result or UserResult has beenplaced in the queue"""


class AllResponsesComplete( Exception ):
    pass

if __name__ == '__main__':
    pass