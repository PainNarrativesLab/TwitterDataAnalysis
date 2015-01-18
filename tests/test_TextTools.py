import unittest

from TextTools import *
import nltk

class TweetTextWordBagMakerTest(unittest.TestCase):
    def setUp(self):
        self.object = TweetTextWordBagMaker()

    def tearDown(self):
        self.object = ''

    def test_add_to_ignorelist(self):
        """
        The tested function combines the lists, removes duplicates, and converts to a tuple
        """
        #testlist1 = ['cat', 'fish']
        #testlist2 = ['cat', 'taco', 'burrito']
        #expect = ('cat', 'fish', 'taco', 'burrito')

        testlist1 = [1, 2]
        testlist2 = [2, 3, 4, 5]
        expect = (1, 2, 3, 4, 5)
        
        self.object.add_to_ignorelist(testlist1)
        #make sure adds to the list
        #t1 = list(self.object.ignore).sort()
        #self.assertListEqual(t1, testlist1.sort())
        self.object.add_to_ignorelist(testlist2)
        #make sure edited out the duplicates
        self.assertTupleEqual(self.object.ignore, expect)
    
    def test__make_wordbag(self):
        test = "The quick brown fox became a delicious taco for the hungry cat. All lived happily ever after"
        expect = ["the", "quick",  "brown", "fox", "became", "a", "delicious", "taco", "for", "the", "hungry", "cat", ".", "all", "lived", "happily", "ever", "after"]
        result = self.object._make_wordbag(test)
        self.assertListEqual(result, expect)
    
    def test__filter_ignored_terms(self):
        to_remove = ['dog', 'cow']
        test = ['cat', 'dog', 'fish', 'cow']
        expect = ['cat', 'fish']
        self.object.add_to_ignorelist(to_remove)
        result = self.object._filter_ignored_terms(test)
        self.assertListEqual(result, expect)
    
    def test__filter_usernames(self):
        test = ['taco', '@burrito', 'cat', '@dog']
        expect = ['taco', 'cat']
        result = self.object._filter_usernames(test)
        self.assertListEqual(result, expect)
    
    def test__filter_urls(self):
        test = ['taco', '//t.co', 'cat', '//t.co']
        expect = ['taco', 'cat']
        result = self.object._filter_urls(test)
        self.assertListEqual(result, expect)
    
 
    def test_process(self):
        test = [{'tweetID' : 1, 'tweetText' : "The first tweet. It has text"},
            {'tweetID' : 2, 'tweetText' : "The quick brown fox became a delicious taco for the hungry cat. All lived happily ever after"}]
        expect = ["first", "tweet", "text", "quick", "brown", "fox", "became", "delicious", "taco", "hungry", "cat",
                  "lived", "happily", "ever"]
        self.object.add_to_ignorelist([".", ","])
        self.object.add_to_ignorelist(nltk.corpus.stopwords.words('english'))
        self.object.process(test)
        self.assertEqual(self.object.masterbag, expect)
        self.assertTupleEqual(self.object.tweet_tuples[0], (1, ["first", "tweet", "text"]))
        self.assertTupleEqual(self.object.tweet_tuples[1], (2, ["quick", "brown", "fox", "became", "delicious", "taco", "hungry", "cat", "lived", "happily", "ever"]))

class WordFiltersTest(unittest.TestCase):
    def setUp(self):
        self.object = WordFilters()

    def tearDown(self):
        self.object = ''
    
    def test_remove_fragments(self):
        test = ['cat', 'dog', "amp", '...', '//t.co', "'re'", "'m", 'fish', "'s", 'cow']
        expect = ['cat', 'dog', 'fish', 'cow']
        result = self.object.remove_fragments(test)
        self.assertListEqual(result, expect)
    
    def test_remove_punctuation(self):
        test = ['cat', 'dog', "&", '.', '/', "'", "!", 'fish', "#", 'cow']
        expect = ['cat', 'dog', 'fish', 'cow']
        result = self.object.remove_punctuation(test)
        self.assertListEqual(result, expect)
    
    def test_filter_stopwords(self):
        test = ['taco', 'a', 'cat', 'the']
        expect = ['taco', 'cat']
        result = self.object.filter_stopwords(test)
        self.assertListEqual(result, expect)
        