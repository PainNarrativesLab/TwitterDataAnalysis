"""
This contains classes which calculate statistical properties of processed text
"""
import nltk

class Stats:
	def __init__(self, data, param):
		"""
		Data should be a list
		param['numToDisplay'] governs how many results will be displayed
		
		"""
		self.numToDisplay = param['numToDisplay']
		self.data = data
		self.unique = sorted(set(data))
	
class WordFreq(Stats):
	"""
	Computes the frequencies of item appearances using the nltk.FreqDist method
	"""
	def __init__(self, data, param):
		Stats.__init__(self, data, param)
		self.freqDist = nltk.FreqDist(self.data)
		self.ranking = self.freqDist.keys()

	def topN(self, numToDisplay):
		"""
		Returns the N most common items in the dataset
		"""
		self.toDisplay = numToDisplay
		self.top = self.ranking[:self.toDisplay]
		return self.top
	
	def plot(self):
		"""
		Displays a plot of the frequency distribution of item frequencies
		"""
		self.freqDist.plot(self.numToDisplay, cumulative=True)
	