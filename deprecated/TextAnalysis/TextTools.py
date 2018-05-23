# Used for WordFilters
from ConstantsAndUtilities import *
import string
import nltk

#from nltk.replacers import RegexpReplacer

from TextAnalysis.AnalysisErrors import NgramError


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

    def process(self, word, **kwargs):
        raise NotImplementedError


class RegexpReplacer(IModifier):
    def __init__(self):
        pass

    def process(self, word, **kwargs):
        """
        Arguments:
            patterns: Replacement patterns
        """
        patterns = replacement_patterns
        compiled = [(re.compile(regex), repl) for (regex, repl) in patterns]
        s = text
        for (pattern, repl) in self.patterns:
            (s, count) = re.subn(pattern, repl, s)
        return s


class Lemmatizer(IModifier):
    """
    Wrapper on nltk.stem.WordNetLemmatizer for lemmatizing words
    """
    def __init__(self):
        IModifier.__init__(self)
        self.lemmatizer = nltk.stem.WordNetLemmatizer()

    def process(self, word, **kwargs):
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
            print(e)


class PorterStemmer(IModifier):
    """
    Wrapper on nltk's porter-stemmer
    """

    def __init__(self):
        IModifier.__init__(self)
        self.stemmer = nltk.stem.PorterStemmer()

    def process(self, word, **kwargs):
        """
        Executes the porter stem and returns the stemmed word
        Args:
            word: String to stem
        Returns:
            Porter stemmed string
        """
        try:
            assert(type(word) is str)
            return self.stemmer.stem(word)
        except Exception as e:
            print(e)


class WordBagMaker(object):
    """
    General class for taking something with strings and processing the text for bag of words type analyses.

    Before running the process command, all lists of strings to ignore should be loaded using add_to_ignorelist()

    Attributes:
        _cleaners: List of ICleaner objects
        masterbag: List containing all words
        _ignore: Tuple of strings to ignore while filtering
    """

    def __init__(self):
        self._ignore = ()
        self._cleaners = []
        self.masterbag = []

    def add_to_ignorelist(self, list_to_ignore):
        """
        Add a list of strings to the internally held tuple of strings to ignore in processing text
        Example:
            bagmaker = WordBagMaker()
            bagmaker.add_to_ignorelist(ignore.get_list())
            bagmaker.add_to_ignorelist(nltk.corpus.stopwords.words('english'))
            bagmaker.add_to_ignorelist(list(string.punctuation))
        
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

    def process(self, to_process):
        """
        Processes list of strings into a word bag stored in self.masterbag

        Args:
            :param to_process: List of strings to process
        """
        assert(isinstance(to_process, list))
        for t in to_process:
            # process text
            words = self._make_wordbag(t)
            words = [w for w in words if self._check_unwanted(w) and w not in self._ignore]
            self.masterbag += words

    def _make_wordbag(self, text):
        """
        Takes a bunch of sentences and extracts all the words, makes them lowercase, and returns them in a list
        
        Args:
            text: String text to be word tokenized
        
        Returns:
            List of words, all lower case
        """
        return [word.lower() for sent in nltk.tokenize.sent_tokenize(text) for word in nltk.tokenize.word_tokenize(sent)]

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


class TweetTextWordBagMaker(WordBagMaker):
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
        self.tweet_tuples = []
        WordBagMaker.__init__(self)

    def process(self, to_process):
        """
        Args:
            to_process: List of tweet dictionary objects with keys 'tweetID' and 'tweetText'

        Best time 225.85651803

        Example
        bagmaker = TweetTextWordBagMaker()
        bagmaker.add_to_ignorelist(ignore.get_list())
        bagmaker.add_to_ignorelist(nltk.corpus.stopwords.words('english'))
        """
        for t in to_process:
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
        # def process(self, list_of_dicts):
    #     """
    #     Processes the tweet texts
    #     Most recent execution time 599.286342144 sec for 732683 tweets
    #     Moved stopwords filtration first: 891.928412914 for 732683 tweets
    #     Merged stopwords into ignore list: 234.204810858
    #     1 loops, best of 3: 14min 56s per loop
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


class INgramFilter(object):
    """
    Interface for filters on ngrams
    """
    def __init__(self, **kwargs):
        pass

    def filter(self, collocation_finder):
        """
        Arguments:
            collocation_finder: Instance of nltk.collocations.AbstractCollocationFinder
        Returns:
            The collocation_finder after has been filtered
        """
        raise NotImplementedError


class CustomFilter(INgramFilter):
    """
    Wrapper for applying arbitrary filter to the collocation finder
    e.g., for getting where 'and' is at trigram[1] but not beginning or end: lambda w1, w2, w3: 'and' in (w1, w3)
    """

    def __init__(self):
        self.filter_function = lambda x: x
        INgramFilter.__init__(self)

    def set_filter(self, filter_function):
        self.filter_function = filter_function

    def filter(self, collocation_finder):
        """
        Arguments:
            collocation_finder: Instance of nltk.collocations.AbstractCollocationFinder
        """
        assert isinstance(collocation_finder, nltk.collocations.AbstractCollocationFinder)
        return collocation_finder.apply_ngram_filter(self.filter_function)


class WordFilter(INgramFilter):
    """
    Wrapper for filtering by specific strings
    Make sure to set filter_words before calling filter
    Attributes:
        _filter_words: Tuple holding words to filter by, can be set with string, tuple, or list
    """

    def __init__(self):
        self._filter_words = ()
        INgramFilter.__init__(self)

    @property
    def filter_words(self):
        return self._filter_words

    @filter_words.setter
    def filter_words(self, words):
        """
        adds words to the internally held tuple of filter_words
        Arguments:
            :param words: Tuple, list, or individual word to add to the filter words
        """
        self._filter_words = list(self._filter_words)
        if isinstance(words, list):
            self._filter_words += words
        elif isinstance(words, str):
            self._filter_words.append(words)
        elif isinstance(words, tuple):
            self._filter_words += list(words)
        self._filter_words = tuple(self._filter_words)

    def filter(self, collocation_finder):
        """
        Arguments:
            collocation_finder: Instance of nltk.collocations.AbstractCollocationFinder
        """
        assert isinstance(collocation_finder, nltk.collocations.AbstractCollocationFinder)
        return collocation_finder.apply_word_filter(lambda w: w in self.filter_words)


class NgramGetter(object):
    """
    Abstract parent class for extracting ngrams.

    Attributes:
        collocation_finder: One of the nltk's collocation finder tools (e.g., BigramCollocationFinder)
        top_likelihood_ratio:
        measurement_tool: One of nltk's measurement tools (e.g., nltk.collocations.BigramAssocMeasures)
        modifiers: IModifier instantiating tool for modifying the text before calculating ngrams
        ngrams: List of ngrams
        raw_freq: Frequency distribution of ngrams
        sorted_ngrams: List of tuples sorted by self.scored_ngrams
        top_pmi: Variable number of n-grams with the highest Pointwise Mutual Information (i.e., which occur together
        more often than would be expected)
        word_bag: List of text to process
    """

    def __init__(self):
        self.modifiers = []
        self.ngram_filters = []
        self.word_bag = []
        self.ngrams = []
        if not self.measurement_tool:
            raise NotImplementedError

    def add_modifier(self, iModifier):
        assert(isinstance(iModifier, IModifier))
        self.modifiers.append(iModifier)

    def _run_modifiers(self):
        """
        Calls the modifiers in sequence and stores the results back in word_bag
        """
        for modifier in self.modifiers:
            self.word_bag = [modifier.process(w) for w in self.word_bag]

    def add_filter(self, iNgramFilter):
        """
        Adds a filter to be run after the ngrams are created
        :param iNgramFilter:
        :return:
        """
        self.ngram_filters.append(iNgramFilter)

    def apply_filters(self):
        for ftr in self.ngram_filters:
            self.collocation_finder.apply_ngram_filter(ftr)

    def process(self, word_bag, min_freq=3, get_top=10, **kwargs):
        """
        Runs any modifiers (stemmers, lemmatizers, etc) on the list of terms and
        then extracts the ngrams

        Args:
            get_top: The cut off for ngrams to get stats for
            min_freq: Integer of minimum number of appearances of ngram to extract
            word_bag: List of strings to extract ngrams from. Should already be filtered.
        """
        raise NotImplementedError

    def _calculate_statistics(self, get_top=10, **kwargs):
        """
        Arguments:
            get_top: The cut off for ngrams to get stats for
        """
        self.topPMI = self.collocation_finder.nbest(self.measurement_tool.pmi, get_top)
        self.raw_freq = self.collocation_finder.score_ngrams(self.measurement_tool.raw_freq)
        self.sorted_ngrams = (ngram for ngram, score in self.raw_freq)
        self.top_likelihood_ratio = self.collocation_finder.nbest(self.measurement_tool.likelihood_ratio, get_top)


class BigramGetter(NgramGetter):
    """
    Extracts 2-grams from a word bag and calculates statistics
    Attributes:
        top_pmi: Variable number of n-grams with the highest Pointwise Mutual Information (i.e., which occur together
        more often than would be expected)
        top_likelihood_ratio:
        raw_freq: Frequency distribution of ngrams
        sorted_ngrams: List of tuples sorted by self.scored_ngrams
    """

    def __init__(self):
        self.measurement_tool = nltk.metrics.BigramAssocMeasures()
        NgramGetter.__init__(self)

    def process(self, word_bag, min_freq=3, get_top=10, **kwargs):
        """
        Arguments:
            word_bag: List of strings
        """
        assert(isinstance(word_bag, list))
        try:
            self._run_modifiers()
            self.collocation_finder = nltk.collocations.BigramCollocationFinder.from_words(self.word_bag)
            self.collocation_finder.apply_freq_filter(min_freq)
        except NgramError('finding collocations for bigram'):
            pass
        try:
            self._calculate_statistics(get_top)
        except NgramError('calculating statistics for bigram'):
            pass

    def _calculate_statistics(self, get_top=10, **kwargs):
        """
        A number of measures are available to score collocations or other associations.
        The arguments to measure functions are marginals of a contingency table,
        in the bigram case (n_ii, (n_ix, n_xi), n_xx):
                w1    ~w1
             ------ ------
         w2 | n_ii | n_oi | = n_xi
             ------ ------
        ~w2 | n_io | n_oo |
             ------ ------
             = n_ix        TOTAL = n_xx
        We test their calculation using some known values presented
        in Manning and Schutze's text and other papers.
        Student's t: examples from Manning and Schutze 5.3.2
        """
        NgramGetter._calculate_statistics(self, get_top)
        # self.measurement_tool.student_t()
        # self.measurement_tool.chi_sq()


class TrigramGetter(NgramGetter):
    """
        Extracts 3-grams from a word bag and calculates statistics
    """

    def __init__(self):
        self.measurement_tool = nltk.metrics.TrigramAssocMeasures()
        NgramGetter.__init__(self)

    def process(self, word_bag, min_freq=3, get_top=10, **kwargs):
        """
        Arguments:
            word_bag: List of strings
        """
        assert(isinstance(word_bag, list))
        try:
            self._run_modifiers()
            self.collocation_finder = nltk.collocations.TrigramCollocationFinder.from_words(self.word_bag)
            self.collocation_finder.apply_freq_filter(min_freq)
        except NgramError('finding collocations for trigram'):
            pass
        try:
            self._calculate_statistics(get_top)
        except NgramError('calculating statistics for trigram'):
            pass


class TextClassification(object):
    """
    Tools for classifying text
    """
    @staticmethod
    def tag_parts_of_speech(word_list):
        return nltk.pos_tag(word_list)

# ------------------------------------------------------------ deprecated ---------------------------------


class TextFilters(object):
    """
    @deprecated
    DEPRECATED
    This has filters for removing various strings and string components.
    This really shouldn't be used

    """


    @staticmethod
    @deprecated
    def remove_numerals(word_list):
        """
        DEPRECATED
        Filters out all non-alphanumeric characters
        :param word_list:
        :return:
        """
        return [word for word in word_list if word.isalpha() is True]


    @staticmethod
    @deprecated
    def remove_fragments(wordlist):
        """
        DEPRECATED
        Filters string fragments from the list and returns the filtered list

        Args:
            wordlist: A list of words to have fragments removed from

        Returns:
            The filtered list
        """
        wordlist = [w for w in wordlist if w not in Ignore.fragments]  # remove fragments
        return wordlist

    @staticmethod
    @deprecated
    def remove_punctuation(word_list):
        """
        DEPRECATED
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
    @deprecated
    def filter_stopwords(wordlist):
        """
        DEPRECATED
        Uses NLTK English stopwords corpus to remove stopwords.

        Args:
            wordlist: List of strings to be filtered

        Returns:
            Filtered list
        """
        return [w for w in wordlist if w not in nltk.corpus.stopwords.words('english')]

    @staticmethod
    @deprecated
    def lemmatize(word_list):
        """
        DEPRECATED
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
            print(e)

    @staticmethod
    @deprecated
    def porter_stem(word_list):
        """
        DEPRECATED
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
            print(e)

if __name__ == '__main__':
    pass
