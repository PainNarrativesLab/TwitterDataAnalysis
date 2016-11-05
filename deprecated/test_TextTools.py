"""
TODO Check that all of the following get done (after the change to new processor)
    words = [w.lower() for w in words]
    words = [w for w in words if w not in Ignore.punctuation]  #remove punctuation
    words = [w for w in words if w not in Ignore.fragments]  #remove fragments
    words = [w for w in words if w[0] != '@']  #Get rid of usernames
    words = [w for w in words if w[0:6] != '//t.co']  #Remove some urls
    words = [w for w in words if w not in Ignore.words['socialmediaterms']]  #Remove terms from social media
    words = [w for w in words if w not in nltk.corpus.stopwords.words('english')]  #Remove stopwords
"""

import unittest
import nltk
from TextAnalysis.TextTools import *


class URLCleanerTest(unittest.TestCase):
    """
    Removes some urls
    """
    def setUp(self):
        self.object = URLCleaner()

    def test_clean(self):
        test = [('taco', True), ('//t.co', False), ('cat', True), ('//t.co', False)]
        for t in test:
            self.assertEqual(self.object.clean(t[0]), t[1])


class UsernameCleanerTest(unittest.TestCase):
    def setUp(self):
        self.object = UsernameCleaner()

    def test_clean(self):
        test = [('taco', True), ('@taco', False), ('cat', True), ('@cat', False)]
        for t in test:
            self.assertEqual(self.object.clean(t[0]), t[1])


class NumeralCleanerTest(unittest.TestCase):
    def setUp(self):
        self.object = NumeralCleaner()

    def test_clean(self):
        test = [('taco', True), (1, False), ('cat', True), ('3', False), (['taco'], False)]
        for t in test:
            self.assertEqual(self.object.clean(t[0]), t[1])


class LemmatizerTest(unittest.TestCase):
    """
    Wrapper on nltk.stem.WordNetLemmatizer for lemmatizing words
    """
    def setUp(self):
        self.object = Lemmatizer()

    def test_process(self):
        self.assertIsInstance(self.object.lemmatizer, nltk.stem.WordNetLemmatizer)

    def test_process_excepts_if_not_string(self):
        self.assertRaises(AssertionError, self.object.process(4))


class PorterStemmerTest(unittest.TestCase):
    def setUp(self):
        self.object = PorterStemmer()

    def test_process(self):
        self.assertIsInstance(self.object.stemmer, nltk.stem.PorterStemmer)

    def test_process_excepts_if_not_string(self):
        self.assertRaises(AssertionError, self.object.process(4))


class WordBagMakerTest(unittest.TestCase):
    def setUp(self):
        self.object = WordBagMaker()

    def tearDown(self):
        self.object = ''

    def test_add_to_ignorelist(self):
        """
        The tested function combines the lists, removes duplicates, and converts to a tuple
        """
        testlist1 = [1, 2]
        testlist2 = [2, 3, 4, 5]
        expect = (1, 2, 3, 4, 5)

        self.object.add_to_ignorelist(testlist1)
        # make sure adds to the list
        # t1 = list(self.object.ignore).sort()
        # self.assertListEqual(t1, testlist1.sort())
        self.object.add_to_ignorelist(testlist2)
        # make sure edited out the duplicates
        self.assertTupleEqual(self.object._ignore, expect)

    def test__make_wordbag(self):
        test = "The quick brown fox became a delicious taco for the hungry cat. All lived happily ever after"
        expect = ["the", "quick",  "brown", "fox", "became", "a", "delicious", "taco", "for", "the", "hungry", "cat", ".", "all", "lived", "happily", "ever", "after"]
        result = self.object._make_wordbag(test)
        self.assertListEqual(result, expect)

    def test_process(self):
        test = ["The first tweet.",  "It has text", "The quick brown fox became a delicious taco for the hungry cat.",
                "All lived happily ever after"]
        expect = ["first", "tweet", "text", "quick", "brown", "fox", "became", "delicious", "taco", "hungry", "cat",
                  "lived", "happily", "ever"]
        self.object.add_to_ignorelist([".", ","])
        self.object.add_to_ignorelist(nltk.corpus.stopwords.words('english'))
        self.object.process(test)
        self.assertEqual(self.object.masterbag, expect)


class TweetTextWordBagMakerTest(unittest.TestCase):
    def setUp(self):
        self.object = TweetTextWordBagMaker()

    def tearDown(self):
        self.object = ''

    def test_add_to_ignorelist(self):
        """
        The tested function combines the lists, removes duplicates, and converts to a tuple
        """
        testlist1 = [1, 2]
        testlist2 = [2, 3, 4, 5]
        expect = (1, 2, 3, 4, 5)
        
        self.object.add_to_ignorelist(testlist1)
        # make sure adds to the list
        # t1 = list(self.object.ignore).sort()
        # self.assertListEqual(t1, testlist1.sort())
        self.object.add_to_ignorelist(testlist2)
        # make sure edited out the duplicates
        self.assertTupleEqual(self.object._ignore, expect)
    
    def test__make_wordbag(self):
        test = "The quick brown fox became a delicious taco for the hungry cat. All lived happily ever after"
        expect = ["the", "quick",  "brown", "fox", "became", "a", "delicious", "taco", "for", "the", "hungry", "cat", ".", "all", "lived", "happily", "ever", "after"]
        result = self.object._make_wordbag(test)
        self.assertListEqual(result, expect)
    
    # def test__filter_ignored_terms(self):
    #     to_remove = ['dog', 'cow']
    #     test = ['cat', 'dog', 'fish', 'cow']
    #     expect = ['cat', 'fish']
    #     self.object.add_to_ignorelist(to_remove)
    #     result = self.object._filter_ignored_terms(test)
    #     self.assertListEqual(result, expect)
    
    # def test__filter_usernames(self):
    #     test = ['taco', '@burrito', 'cat', '@dog']
    #     expect = ['taco', 'cat']
    #     result = self.object._filter_usernames(test)
    #     self.assertListEqual(result, expect)
    
    # def test__filter_urls(self):
    #     test = ['taco', '//t.co', 'cat', '//t.co']
    #     expect = ['taco', 'cat']
    #     result = self.object._filter_urls(test)
    #     self.assertListEqual(result, expect)

    def test_process(self):
        test = [{'tweetID': 1, 'tweetText': "The first tweet. It has text"},
                {'tweetID': 2, 'tweetText': "The quick brown fox became a delicious taco for the hungry cat. All lived happily ever after"}]
        expect = ["first", "tweet", "text", "quick", "brown", "fox", "became", "delicious", "taco", "hungry", "cat",
                  "lived", "happily", "ever"]
        self.object.add_to_ignorelist([".", ","])
        self.object.add_to_ignorelist(nltk.corpus.stopwords.words('english'))
        self.object.process(test)
        self.assertEqual(self.object.masterbag, expect)
        self.assertTupleEqual(self.object.tweet_tuples[0], (1, ["first", "tweet", "text"]))
        self.assertTupleEqual(self.object.tweet_tuples[1], (2, ["quick", "brown", "fox", "became", "delicious", "taco", "hungry", "cat", "lived", "happily", "ever"]))


class TextFiltersTest(unittest.TestCase):
    def setUp(self):
        self.object = TextFilters()

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


class WordFiltersTest(unittest.TestCase):
    def setUp(self):
        self.expected = ('cat', 'fish', 'taco', 'dog')
        self.object = WordFilter()

    def test_filter_words_tuple_case(self):
        self.object.filter_words = ('cat', 'fish')
        self.object.filter_words = ('taco', 'dog')
        self.assertTupleEqual(self.object._filter_words, self.expected)

    def test_filter_words_list_case(self):
        self.object.filter_words = ['cat', 'fish']
        self.object.filter_words = ['taco', 'dog']
        self.assertTupleEqual(self.object._filter_words, self.expected)

    def test_filter_words_list_case(self):
        self.object.filter_words = 'cat'
        self.object.filter_words = 'fish'
        self.object.filter_words = 'taco'
        self.object.filter_words = 'dog'
        self.assertTupleEqual(self.object._filter_words, self.expected)