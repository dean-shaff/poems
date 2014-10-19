from nltk.corpus import cmudict
from article_stuff import Article_Stuff
from twitter_tools import Twitter_Tools
from text_generator import Text_Generator
from inoutsoft import InOut
import os 
import numpy.random as random

class Stress_Poem(Text_Generator):
	"""
	1 = primary stress
	2 = secondary stress 
	0 = not stressed
	"""
	def __init__(self,source_text,stresspattern,linecount):
		Text_Generator.__init__(self,text=source_text)
		self.text_w_stress = self.stress(bysentence=False)
		self.stresspattern = str(stresspattern)
		self.linecount = int(linecount)
	def make_stresspoem_random(self):
		"""
		This function takes a string (stresspattern) with the desired stress pattern, expressed 
		as a series of 1's and 0's (1 meaning stress and 0 meaning unstressed)
		and returns a poem that has the number of syllables expressed in the list
		linecount. The number of lines will be equal to len(linecount).
		source_text is a string with the desired text.
		"""
		def make_line():
			integer_list = random.choice(xrange(len(self.text_w_stress)-1),size=len(self.text_w_stress)-1,replace=False)
			index = 0
			stress_created = str()
			line = str()
			for i in xrange(len(self.text_w_stress)-1):
				random_word = self.text_w_stress[int(integer_list[index])]
				try:
					cond = stress_created + random_word[1] == self.stresspattern[0:len(stress_created + random_word[1])]
				except IndexError:
					index += 1
					pass
				if cond:
					stress_created += random_word[1]
					line = line + random_word[0] + " "
					index += 1
				elif not cond:
					index += 1
			return (line, stress_created)
		poem = str()
		for i in xrange(self.linecount):
			poem = poem + make_line()[0] + '\n'
		return poem
