__author__ = 'adam'


class ProcessingError(Exception):
    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return "%s went bad on %s : %s" % (self.kind, self.identifier_type, self.identifier)


class TweetProcessingError(ProcessingError):
    def __init__(self, tweetID):
        self.kind = 'TweetProcessing'
        self.identifier_type = 'tweetID'
        ProcessingError.__init__(self, tweetID)


class StringProcessingError(ProcessingError):
    def __init__(self, string_processed):
        self.kind = 'StringProcessing'
        self.identifier_type = 'String content'
        ProcessingError.__init__(self, string_processed)
