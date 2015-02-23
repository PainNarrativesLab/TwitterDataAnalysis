"""
This contains classes for loading tweet data

THIS SHOULD INSTEAD USE THE DAO IN TwitterMining
"""

import DAO


class TwitterSQLDAO(DAO.BaseDAO):
    """
    Base database abstraction layer for twitter mysql database
    """

    def __init__(self, test=False, local=True):
        if test is False:
            databaseName = 'twitter_data'
        else:
            databaseName = 'twitter_dataTEST'
        DAO.BaseDAO.__init__(self)
        if local is False:
            self.connectRemote(databaseName)
        else:
            self.connect(databaseName)


class TweetTextGetter(TwitterSQLDAO):
    """
    Loads all tweetids and tweettext
    
    Args:
        test: Whether to use the test db
        local: Whether to use the local or remote db
    
    Returns:
        List of dictionaries with keys tweetID and tweetText
    """

    def __init__(self, test=False, local=True):
        TwitterSQLDAO.__init__(self, test=test, local=local)


    def load_tweets(self):
        self.query = """SELECT tweetID, tweetText FROM tweets"""
        self.val = []
        self.returnAll()
        return list(self.results)


if __name__ == '__main__':
    pass