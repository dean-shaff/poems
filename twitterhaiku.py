from tools import Article_Stuff
from tools import Twitter_Tools
from tools import Text_Generator
from tools import InOut
from tools import Haiku 
import os 
import time
import numpy

# word_list2 = [['agreement ', 3], ['with ', 1], ['the ', 1], ['Emirate ', 3], ['of ', 1], ['Abu ', 2], ['Dhabi ', 2], ['to ', 1], ['create ', 2], ['NYU', 1], ['Abu ', 2], ['Dhabi', 2], ['is ', 1], ['the ', 1], ['outcome ', 2], ['of ', 1], ['a ', 1], ['shared ', 1], ['understanding ', 4], ['of ', 1], ['the ', 1], ['essential ', 3], ['roles ', 1], ['and ', 1], ['challenges ', 3], ['of ', 1], ['higher ', 2], ['education ', 4], ['in ', 1], ['the ', 1], ['century ', 3], ['a ', 1], ['common ', 2], ['belief ', 2], ['in ', 1], ['value ', 2], ['of ', 1], ['a ', 1], ['liberal ', 3], ['arts ', 1], ['education ', 4], ['concurrence ', 3], ['on ', 1], ['the ', 1], ['benefits ', 3], ['a ', 1], ['research ', 2], ['university ', 5], ['brings ', 1], ['to ', 1], ['the ', 1], ['society ', 4], ['that ', 1], ['sustains ', 2], ['it ', 1], ['a ', 1], ['conviction ', 3], ['that ', 1], ['interaction ', 4], ['with ', 1], ['new ', 1], ['ideas ', 3], ['and ', 1], ['people ', 2], ['who ', 1], ['are ', 1], ['different ', 3], ['is ', 1], ['valuable ', 4], ['and ', 1], ['necessary ', 4], ['and ', 1], ['a ', 1], ['commitment ', 3], ['to ', 1], ['educating ', 4], ['students ', 2], ['who ', 1], ['are ', 1], ['true ', 1], ['citizens ', 3], ['of ', 1], ['the ', 1], ['As ', 1], ['the ', 1], ['first ', 1], ['comprehensive ', 4], ['liberal ', 3], ['arts ', 1], ['and ', 1], ['science ', 2], ['campus ', 2], ['in ', 1], ['the ', 1], ['Middle ', 2], ['East ', 1], ['to ', 1], ['be ', 1], ['operated ', 4], ['abroad ', 2], ['by ', 1], ['a ', 1], ['major ', 2], ['American ', 4], ['research ', 2], ['university ', 5], ['NYU', 1], ['Abu ', 2], ['Dhabi', 2], ['has ', 1], ['been ', 1], ['built ', 1], ['on ', 1], ['the ', 1], ['following ', 3], ['principles ', 3], ['NYU', 1], ['Abu ', 2], ['Dhabi', 2], ['is ', 1], ['a ', 1], ['research ', 2], ['university ', 5], ['with ', 1], ['a ', 1], ['fully ', 2], ['integrated ', 4], ['liberal ', 3], ['arts ', 1], ['and ', 1], ['science ', 2], ['It ', 1], ['draws ', 1], ['students ', 2], ['from ', 1], ['around ', 2], ['the ', 1], ['world ', 1], ['and ', 1], ['prepares ', 2], ['them ', 1], ['for ', 1], ['the ', 1], ['challenges ', 3], ['and ', 1], ['opportunities ', 5], ['of ', 1], ['our ', 1], ['interconnected ', 5], ['NYU', 1], ['Abu ', 2], ['Dhabi', 2], ['equips ', 2], ['students ', 2], ['for ', 1], ['leadership ', 3], ['in ', 1], ['all ', 1], ['arenas ', 3], ['of ', 1], ['human ', 2], ['endeavor ', 3]]
# word_list3 = [['These ', 1], ['are ', 1], ['flowers ', 2], ['they ', 1], ['are ', 1], ['sculptures ', 2], ['nvicted ', 2], ['Cold ', 1], ['War ', 1], ['spy ', 1], ['John ', 1], ['Walker ', 2], ['dies ', 1], ['in ', 1], ['prison ', 2], ['Bad ', 1], ['goes ', 1], ['out ', 1], ['on ', 1], ['top ', 1], ['at ', 1], ['Primetime ', 3], ['Emmys ', 2], ['Saudi ', 2], ['terror ', 2], ['network ', 2], ['busted ', 2], ['government ', 3], ['says ', 1], ['Vivid ', 2], ['Sydney ', 2], ['lights ', 1], ['the ', 1], ['sails ', 1], ['ambodia ', 4], ['dark ', 1], ['past ', 1], ['on ', 1], ['show ', 1], ['Did ', 1], ['a ', 1], ['second ', 2], ['ISIS ', 2], ['militant ', 3], ['kill ', 1], ['James ', 1], ['Foley ', 2], ['Meet ', 1], ['Sobrr ', 1], ['the ', 1], ['app ', 1], ['Justin ', 2], ['Bieber ', 2], ['charged ', 1], ['with ', 1], ['assault ', 2], ['in ', 1], ['Canada ', 3], ['Tick ', 1], ['bite ', 1], ['almost ', 2], ['kills ', 1], ['Hampton ', 2], ['Iraqi ', 3], ['military ', 4], ['families ', 3], ['storm ', 1], ['parliament ', 3], ['Peak ', 1], ['rush ', 1], ['Paragliding ', 4], ['the ', 1], ['Swiss ', 1], ['Alps ', 1], ['an ', 1], ['meet ', 1], ['South ', 1], ['Sudan ', 2], ['challenge ', 2], ['Opinion ', 3], ['World ', 1], ['theme ', 1], ['parks ', 1], ['How ', 1], ['printing ', 2], ['is ', 1], ['changing ', 2], ['everything ', 3], ['KOI ', 1]]

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

# texter = Text_Generator(text=harperleestring()) #now I can syllabalize this 
texter = Text_Generator(generate=True,text=None)
word_list4 = texter.make_syll(python=True)
# print(Haiku(wordlist=word_list4).make_poem_ordered(diff_style=True))
def postit():
	t = 0
	while t < 15:
		t += 1
		make_me_a_haiku = Haiku(wordlist=word_list4)
		orderedpoem = make_me_a_haiku.make_poem_ordered(diff_style=True)
		print(orderedpoem)
		twitter = Twitter_Tools()
		twitter.get_authorization()
		twitter.make_post(orderedpoem)
		time.sleep(int(numpy.random.randint(low=600,high=4000)))
		print("Time done")
# postit()
