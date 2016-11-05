"""
This contains tools for doing calculations on sets of words (not graphs)
Moved to TextStats
"""
import nltk
from nltk import *

# def compute_frequency_of_words_in_bag(wordbag):
#     """
#     Computes the frequency of words
#     """
#     fd = nltk.FreqDist()
#     for word in wordbag:
#         fd.inc(word)
#     results = []
#     for w in fd.iteritems():
#         results.append({'word' : w[0], 'count' : w[1]})
#     return results
