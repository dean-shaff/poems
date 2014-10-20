from nltk.corpus import cmudict
from tools import Article_Stuff
from tools import Twitter_Tools
from tools import Text_Generator
from tools import InOut
import os 
import numpy.random as random
from tools import Stress_Poem

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

# harper = Text_Generator(text=harperleestring()).strip_punctuation()
# totaldic = cmudict.dict()
# pronunsplit = []
# pattern = []
# for word in harper.lower().split()[0:100]:
# 	try:
# 		pronunsplit.append(totaldic[word][0])
# 		stress = str()
# 		for phoneme in totaldic[word][0]:
# 			for stresser in stress_patterns:
# 				if stresser in phoneme:
# 					stress += stresser
# 		pattern.append([word,stress])
# 	except KeyError:
# 		pass

# print(pronunsplit[40:100])

# print(Text_Generator(text=harperleestring()).stress()[0:10])
word_stress_list = Text_Generator(text=harperleestring()).stress(bysentence=False)
# print(word_stress_list[0:10])
poems = Stress_Poem(harperleestring(),'1010101010',12,'1010').make_stresspoem_random()
print('\n')
print(poems['poem'])
# print(poems['last phonemes'])
# print("{}\n{}\n".format(poems[0],poems[1]))#,poems[2]))





		

















