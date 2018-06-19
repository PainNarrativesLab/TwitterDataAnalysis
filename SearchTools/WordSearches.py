"""
Created by adam on 5/31/18
"""
__author__ = 'adam'
import sqlite3
import environment


def get_all_words_in_tweet(tweetId, db):
    """
    Returns all the words used in the tweet

    Example:
        words = get_all_words_in_tweet(331546674315014144, db=environment.TWEET_DB_NO_STOP)
        words = [x[2] for x in words]
    Result:
        words = ['thought', 'crying',
        'like', 'crazy',
        'im', 'tired',
        'pain','inevitability',
        'rely', 'life',
        'spoonie']
    """
    conn = sqlite3.connect(db)

    query = "SELECT * FROM word_map WHERE tweet_id = ?"
    param = (tweetId, )
    with conn:
        r = conn.execute(query, param)
        return r.fetchall()


if __name__ == '__main__':
    pass