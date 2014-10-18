from tools.article_stuff import Article_Stuff 
from nltk import word_tokenize
from bs4 import BeautifulSoup as bs 
import os
from nltk_contrib.readability.textanalyzer import syllables_en
import time 
from inoutsoft import InOut 

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

	# def find_syll(self,word,python=True): 
	# 	"""
	# 	I've added an option to do it using the built in NLTK function,
	# 	which doesn't work as well, but is substantially quicker. 
	# 	This will just find the number of syllables in a single word. 
	# 	"""
	# 	if python:
	# 		if word.isalpha():
	# 			t1 = time.time()
	# 			return {'syll':syllables_en.count(word), 'timing':time.time()-t1}

	# 	if not python:
	# 		with InOut(self.textdir): #changes directory, and closes it outside of with statement
	# 			with open(self.dic,'r') as dic, open(self.syll) as syll: #where self.dic and self.syll are the files of the dictionary and hyphenated dictionaries respectively
	# 				for index, (linedic, linesyll) in enumerate(zip(dic, syll)):
	# 					# print(r"{}".format(linedic.lower().strip('\n')))
	# 					t1 = time.time()
	# 					if linedic.lower().strip('\r\n') == word.lower():
	# 						num_syll = 1 #because the number of syllables will be one more than the number of plus signs
	# 						for char in linesyll:
	# 							if char == "+" or char == " ":
	# 								num_syll += 1
	# 						print("One word down!")
	# 						return {'syll':num_syll, 'timing':time.time()-t1}
	# 					else:							
	# 						pass
	# 				return {'syll':None, 'timing':time.time()-t1}

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
					word = word.strip('\n')
					if python:
						wording.append([word,syllables_en.count(word)])
		if not python:
			with InOut(self.textdir): #changes directory, and closes it outside of with statement
				with open(self.dic,'r') as dic, open(self.syll,'r') as syll: #where self.dic and self.syll are the files of the dictionary and hyphenated dictionaries respectively
					for word in words:
						t1 = time.time()
						if word.isalpha():						
							for index, (linedic, linesyll) in enumerate(zip(dic, syll)):
								# print(r"{}".format(linedic.lower().strip('\n')))
								if linedic.lower().strip('\r\n') == word.lower():
									num_syll = 1 #because the number of syllables will be one more than the number of plus signs
									for char in linesyll:
										if char == "+" or char == " ":
											num_syll += 1
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

