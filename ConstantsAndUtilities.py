import string


class Ignore(object):
    """
    This contains all the terms to be ignored from hashtags etc. It is inherited by other classes which do cleaning
    
    Attributes:
        words: Dictionary with categories of irrelevant terms as keys (placenames, smallwords, socialmediaterms, irrelevant)
        fragments: String fragments which should be filterd out
    """
    fragments = ["'s", "amp", '...', '//t.co', "'re'", "'m"]
    punctuation = string.punctuation
    words = {
    'placenames' : ['tn', 'nashville', 'memphis', 'tennessee', 'knoxville', 'fl', 'tx', 'sc', 'nc', 'co', 
                    'nyc', 'va', 'ga', 'twittoma', 'team243'],
    'smallwords' : ['no', 'be', 'my', 'the',  'like', 'in', 'i', 'a', 'you', 'is', 'of', 'and', 'it', 'to',
                    'this', 'so', 'for', 'on', 'up'], 
    'socialmediaterms' : ['hashtag', 'selfie', 'repost', 'nofilter', 'instagram', 'instamood', 'instalike',
                          'instadaily', 'picoftheday', 'photo', 'instapic', 'http', 'rt', 'mt'],
    'irrelevant' : ['recordstoreday', 'vinyl', 'naruto', 'bread' ]
    }

    def __init__(self):
        self.words = Ignore.words
        wordlist = []
        [wordlist.append(word) for k in Ignore.words.keys() for word in Ignore.words[k]]
        # [wordlist.append(w) for w in wl for wl in self.words.values()]
        self.wordtuple = tuple(wordlist)


    @staticmethod
    def iterable(self):
        """
        Iterable object for all the contents of the ignore list
        TODO Make a generator 
        """
        wordlist = []
        [wordlist.append(word) for k in words.keys() for word in words[k]]
        # [wordlist.append(w) for w in wl for wl in Ignore.words.values()]
        return wordlist

    def generator(self):
        """
        Generator which returns ignore words
        """
        pass
        # (word for word in self.wordtuple)
        #     yield word


    @staticmethod
    def get_list(self):
        """
        Returns a list of everything to ignore
        """
        wordlist = []
        [wordlist.append(w) for wl in self.words.values() for w in wl]
        wordlist += self.fragments
        wordlist += self.punctuation
        return wordlist
    
    
class Merge(object):
    """
    This holds terms which are to be merged together in analyzing graphs
    
    Attributes:
        toMerge: Dictionary with the master term as key and values to be merged in list as values
    """
    toMerge = {
        'Fibromyalgia' : ['fibro', 'fibromyalgia', 'fms', 'fm'],
            'CRPS' : ['crps', 'rsd'], 
            'ChronicFatigue' : ['chronicfatigue', 'chronicfatiguesyndrome', 'cfs', 'mecfs', 'cfsme', 'cfids', 
                                'myalgicencephalomyelitis', 'mcs' ], 
            'RheumatoidArthritis' : ['rheumatoid', 'ra', 'rheumatoidarthritis'],
            'Endometriosis' : ['endometriosis', 'endo']
        }

if __name__ == '__main__':
    pass
