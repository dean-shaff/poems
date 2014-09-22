from tools.article_stuff import Article_Stuff 
from nltk import word_tokenize
from bs4 import BeautifulSoup as bs 
import os
from nltk_contrib.readability.textanalyzer import syllables_en
import time 
from tools.inoutsoft import InOut 


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
			with InOut(self.tempdir):
				with open(self.title_filename, 'r') as writer:
					for line in writer:
						line = str(line)
						# print(line)
						text1 += line
			self.text = text1
		elif text != None:
			self.text = text
		self.dic = "mdic.txt"
		self.syll = "msyll.txt"
		self.text_directory = "/home/dean/python_stuff_ubuntu/poems/texts"

	def find_syll(self,word,python=True): 
		"""
		I've added an option to do it using the built in NLTK function,
		which doesn't work as well, but is substantially quicker. 
		"""
		if python:
			if word.isalpha():
				t1 = time.time()
				return {'syll':syllables_en.count(word), 'timing':time.time()-t1}

		if not python:
			with InOut(self.text_directory): #changes directory, and closes it outside of with statement
				with open(self.dic,'r') as dic, open(self.syll) as syll: #where self.dic and self.syll are the files of the dictionary and hyphenated dictionaries respectively
					for index, (linedic, linesyll) in enumerate(zip(dic, syll)):
						# print(r"{}".format(linedic.lower().strip('\n')))
						t1 = time.time()
						if linedic.lower().strip('\r\n') == word.lower():
							num_syll = 1 #because the number of syllables will be one more than the number of plus signs
							for char in linesyll:
								if char == "+":
									num_syll += 1
							return {'syll':num_syll, 'timing':time.time()-t1}
						else:
							pass							
					print("Error: Couldn't find word")
					return {'syll':None, 'timing':time.time()-t1}

	def make_syll(self,python=True):
		"""
		This function takes a text, just a long string, and returns 
		a list of words with the number of syllables associated with it 
		attached. It also has a timing component, because the lookup process is often
		a bit lengthy
		This returns a list with words in their original order
		"""

		time1 = 0
		words = word_tokenize(self.text)
		wording = []
		for word in words:
			if word.isalpha():
				word = word.strip('\n')
				result = self.find_syll(str(word).lower(),python)
				if result == None:
					print("No results found online!")
					num = syllables_en.count(word)
					time2 = 1
					word += " "
					wording.append([word, num])
				else:
					num = result['syll']
					time2 = result['timing']
					word += " "
					# num = syllables_en.count(word)
					wording.append([word, num])
				time1 += time2
		if len(wording) == 1:
			return wording[0] #in case you want to find syllable length of a single word	
		else:
			return wording

