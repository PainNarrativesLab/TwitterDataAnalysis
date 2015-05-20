import string


def deprecated(deprecated_function, *args, **kwargs):
    """
    Wrapper for deprecated functions which ensures that
    the user gets a warning that the function is deprecated
    when they call it.
    """
    import warnings
    from functools import wraps

    @wraps(deprecated_function)
    def wrapper(*args, **kwargs):
        warnings.filterwarnings('always')
        warnings.warn("deprecated", DeprecationWarning)
        deprecated_function(*args, **kwargs)
    return wrapper


class Ignore(object):
    """
    This contains all the terms to be ignored from hashtags etc. It is inherited by other classes which do cleaning
    
    Attributes:
        fragments: (Class attribute) String fragments which should be filtered out
        words: (Class attribute) Dictionary with categories of irrelevant terms as keys (placenames, smallwords, socialmediaterms, irrelevant)
        word_tuple: (Class attribute and instance attribute) Tuple with everything to ignore
    """
    fragments = ["'s", "amp", '...', '//t.co', "'re'", "'m"]
    punctuation = ['.', ',', '--', '?', ')', '(', ':', '\'', '"', '""', '-', '}', '{',
                   '://', '/"', '\xc2\xb2', '...', '???', '..']
    words = {
        'placenames': ('tn', 'nashville', 'memphis', 'tennessee', 'knoxville', 'fl', 'tx', 'sc', 'nc', 'co',
                       'nyc', 'va', 'ga', 'twittoma', 'team243'),
        'smallwords': ('no', 'be', 'my', 'the', 'like', 'in', 'i', 'a', 'you', 'is', 'of', 'and', 'it', 'to',
                       'this', 'so', 'for', 'on', 'up'),
        'socialmediaterms': ('hashtag', 'selfie', 'repost', 'nofilter',
                             'instagram', 'instamood', 'instalike',
                             'instadaily', 'picoftheday', 'photo', 'instapic',
                             'http', 'rt', 'mt'),
        'irrelevant': ('recordstoreday', 'vinyl', 'naruto', 'bread')
    }

    def __init__(self):
        self._construct()
        self.word_tuple = Ignore.word_tuple


    @staticmethod
    def iterable(self):
        """
        Unused / deprecated
        Iterable object for all the contents of the ignore list
        """
        raise NotImplementedError

    def generator(self):
        """
        Generator which returns ignore words
        Example:
            generator = Ignore.generator()
            next(generator)
        """
        for word in self.word_tuple:
            yield word

    @classmethod
    def get_list(cls):
        """
        Returns a list of everything to ignore
        """
        cls._construct()
        return list(cls.word_tuple)

    @classmethod
    def _construct(cls):
        """
        Constructs the list of things to ignore at the class level from
        various sources.
        Note: This uses the string built in list of punctuation
        """
        word_list = []
        word_list += cls.fragments
        word_list += cls.punctuation
        [word_list.append(x) for x in string.punctuation]
        [word_list.append(word) for k in Ignore.words.keys() for word in Ignore.words[k]]
        cls.word_tuple = tuple(word_list)


class Merge(object):
    """
    This holds terms which are to be merged together in analyzing graphs
    
    Attributes:
        toMerge: Dictionary with the master term as key and values to be merged in list as values
    """
    toMerge = {
        'Fibromyalgia': ['fibro', 'fibromyalgia', 'fms', 'fm'],
        'CRPS': ['crps', 'rsd'],
        'ChronicFatigue': ['chronicfatigue', 'chronicfatiguesyndrome', 'cfs', 'mecfs', 'cfsme', 'cfids',
                           'myalgicencephalomyelitis', 'mcs'],
        'RheumatoidArthritis': ['rheumatoid', 'ra', 'rheumatoidarthritis'],
        'Endometriosis': ['endometriosis', 'endo']
    }


if __name__ == '__main__':
    pass
