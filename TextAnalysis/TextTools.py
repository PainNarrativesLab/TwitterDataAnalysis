import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

# Used for WordFilters
from ConstantsAndUtilities import Ignore
import string
import nltk
# from TextAnalysis.AnalysisErrors import *


class ICleaner(object):
    """
    Interface for text processing objects which take a word as input and
    either return True or False.

    A list of these will be passed in to objects like TweetTextWordBagMaker
    """
    def __init__(self):
        pass

    def clean(self, word):
        raise NotImplementedError


class URLCleaner(ICleaner):
    """
    Removes some urls
    TODO: Make this better
    """
    def __init__(self):
        ICleaner.__init__(self)

    def clean(self, word):
        if word[0:6] != '//t.co':
            return True
        else:
            return False


class UsernameCleaner(ICleaner):
    """
    Filters out usernames
    """
    def __init__(self):
        ICleaner.__init__(self)

    def clean(self, word):
        assert(type(word) is str)
        if word[0] != '@' and word[0:1] != '.@':
            return True
        else:
            return False


class NumeralCleaner(ICleaner):
    """
    Filters out all non-alphanumeric characters
    """
    def __init__(self):
        ICleaner.__init__(self)

    def clean(self, word):
        if type(word) is str:
            return word.isalpha()
        else:
            return False


class IModifier(object):
    """
    Interface for classes which modify words through stemming
    lemmatizing etc
    """
    def __init__(self):
        pass

    def process(self, word):
        raise NotImplementedError


class Lemmatizer(IModifier):
    """
    Wrapper on nltk.stem.WordNetLemmatizer for lemmatizing words
    """
    def __init__(self):
        IModifier.__init__(self)
        self.lemmatizer = nltk.stem.WordNetLemmatizer()

    def process(self, word):
        """
        Args:
            word: String to be lemmatized
        Returns:
            Lemmatized string
        """
        try:
            assert(type(word) is str)
            return self.lemmatizer.lemmatize(word)
        except Exception as e:
            print e


class PorterStemmer(IModifier):
    """
    Wrapper on nltk's porter-stemmer
    """

    def __init__(self):
        IModifier.__init__(self)
        self.stemmer = nltk.stem.PorterStemmer()

    def process(self, word):
        """
        Args:
            word: String to stem
        Returns:
            Porter stemmed string
        """
        try:
            assert(type(word) is str)
            return self.stemmer.stem(word)
        except Exception as e:
            print e


class WordBagMaker(object):
    """
        This takes a list of dictionaries containing tweetID and tweetText and processes the texts for bag of words type analyses.

    Before running the process command, all lists of strings to ignore should be loaded using add_to_ignorelist()

    Attributes:
        _cleaners: List of ICleaner objects
        masterbag: List containing all words
        _ignore: Tuple of strings to ignore while filtering
        tweet_tuples: List containing tuples with the structure (tweetID, [list of words in tweet])
    """



    def __init__(self):
        self._ignore = ()
        self._cleaners = []
        self.masterbag = []
        self.tweet_tuples = []

    def add_to_ignorelist(self, list_to_ignore):
        """
        Add a list of strings to the internally held tuple of strings to ignore in processing text
        Example:
            bagmaker = TweetTextWordBagMaker()
            bagmaker.add_to_ignorelist(ignore.get_list())
            bagmaker.add_to_ignorelist(nltk.corpus.stopwords.words('english'))
        
        Args:
            list_to_ignore: List of strings to ignore.
        """
        self._ignore = list(self._ignore)
        [self._ignore.append(i) for i in list_to_ignore]
        self._ignore = set(self._ignore)
        self._ignore = tuple(self._ignore)

    def add_to_cleaners(self, icleaner):
        """
        Adds an object which does cleaning to the que of cleaners which get
        called by _check_unwanted()
        Example:
            bagmaker.add_to_cleaners(URLCleaner())
            bagmaker.add_to_cleaners(UsernameCleaner())
            bagmaker.add_to_cleaners(NumeralCleaner())

        Args:
            :param icleaner: ICleaner inheriting object
        """
        assert(isinstance(icleaner, ICleaner))
        self._cleaners.append(icleaner)



    def _make_wordbag(self, text):
        """
        Takes a bunch of sentences and extracts all the words, makes them lowercase, and returns them in a list
        
        Args:
            text: String text to be word tokenized
        
        Returns:
            List of words, all lower case
        """
        return [word.lower() for sent in nltk.tokenize.sent_tokenize(text) for word in nltk.tokenize.word_tokenize(sent)]

    # def _filter_ignored_terms(self, wordlist):
    #     """
    #     Remove items that are in the ignore list
    #
    #     Args:
    #         wordlist: List of strings to be filtered
    #
    #     Returns:
    #         Filtered list
    #     """
    #     assert(len(self._ignore  > 0))
    #     return [w for w in wordlist if w not in self._ignore]

    def _check_unwanted(self, word):
        """
        Args:
            word: String to evaluate with ICleaner objects in _cleaners
        Returns:
            False if the the string is to be left out
            True if the string is to be included
        """
        for cleaner in self._cleaners:
            if cleaner.clean(word) is False:
                return False
        return True

    # def _filter_usernames(self, wordlist):
    #     """
    #     Gets rid of usernames by recognizing the @

    #
    #     """
    #     words = [w for w in wordlist if w[0] != '@']
    #     return words

    # def _filter_urls(self, wordlist):
    #     """
    #     Removes some urls
    #     TODO: Make this better
    #
    #     Args:
    #         wordlist: List of strings to be filtered
    #
    #     Returns:
    #         Filtered list
    #     """
    #     words = [w for w in wordlist if w[0:6] != '//t.co']
    #     return words


class TweetTextWordBagMaker(object):
    """
    This takes a list of dictionaries containing tweetID and tweetText and processes the texts for bag of words type analyses.

    Before running the process command, all lists of strings to ignore should be loaded using add_to_ignorelist()

    Attributes:
        _cleaners: List of ICleaner objects
        masterbag: List containing all words
        _ignore: Tuple of strings to ignore while filtering
        tweet_tuples: List containing tuples with the structure (tweetID, [list of words in tweet])
    """

        # def process(self, list_of_dicts):
    #     """
    #     Processes the tweet texts
    #     Most recent execution time 599.286342144 sec for 732683 tweets
    #     Moved stopwords filtration first: 891.928412914 for 732683 tweets
    #     Merged stopwords into ignore list: 234.204810858
    #     1 loops, best of 3: 14min 56s per loop
    #     TODO: Change order of execution for optimization
    #
    #     Args:
    #         list_of_dicts: List of dictionaries with keys tweetID and tweetText
    #     """
    #     for t in list_of_dicts:
    #         tweetid = t['tweetID']
    #         # process text
    #         words = self._make_wordbag(t['tweetText'])
    #         # words = self._filter_stopwords(words)
    #         words = self._filter_ignored_terms(words)
    #         words = self._filter_usernames(words)
    #         words = self._filter_urls(words)
    #         # process tuple
    #         tweet_tuple = (tweetid, words)
    #         self.tweet_tuples.append(tweet_tuple)
    #         self.masterbag += words

    def process(self, list_of_dicts):
        """
        Args:
            list_of_dicts: List of tweet dictionary objects with keys 'tweetID' and 'tweetText'

        Best time 225.85651803

        Example
        bagmaker = TweetTextWordBagMaker()
        bagmaker.add_to_ignorelist(ignore.get_list())
        bagmaker.add_to_ignorelist(nltk.corpus.stopwords.words('english'))

        """
        for t in list_of_dicts:
            tweetid = t['tweetID']
            # process text
            words = self._make_wordbag(t['tweetText'])
            words = [w for w in words if self._check_unwanted(w) and w not in self._ignore]
            # process tuple
            tweet_tuple = (tweetid, words)
            self.tweet_tuples.append(tweet_tuple)
            self.masterbag += words

    # def OLDprocess(self, list_of_dicts):
    #     for t in list(self.results):
    #         tweetid = t['tweetID']
    #         #process text
    #         words = [word for sent in sent_tokenize(t['tweetText']) for word in word_tokenize(sent)]
    #         words = [w.lower() for w in words]
    #         words = [w for w in words if w not in Ignore.punctuation]  #remove punctuation
    #         words = [w for w in words if w not in Ignore.fragments]  #remove fragments
    #         words = [w for w in words if w[0] != '@']  #Get rid of usernames
    #         words = [w for w in words if w[0:6] != '//t.co']  #Remove some urls
    #         words = [w for w in words if w not in Ignore.words['socialmediaterms']]  #Remove terms from social media
    #         words = [w for w in words if w not in nltk.corpus.stopwords.words('english')]  #Remove stopwords
    #         #process tuple
    #         tweet_tuple = (tweetid, words)
    #         self.tweet_tuples.append(tweet_tuple)
    #         self.masterbag += words



class TextFilters(object):
    """
    @deprecated
    DEPRECATED
    This has filters for removing various strings and string components.
    This really shouldn't be used

    """

    @staticmethod
    def remove_numerals(word_list):
        """
        Filters out all non-alphanumeric characters
        :param word_list:
        :return:
        """
        return [word for word in word_list if word.isalpha() is True]

    @staticmethod
    def remove_fragments(wordlist):
        """
        Filters string fragments from the list and returns the filtered list
        
        Args:
            wordlist: A list of words to have fragments removed from
        
        Returns:
            The filtered list
        """
        wordlist = [w for w in wordlist if w not in Ignore.fragments]  # remove fragments
        return wordlist

    @staticmethod
    def remove_punctuation(word_list):
        """
        Filters out punctuation from input list. Does not filter at the word level (e.g., will not remove the period in "cat.")
        
        Args:
            word_list: A list of strings to be filtered for list items which are punctuation marks.
        
        Returns:
            The filtered list
        """
        punctuation = string.punctuation
        punctuation = ['.', ',', '--', '?', ')', '(', ':', '\'', '"', '""', '-', '}', '{',
                             '://', '/"', '\xc2\xb2', '...', '???', '..']
        [punctuation.append(x) for x in string.punctuation]
        return [w for w in word_list if w not in punctuation]

    @staticmethod
    def filter_stopwords(wordlist):
        """
        Uses NLTK English stopwords corpus to remove stopwords.
        
        Args:
            wordlist: List of strings to be filtered
            
        Returns:
            Filtered list
        """
        return [w for w in wordlist if w not in nltk.corpus.stopwords.words('english')]

    @staticmethod
    def lemmatize(word_list):
        """
        Wrapper on nltk.stem.WordNetLemmatizer for lemmatizing words
        Args:
            word_list: List of words
        Returns:
            List of lemmatized words
        """

        try:
            assert(type(word_list) is list)
            lemmatizer = nltk.stem.WordNetLemmatizer()
            return [lemmatizer.lemmatize(w) for w in word_list]
        except Exception as e:
            print e

    @staticmethod
    def porter_stem(word_list):
        """
        Wrapper on porterstemmer

        Args:
            word_list: List of words
        Returns:
            Porter stemmed list
        """
        try:
            assert(type(word_list) is list)
            stemmer = nltk.stem.PorterStemmer()
            return [stemmer.stem(w) for w in word_list]
        except Exception as e:
            print e


class TextClassification(object):
    """
    Tools for classifying text
    """
    @staticmethod
    def tag_parts_of_speech(word_list):
        return nltk.pos_tag(word_list)


if __name__ == '__main__':
    pass
