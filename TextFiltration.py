import sys
import nltk, re, pprint, string
from nltk.collocations import *
import nltk.data
from nltk.tokenize import word_tokenize, regexp_tokenize
from replacers import RegexpReplacer
"""
This contains classes used for filtering words, sentences, ngrams, etc to be used in statistical analysis
"""

class Text:
	"""
	This is the parent class for text normalization functions
	Can be run on an individual record
	TODO Extend so can be ran on a record set [??]
	"""
	def __init__(self, text, settings):
		"""
		@param text: List of text
		@param settings: dictionary of booleans
		@type settings: C{dictionary}
		param['replaceContractions'] is True or False
		"""
		self.settings = settings
		self.text = text
		#lowercase all
		#self.text = [w.lower() for w in text]
		#replace contractions
		try:
			if settings['replaceContractions'] == True:
				replacer = RegexpReplacer()
				self.text = [replacer.replace(w) for w in self.text]
		except:
			print('failed to replace contractions')
			pass
		

	def displayText(self):
		"""
		Returns the list of altered text
		"""
		return self.text

class Sentences(Text):
	def __init__(self, text, settings):
		Text.__init__(self, text, settings)
		tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
		self.sentences = []
		for rec in self.text:
			self.sentences.extend(tokenizer.tokenize(rec))

class Words(Text):
	def __init__(self, text, settings):
		"""
		Parses out a list of words from the text.
		param['removePunctuation] is True/False. Governs whether to remove punctuation
		param['removeStops'] is True/False. Governs whether to remove stopwords
		"""
		#self.text = text
		Text.__init__(self, text, settings)
		self.extra_punctuation = ['.', ',', '--','?',')', '(', ':','\'','"', '""', '-','}','{', '://', '/"', '\xc2\xb2', '...', '???', '..']
		self.words = []
		try:
			try:
				if self.settings['removePunctuation'] == 'True':
					pattern = r'\w+|[^\w\s]+'
					#self.words.extend(regexp_tokenize(self.text, pattern))
					self.words.extend(word_tokenize(self.text))
					self.words = [w for w in self.words if w not in string.punctuation]
					self.words = [w for w in self.words if w not in self.extra_punctuation]
					self.words = [string.lower(w) for w in self.words]
					#print('Punctuation removed')
				else:
					self.words.extend(word_tokenize(self.text))
					self.words = [string.lower(w) for w in self.words]
					#print ('punctuation not removed')
			except:
				
				pass
			try:
				if self.settings['removeStops'] == 'True':
					from nltk.corpus import stopwords
					#english_stops = set(stopwords.words('english'))
					english_stops = stopwords.words('english')
					self.w_stop_words = self.words
					self.words = [word for word in self.words if word not in english_stops]
					#print('Removed stops')
			except:
				#print('stop words not removed')
				pass
			try:
				if self.settings['lemmatize'] == 'True':
					from nltk.stem import WordNetLemmatizer
					lemmatizer = WordNetLemmatizer()
					self.words = [lemmatizer.lemmatize(w) for w in self.words]
					#print('Lemmatized')
			except Exception:
				#print('Not lemmatized')
				pass
			try:
				if self.settings['porterStem'] == 'True':
					from nltk.stem import PorterStemmer
					stemmer = PorterStemmer()
					self.words = [stemmer.stem(w) for w in self.words]
					self.stems = self.words
					#print('Porter stemmed ')
			except:
				#print('Not porter stemmed')
				pass
			try:
				if self.settings['removeNumerals'] == 'True':
					#filters out all non alphabetical characters
					self.words = [word for word in self.words if word.isalpha() == True]
					#Filters any word composed only of digits
					#self.words = [word for word in self.words if word.isnumeric() == False]
					
					#numbers = [str(0), str(1), str(2), str(3), str(4), str(5), str(6), str(7), str(8), str(9)]
					#Check whether the word is an integer (non-string) and filter
					#self.words = [word for word in self.words if isinstance(word, int) == False]
					#Filter out string digits
					#self.words = [word for word in self.words if word not in string.digits]
					#print ('Removed numerals')
					#realwords = []
					#for w in self.words:
						#num = False
						#for d in w:
							###if d in string.digits:
								#num = True
								#exit
						#if num == False:
							#realwords.append(w)
					#self.words = realwords
			except:
				#print('Numerals not removed')
				pass
		
		except Exception, exc:
			sys.exit( "processing failed; %s" % str(exc) ) # give a error message
	
	def tag_parts_of_speech(self):
		self.words_pos = nltk.pos_tag(self.words)
	



class Ngrams(Words):
	"""
	Abstract parent class. Don't instantiate
	"""
	def __init__(self, text, param):
		self.settings = param
		self.text = text
		Words.__init__(self, text, param)
		self.bigram_measures = nltk.collocations.BigramAssocMeasures()
		self.trigram_measures = nltk.collocations.TrigramAssocMeasures()

class Bigrams(Ngrams):
	def __init__(self, text, param):
		Ngrams.__init__(self, text, param)
		finder = BigramCollocationFinder.from_words(self.words)
	# only bigrams that appear 3+ times
		finder.apply_freq_filter(3) 
	# return the 10 n-grams with the highest PMI (i.e., which occur together more often than would be expected)
		self.topPMI = finder.nbest(self.bigram_measures.pmi, 10)
		#self.topLR = finder.nbest(self.trigram_measures.likelihood_ratio, 10)

class Trigrams(Ngrams):
	def __init__(self, text, param):
		Ngrams.__init__(self, text, param)
		finder = TrigramCollocationFinder.from_words(self.words)
	# only bigrams that appear 3+ times
		finder.apply_freq_filter(3) 
	# return the 10 n-grams with the highest PMI (i.e., which occur together more often than would be expected)
		self.topPMI = finder.nbest(self.trigram_measures.pmi, 10)
		#self.topLR = finder.nbest(self.trigram_measures.likelihood_ratio, 10)

#
#class Lemmatized(Words):
#	def __init__(self, text, param):
#		Words.__init__(self, text, param)
#		from nltk.stem import WordNetLemmatizer
#		lemmatizer = WordNetLemmatizer()
#		self.lemmas = [lemmatizer.lemmatize(w) for w in self.words]
#	
#class PorterStemmed(Words):
#	"""
#	Implements a Porter Stemmer
#	"""
#	def __init__(self, text, param):
#		Words.__init__(self, text, param)
#		from nltk.stem import PorterStemmer
#		stemmer = PorterStemmer()
#		self.stems = [stemmer.stem(w) for w in self.words]

#		# Group bigrams by first word in bigram.
#		prefix_keys = collections.defaultdict(list)
#		for key, scores in scored:
#		   prefix_keys[key[0]].append((key[1], scores))
#
## Sort keyed bigrams by strongest association.                                  
#for key in prefix_keys:
#   prefix_keys[key].sort(key = lambda x: -x[1])

#class RegexpReplacer(object):
#	def __init__(self, patterns=replacement_patterns):
#		self.patterns = [(re.compile(regex), repl) for (regex, repl) in patterns]
#		def replace(self, text):
#			s = text
#			for (pattern, repl) in self.patterns:
#				(s, count) = re.subn(pattern, repl, s)
#				return s

#class NGramFinder(Text):
#	def __init__(self, text, param):
#		from nltk.collocations import BigramCollocationFinder
#		from nltk.metrics import BigramAssocMeasures
#		bcf = BigramCollocationFinder.from_words(words go here)
#		bcf.nbest(BigramAssocMeasures.likelihood_ratio, self.numGram)