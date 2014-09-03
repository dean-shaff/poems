from tools.article_stuff import Article_Stuff 
from nltk import word_tokenize
from bs4 import BeautifulSoup as bs 
import os
from nltk_contrib.readability.textanalyzer import syllables_en
import time 


class Text_Generator(Article_Stuff):
	def __init__(self, generate=False):
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
		text1 = str()
		os.chdir(self.tempdir)
		with open(self.title_filename, 'r') as writer:
			for line in writer:
				line = str(line)
				# print(line)
				text1 += line
		os.chdir(self.path_current)
		self.text = text1
			
	def make_syll(self, online=True): #Now I can use both sources! From the internet from the nltk
		"""
		This function takes a text, just a long string, and returns 
		a list of words with the number of syllables associated with it 
		attached. It also has a timing component, because the lookup process is often
		a bit lengthy
		This returns a list with words in their original order
		"""

		def find_syll(word): 
			"""
			This function calculates the number of syllables in a word 
			using the howmanysyllables.com website. 
			I've added an option to do it using the built in NLTK function,
			which doesn't work as well, but is substantially quicker. 
			"""
			if online:
				t1 = time.time()
				keyphrase = 'how many syllables in {}? '.format(word)
				if word.isalpha():
					url = 'http://www.howmanysyllables.com/words/{}'.format(word.lower())
				else:
					raise Exception	
				thing = urllib2.urlopen(url)
				data = thing.read()
				html_file = 'temp.html'
				with open(html_file,'w') as temp:
					temp.write(data)
				soup = bs(open(html_file))
				info = soup.get_text()
				word = ""
				t = 0
				for index, char in enumerate(info):
					word += char
					if keyphrase in word.lower(): 
						while t < 10: #arbitrary
							try:
								int(info[index+t])
								return {'syll':int(info[index+t]), 'timing':time.time()-t1} # 'syll' is the number of syllables
							except ValueError:
								pass
							t += 1
			elif not online:
				if word.isalpha():
					t1 = time.time()
					return {'syll':syllables_en.count(word), 'timing':time.time()-t1}

		time1 = 0
		words = word_tokenize(self.text)
		wording = []
		for word in words:
			if word.isalpha():
				word = word.strip('\n')
				result = find_syll(str(word).lower())
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
				if online:
					print(time1)
			

		return wording

