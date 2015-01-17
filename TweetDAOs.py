"""
This contains classes for loading tweet data
"""
import TwitterSQLService

class TweetTextGetter(TwitterSQLService.SQLService):
    """
    Loads all tweetids and tweettext
    
    Args:
        test: Whether to use the test db
        local: Whether to use the local or remote db
    
    Returns:
        List of dictionaries with keys tweetID and tweetText
    """
    def __init__(self, test=False, local=True):
        TwitterSQLService.SQLService.__init__(self, test, local)
        self.query = """SELECT tweetID, tweetText FROM tweets"""
        self.val = []
        self.returnAll()
        return list(self.results)