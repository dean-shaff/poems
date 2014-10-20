"""
Right now this only deals with large strings -- it can't discern between sentences.
I want to make it so this will work with sentences and strings. 
"""
from tools.article_stuff import Article_Stuff 
from nltk import word_tokenize
from bs4 import BeautifulSoup as bs 
import os
from nltk_contrib.readability.textanalyzer import syllables_en
from nltk.tokenize.punkt import PunktWordTokenizer, PunktSentenceTokenizer
import time 
from inoutsoft import InOut 
from nltk.corpus import cmudict
import string

class Text_Generator(Article_Stuff): 
	def __init__(self,generate=False,text=None):
		Article_Stuff.__init__(self)
		"""
		Upon initialization, this will either 
		1) read the article titles in the "article_titles.txt" file 
		and extract a string containing all the article titles.
		2) update the article_titles.txt file, and then extract a string 
		containing all the article titles. 
		"""
		if generate:
			articles = Article_Stuff()
			articles.gen_article_titles()
		else:
			pass
		if text == None: 
			text1 = str()
			with InOut(self.textdir):
				with open(self.title_filename, 'r') as reader:
					for line in reader:
						line = str(line)
						# print(line)
						text1 += line
			self.text = text1
		elif text != None:
			self.text = text
		self.dic = "mdic.txt"
		self.syll = "msyll.txt"

	def strip_punctuation(self,bysentence=False):
		"""
		strips the punctuation off the string that is self.text
		"""
		if bysentence:
			sentences = PunktSentenceTokenizer().tokenize(master_str)
			return [sentence.translate(string.maketrans("",""), string.punctuation) for sentence in sentences]
		elif not bysentence:	
			return self.text.translate(string.maketrans("",""), string.punctuation) 
	def stress(self,bysentence=False):
		"""
		tokenizes (I guess) the words in self.text by the stress pattern in each of the words.
		"""
		vowels = ['A','E','I','O','U']
		possible_stresses = ['1','2','0']
		totaldic = cmudict.dict()
		def gen_stress(stripped_text):
			stress_list = []
			for word in stripped_text.lower().split():
				try:
					stress = str()
					phonemized = totaldic[word][0]
					for phoneme in phonemized:
						for stresser in possible_stresses:
							if stresser in phoneme:
								stress += stresser
					for index, sound in enumerate(phonemized[len(phonemized)-3:len(phonemized)]):
						for vowel in vowels:
							if vowel in sound:
								stress_list.append([word,stress,[index, sound],phonemized])
				except KeyError:
					# print("{} couldn't be found".format(word))
					pass
			return stress_list

		if bysentence:
			sentences = PunktSentenceTokenizer().tokenize(master_str)
			stress_by_sentence = [sentence.translate(string.maketrans("",""), string.punctuation) for sentence in sentences]
			return [gen_stress(sentence) for sentence in stress_by_sentence]

		elif not bysentence:
			stress_total = self.text.translate(string.maketrans("",""), string.punctuation) 
			return gen_stress(stress_total)

	def make_syll(self,python=True):
		"""
		This function takes a text, just a long string, and returns 
		a list of words with the number of syllables associated with it 
		attached. It also has a timing component, because the lookup process is often
		a bit lengthy
		This returns a list with words in their original order.
		18/10/2014 Incorporating the above "find_syll" function into this one to make
		the dictionary lookup process quicker (it takes forever right now!)
		"""
		time1 = 0
		words = word_tokenize(self.text)
		wording = []
		if python:
			for word in words:
				if word.isalpha():
					word = word.strip('\n').strip('\n')
					word += " "	
					wording.append([word,syllables_en.count(word)])
		if not python:
			with InOut(self.textdir): #changes directory, and closes it outside of with statement
				with open(self.dic,'r') as dic, open(self.syll,'r') as syll: #where self.dic and self.syll are the files of the dictionary and hyphenated dictionaries respectively
					for word in words:
						t1 = time.time()
						if word.isalpha():
							word = word.strip('\n')
							word = word.strip('\n')						
							for index, (linedic, linesyll) in enumerate(zip(dic, syll)):
								# print(r"{}".format(linedic.lower().strip('\n')))
								if linedic.lower().strip('\r\n') == word.lower():
									num_syll = 1 #because the number of syllables will be one more than the number of plus signs
									for char in linesyll:
										if char == "+" or char == " ":
											num_syll += 1
									word = word + " "
									wording.append([word,num_syll])
									time1 += time.time()-t1
									print(time1)
								else:							
									pass
								wording.append([word,syllables_en.count(word)])
						dic.seek(0) #reset
						syll.seek(0)
		if len(wording) == 1:
			return wording[0] #in case you want to find syllable length of a single word	
		else:
			return wording

