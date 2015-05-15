"""
This contains classes which calculate statistical properties of processed text
"""
import nltk


class Stats(object):
    def __init__(self, data):
        """
        Args:
            data: list of the strings to calc
        """
        assert(type(data) is list)
        self.data = data
        self.unique = sorted(set(data))


class WordFreq(Stats):
    """
    Tools for computing and plotting frequencies of word appearances using the nltk.FreqDist method
    """

    def __init__(self, word_list):
        """
        Args:
            word_list: list of words
        """
        assert(type(word_list) is list)
        Stats.__init__(self, word_list)
        self.freqDist = nltk.FreqDist(self.data)
        self.ranking = list(self.freqDist.keys())

    def topN(self, number_to_display):
        """
        Returns the N most common items in the dataset

        Args:
            number_to_display: The number to display
        """
        assert(type(number_to_display) is int)
        return self.ranking[0: number_to_display]

    def plot(self, number_to_display):
        """
        Displays a plot of the frequency distribution of item frequencies
        Args:
            number_to_display: The top n to display
        """
        assert(type(number_to_display) is int)
        self.freqDist.plot(number_to_display, cumulative=True)

    def compute_individual_word_freq(self):
        """
        Computes the frequency of individual words

        Returns:
            List of dictionaries with the keys 'word' and 'count'
        """
        fd = nltk.FreqDist()
        for word in self.data:
            fd.inc(word)
        results = []
        for w in fd.items():
            results.append({'word': w[0], 'count' : w[1]})
        return results
