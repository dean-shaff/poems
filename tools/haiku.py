from nltk_contrib.readability.textanalyzer import syllables_en
from nltk.corpus import cmudict, wordnet as wn
from nltk import word_tokenize
from nltk.corpus import words
import numpy.random as random
import urllib2
from bs4 import BeautifulSoup as bs 
import time
from article_stuff import Article_Stuff
from twitter_tools import Twitter_Tools
from text_generator import Text_Generator
from inoutsoft import InOut
import os

class Haiku(Twitter_Tools):
	def __init__(self,wordlist):
		"""
		The wordlist is a list of words that are in the order they were found. Also, each word has an associated number of syllables.
		"""
		Twitter_Tools.__init__(self)
		self.wordlist = list(wordlist)
	def make_poem_ordered(self,diff_style=False):
		"""
		This function takes found text and extracts coherent strings of words that have the appropriate 
		number of syllables and creakes haikus. 
		The diff_style option creates a haiku whose first two lines are coherent and whose last is disparate.
		"""
		poem = str()
		length = len(self.wordlist)
		def make_simple_line(syll):
			size = int((2*length)/3)
			line = [str(),0]
			starting_point_list = random.choice(xrange(size),size=size,replace=False)
			index = 0
			random_num = starting_point_list[index]
			word = self.wordlist[random_num]
			while line[1] != syll:		
				if line[1] > syll:
					index += 1
					random_num = starting_point_list[index]
					word = self.wordlist[random_num]
					line = [str(),0]
				elif line[1] < syll:
					line[0] = line[0] + word[0]
					line[1] = line[1] + word[1]
					random_num += 1
					word = self.wordlist[random_num]
			
			try:
				syll_total = 0
				for wordpair in Text_Generator(text=line[0]).make_syll():
					syll_total += wordpair[1] 
				assert line[1] == syll and syll == syll_total, "Algorithm failed"
			except TypeError:
				pass
			
			return {'line':str(line[0]),'line_syll':int(line[1]),'place':random_num}

		def make_complex_line(syll1, syll2):
			size = int((2*length)/3)
			line = [str(),0]
			starting_point_list = random.choice(xrange(size),size=size,replace=False)
			index = 0
			random_num = starting_point_list[index]
			firstlineinfo = make_simple_line(syll1)
			firstline = firstlineinfo['line']
			firstlinesyll = firstlineinfo['line_syll']
			place = firstlineinfo['place']
			word = self.wordlist[place]
			while line[1] != syll2:
				if line[1] > syll2:
					firstlineinfo = make_simple_line(syll1)
					firstline = firstlineinfo['line']
					firstlinesyll = firstlineinfo['line_syll']
					place = firstlineinfo['place']
					word = self.wordlist[place]
					line = [str(),0]
				elif line[1] < syll2:
					line[0] = line[0] + word[0]
					line[1] = line[1] + word[1] 
					place += 1
					word = self.wordlist[place]
					
			return {'line':firstline + str(line[0]),'line_syll':firstlinesyll+int(line[1])}

		if not diff_style:
			syll_list = [5,7,5]
			for index in syll_list:
				line_info = make_simple_line(index)
				line = line_info['line']
				line_num = line_info['line_syll']
				poem = "{}\n".format(poem + line)		
			return poem

		elif diff_style:
			# This is a big 'ole mess!
			first2linesinfo = make_complex_line(5,7)
			first2lines = first2linesinfo['line']
			texter1 = Text_Generator(generate=False,text=first2lines)
			lines = texter1.make_syll(python=True)
			# print(lines)
			firstlinesfinal = str()
			syll_count = int()
			for i in xrange(0,len(lines)):
				word = lines[i]
				firstlinesfinal = firstlinesfinal + word[0]
				syll_count = syll_count + word[1]
				if syll_count == 5:
					firstlinesfinal = firstlinesfinal + '\n'

			last_line_info = make_simple_line(5)
			last_line = last_line_info['line']
			return firstlinesfinal + '\n' + last_line
	def make_poem_random(self): #self.wordlist should be a list that looks like what make_syll returns
		"""
		This function makes a haiku out of random words. 
		"""
		poem = str()
		syll_list = [5,7,5]

		def make_line(syll):
			integer_list = random.choice(xrange(len(self.wordlist)),size=len(self.wordlist),replace=False)
			line = [str(),0]		
			for j in xrange(len(integer_list)-2):
				i = integer_list[j]
				iplus1 = integer_list[j+1]
				item = self.wordlist[i]
				item_next = self.wordlist[iplus1]
				#below I try to get rid of duplicate words, and I try to prevent the use of 
				#non-English words. 
				if item[0] == item_next[0] or "CNN" in item[0] or item[0] not in words.words():
					pass
				if line[1] + item[1] > syll:
					pass
				elif line[1] + item[1] == syll:
					return {'line': str(line[0]+item[0]), 'line_syll': int(line[1]+item[1])}
				elif line[1] + item[1] < syll:
					line[0] += item[0]
					line[1] += item[1]

		#checking to see if the syllables are correct			
		for i in syll_list:
			line_info = make_line(i)
			line = line_info['line']
			line_num = line_info['line_syll']
			print(line_num)
			while line_num != i:
				print("Trying again...")
				line_info = make_line(i)
				line = line_info['line']
				line_num = line_info['line_syll']
			poem = poem+line+'\n'

		return poem 



