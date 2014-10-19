"""
stress patterns: (1=primary, 2=secondary, 0=no stress)
"""
from nltk.corpus import cmudict
from tools import Article_Stuff
from tools import Twitter_Tools
from tools import Text_Generator
from tools import InOut
import os 
import numpy.random as random
from tools import StressPoem

stress_patterns = ['1','2','0']
home = os.path.expanduser("~")
text_dir = "{}/texts".format(os.getcwd())
def harperleestring():
	harper = "harperlee.txt"
	harperstr = str()
	with InOut(text_dir):
		with open(harper,'r') as reader:
			for line in reader:
				if line == '\n':
					pass
				else:
					harperstr += line.strip('\n')
	return harperstr

harper = Text_Generator(text=harperleestring()).strip_punctuation()
totaldic = cmudict.dict()
pronunsplit = []
pattern = []
for word in harper.lower().split()[0:100]:
	try:
		pronunsplit.append(totaldic[word][0])
		stress = str()
		for phoneme in totaldic[word][0]:
			for stresser in stress_patterns:
				if stresser in phoneme:
					stress += stresser
		pattern.append([word,stress])
	except KeyError:
		pass

# print(pronunsplit[40:100])

# print(Text_Generator(text=harperleestring()).stress()[0:10])

class StressPoem(Text_Generator):
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

	
# poem = StressPoem(harperleestring(),'101010',5).make_stresspoem_random()





		

















