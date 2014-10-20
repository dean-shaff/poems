from nltk.corpus import cmudict
from article_stuff import Article_Stuff
from twitter_tools import Twitter_Tools
from text_generator import Text_Generator
from inoutsoft import InOut
import os 
import numpy.random as random
import time

class Stress_Poem(Text_Generator):
	"""
	1 = primary stress
	2 = secondary stress 
	0 = not stressed
	"""
	def __init__(self,source_text,stresspattern,linecount,rhymepattern):
		"""
		stresspattern should be a string that is a sequence of 1's and 0's. 
		rhymepattern should be a string that is also a sequence of integers, ie "1212" is an "abab" rhyme pattern
		linecount is the number of lines in the poem
		"""
		Text_Generator.__init__(self,text=source_text)
		self.text_w_stress = self.stress(bysentence=False)
		self.stresspattern = str(stresspattern)
		self.linecount = int(linecount)
		self.rhymepattern = rhymepattern
		assert self.linecount % len(self.rhymepattern) == 0, "Number of lines incompatible with rhyme pattern"
	def make_stresspoem_random(self):
		"""
		This function takes a string (stresspattern) with the desired stress pattern, expressed 
		as a series of 1's and 0's (1 meaning stress and 0 meaning unstressed)
		and returns a poem that has the number of syllables expressed in the list
		linecount. The number of lines will be equal to len(linecount).
		source_text is a string with the desired text.
		"""
		not_allowed = ['the','a','and','i']
		vowels = ['A','E','I','O','U']
		def make_line():
			integer_list = random.choice(xrange(len(self.text_w_stress)-1),size=len(self.text_w_stress)-1,replace=False)
			index = 0
			stress_created = str()
			line = str()
			last_phoneme = []
			total_phoneme = list()
			for i in xrange(len(self.text_w_stress)-1):
				random_word = self.text_w_stress[int(integer_list[index])]
				try:
					cond = stress_created + random_word[1] == self.stresspattern[0:len(stress_created + random_word[1])]
				except IndexError:
					index += 1
					pass
				if cond:
					# print(random_word[0],random_word[1],random_word[2],random_word[3])
					stress_created += random_word[1]
					line = line + random_word[0] + " "
					last_phoneme.append(random_word[2])
					total_phoneme.append(random_word[3])
					# print(line,stress_created,last_phoneme,total_phoneme)
					index += 1
				elif not cond:
					index += 1
			assert stress_created == self.stresspattern, "make_line() failed"
			return (line, stress_created, last_phoneme, total_phoneme)


		def make_rhymedict():
			rhymedict = dict()
			# cond1 = len(set(rhymedict.keys())) != len(set(self.rhymepattern))
			listrhyme = list(set(self.rhymepattern))
			while len(set(rhymedict.keys())) != len(set(self.rhymepattern)):
				for i in xrange(len(set(self.rhymepattern))):
					line = make_line()
					while line[0].split()[-1].lower() in not_allowed: #so I don't get the same end lines
						line = make_line()
					rhymedict[str(listrhyme[i])] = line[2][-1]
			return rhymedict

		poem = str()
		poem_last_phoneme = []
		
		def list_element_in_word(vector,word):
			for i in vector:
				if i in word:
					return True
				else:
					pass
			return False

		for i in xrange(self.linecount/len(self.rhymepattern)):
			rhymedict = make_rhymedict()
			stanza = str()
			stanza_last_phoneme = []
			for j in xrange(len(self.rhymepattern)):
				# t1 = time.time()
				line = make_line()
				# print(time.time()-t1)
				while line[2][-1][0] != rhymedict[self.rhymepattern[j]][0] and line[2][-1][1] != rhymedict[self.rhymepattern[j]][1]:
					line = make_line()
				stanza = stanza + line[0] +'\n'
				stanza_last_phoneme.append(line[2])
			poem = poem + stanza +'\n'
			poem_last_phoneme.append(stanza_last_phoneme[1])

		return {'poem':poem,'last phonemes':poem_last_phoneme}

		# 	for j in xrange(len(self.rhymepattern)):

		# 	poem = poem + line[0] + '\n'
		# 	poem_last_phoneme = poem_last_phoneme + line[2] + '\n'
		# 	poem_total_phoneme = poem_total_phoneme + str(line[3]) + '\n\n'
		# return (poem, poem_last_phoneme, poem_total_phoneme)





















