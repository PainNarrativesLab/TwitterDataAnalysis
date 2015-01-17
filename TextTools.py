
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import time

#Used for WordFilters
from ConstantsAndUtilities import Ignore
import string

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


class TweetTextWordBagMaker(object):
    """
    This takes a list of dictionaries containing tweetID and tweetText and processes the texts for bag of words type analyses.
    
    Before running the process command, all lists of strings to ignore should be loaded using add_to_ignorelist()
    
    Attributes:
        masterbag: List containing all words
        ignore: Tuple of strings to ignore through filtering
        tweet_tuples: List containing tuples with the structure (tweetID, [list of words in tweet])
    """
    def __init__(self):
        self.ignore = ()
        self.masterbag = [] #This will hold all words
        self.tweet_tuples = []
    
    def add_to_ignorelist(self, list_to_ignore):
        """
        Add a list of strings to the internally held tuple of strings to ignore in processing text
        
        Args:
            list_to_ignore: List of strings to ignore.
        """
        self.ignore = list(self.ignore)
        [self.ignore.append(i) for i in list_to_ignore]
        self.ignore = set(self.ignore)
        self.ignore = tuple(self.ignore)
    
    def process(self, list_of_dicts):
        for t in list_of_dicts:
            tweetid = t['tweetID']
            #process text
            words = self._make_wordbag(t['tweetText'])
            words = self._filter_ignored_terms(words)
            words = self._filter_usernames(words)
            words = self._filter_urls(words)
            words = self._filter_stopwords(words)
            #process tuple
            tweet_tuple = (tweetid, words)
            self.tweet_tuples.append(tweet_tuple)
            self.masterbag += words
            
    def OLDprocess(self, list_of_dicts):  
        for t in list(self.results):
            tweetid = t['tweetID']
            #process text
            words = [word for sent in sent_tokenize(t['tweetText']) for word in word_tokenize(sent)]
            words = [w.lower() for w in words]
            words = [w for w in words if w not in Ignore.punctuation]#remove punctuation
            words = [w for w in words if w not in Ignore.fragments]#remove fragments
            words = [w for w in words if w[0] != '@']#Get rid of usernames
            words = [w for w in words if w[0:6] != '//t.co'] #Remove some urls
            words = [w for w in words if w not in Ignore.words['socialmediaterms']] #Remove terms from social media
            words = [w for w in words if w not in nltk.corpus.stopwords.words('english')] #Remove stopwords
            #process tuple
            tweet_tuple = (tweetid, words)
            self.tweet_tuples.append(tweet_tuple)
            self.masterbag += words
    
    def _make_wordbag(self, text):
        """
        Takes a bunch of sentences and extracts all the words, makes them lowercase, and returns them in a list
        
        Args:
            text: String text to be word tokenized
        
        Returns:
            List of words, all lower case
        """
        bag = [word.lower() for sent in sent_tokenize(text) for word in word_tokenize(sent)]
        return bag

    def _filter_ignored_terms(self, wordlist):
        """
        Remove items that are in the ignore list
        
        Args:
            wordlist: List of strings to be filtered
            
        Returns:
            Filtered list
        """
        if len(self.ignore) == 0:
            pass
            # TODO Raise error message
            #raise
        words = [w for w in wordlist if w not in self.ignore]
        return words
    
    def _filter_usernames(self, wordlist):
        """
        Gets rid of usernames by recognizing the @
        TODO: Modify to recognize cases of .@username
        
        """
        words = [w for w in wordlist if w[0] != '@']
        return words
    
    def _filter_urls(self, wordlist):
        """
        Removes some urls
        TODO: Make this better
        
        Args:
            wordlist: List of strings to be filtered
            
        Returns:
            Filtered list
        """
        words = [w for w in wordlist if w[0:6] != '//t.co']
        return words
    
    def _filter_stopwords(self, wordlist):
        """
        Uses NLTK English stopwords corpus to remove stopwords
        
        Args:
            wordlist: List of strings to be filtered
            
        Returns:
            Filtered list
        """
        words = [w for w in wordlist if w not in nltk.corpus.stopwords.words('english')]
        return words

class WordFilters(object):
    """
    This has filters for removing various strings and string components.
    
    """
    
    @staticmethod
    def remove_fragments(wordlist):
        """
        Filters string fragments from the list and returns the filtered list
        
        Args:
            wordlist: A list of words to have fragments removed from
        
        Returns:
            The filtered list
        """
        wordlist = [w for w in wordlist if w not in Ignore.fragments]#remove fragments
        return wordlist

    @staticmethod 
    def remove_punctuation(wordlist):
        """
        Filters out punctuation from input list. Does not filter at the word level (e.g., will not remove the period in "cat.")
        
        Args:
            wordlist: A list of strings to be filtered for list items which are punctuation marks. 
        
        Returns:
            The filtered list
        """
        wordlist = [w for w in wordlist if w not in string.punctuation]#remove punctuation
        return wordlist
