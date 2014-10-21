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

word_stress_list = Text_Generator(text=harperleestring()).stress(bysentence=False)
# print(word_stress_list[0:10])
poem12 = Stress_Poem(harperleestring(),'1010101010',12,'1010').make_stresspoem_random()
poem2 = Stress_Poem(harperleestring(),'1010101010',2,'11').make_stresspoem_random()
# print(Text_Generator(text=poem12['poem']).stress(bysentence=False))
print(poem12['poem'])
print(poem2['poem'])





		

















