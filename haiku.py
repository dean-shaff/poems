from nltk_contrib.readability.textanalyzer import syllables_en
from nltk.corpus import cmudict, wordnet as wn
from nltk import word_tokenize
import numpy.random as random
import urllib2
from bs4 import BeautifulSoup as bs 
import time
from tools import Article_Stuff
from tools import Twitter_Tools
import os

title_filename = "article_titles.txt"
tempdir = '/home/dean/python_stuff_ubuntu/poems/temp'
path_current = '/home/dean/python_stuff_ubuntu/poems'

def make_text():
	text1 = str()
	articles = Article_Stuff()
	title_list = articles.gen_article_titles()
	for i in title_list:
		text1 += i
	# print(text1)
	return text1


def read_textfile():
	text1 = str()
	os.chdir(tempdir)
	with open(title_filename, 'r') as writer:
		for line in writer:
			line = str(line)
			# print(line)
			text1 += line

	# print(text1)
	os.chdir(path_current)
	return text1

#text1 = make_text()
text1 = read_textfile()
# print(u"{}".format(text1))

def find_syll(word): 
	"""
	This function calculates the number of syllables in a word 
	using the howmanysyllables.com website
	"""
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
					return {'syll':int(info[index+t]), 'time':time.time()-t1}
				except ValueError:
					pass
				t += 1
			
def make_syll(text): #Now I can use both sources! From the internet from the nltk
	"""
	This function takes a text, just a long string, and returns 
	a list of words with the number of syllables associated with it 
	attached. It also has a timing component, because the lookup process is often
	a bit lengthy
	"""
	time1 = 0
	words = word_tokenize(text)
	wording = []
	for word in words:
		try:
			if word.isalpha():
				word = word.strip('\n')
				result = find_syll(str(word).lower())
				if result == None:
					print("No results found online!")
					num = syllables_en.count(word)
					time = 1
					word += " "
					wording.append([word, num])
				else:
					num = result['syll']
					time = result['time']
					word += " "
					# num = syllables_en.count(word)
					wording.append([word, num])
				time1 += time
				print(time1)
		except socket.error:
			print("No connection")
			pass

	return wording

word_list1 = make_syll(text1)
print(word_list1)

word_list2 = [['agreement ', 3], ['with ', 1], ['the ', 1], ['Emirate ', 3], ['of ', 1], ['Abu ', 2], ['Dhabi ', 2], ['to ', 1], ['create ', 2], ['NYU', 1], ['Abu ', 2], ['Dhabi', 2], ['is ', 1], ['the ', 1], ['outcome ', 2], ['of ', 1], ['a ', 1], ['shared ', 1], ['understanding ', 4], ['of ', 1], ['the ', 1], ['essential ', 3], ['roles ', 1], ['and ', 1], ['challenges ', 3], ['of ', 1], ['higher ', 2], ['education ', 4], ['in ', 1], ['the ', 1], ['century ', 3], ['a ', 1], ['common ', 2], ['belief ', 2], ['in ', 1], ['value ', 2], ['of ', 1], ['a ', 1], ['liberal ', 3], ['arts ', 1], ['education ', 4], ['concurrence ', 3], ['on ', 1], ['the ', 1], ['benefits ', 3], ['a ', 1], ['research ', 2], ['university ', 5], ['brings ', 1], ['to ', 1], ['the ', 1], ['society ', 4], ['that ', 1], ['sustains ', 2], ['it ', 1], ['a ', 1], ['conviction ', 3], ['that ', 1], ['interaction ', 4], ['with ', 1], ['new ', 1], ['ideas ', 3], ['and ', 1], ['people ', 2], ['who ', 1], ['are ', 1], ['different ', 3], ['is ', 1], ['valuable ', 4], ['and ', 1], ['necessary ', 4], ['and ', 1], ['a ', 1], ['commitment ', 3], ['to ', 1], ['educating ', 4], ['students ', 2], ['who ', 1], ['are ', 1], ['true ', 1], ['citizens ', 3], ['of ', 1], ['the ', 1], ['As ', 1], ['the ', 1], ['first ', 1], ['comprehensive ', 4], ['liberal ', 3], ['arts ', 1], ['and ', 1], ['science ', 2], ['campus ', 2], ['in ', 1], ['the ', 1], ['Middle ', 2], ['East ', 1], ['to ', 1], ['be ', 1], ['operated ', 4], ['abroad ', 2], ['by ', 1], ['a ', 1], ['major ', 2], ['American ', 4], ['research ', 2], ['university ', 5], ['NYU', 1], ['Abu ', 2], ['Dhabi', 2], ['has ', 1], ['been ', 1], ['built ', 1], ['on ', 1], ['the ', 1], ['following ', 3], ['principles ', 3], ['NYU', 1], ['Abu ', 2], ['Dhabi', 2], ['is ', 1], ['a ', 1], ['research ', 2], ['university ', 5], ['with ', 1], ['a ', 1], ['fully ', 2], ['integrated ', 4], ['liberal ', 3], ['arts ', 1], ['and ', 1], ['science ', 2], ['It ', 1], ['draws ', 1], ['students ', 2], ['from ', 1], ['around ', 2], ['the ', 1], ['world ', 1], ['and ', 1], ['prepares ', 2], ['them ', 1], ['for ', 1], ['the ', 1], ['challenges ', 3], ['and ', 1], ['opportunities ', 5], ['of ', 1], ['our ', 1], ['interconnected ', 5], ['NYU', 1], ['Abu ', 2], ['Dhabi', 2], ['equips ', 2], ['students ', 2], ['for ', 1], ['leadership ', 3], ['in ', 1], ['all ', 1], ['arenas ', 3], ['of ', 1], ['human ', 2], ['endeavor ', 3]]
word_list3 = [['These ', 1], ['are ', 1], ['flowers ', 2], ['they ', 1], ['are ', 1], ['sculptures ', 2], ['nvicted ', 2], ['Cold ', 1], ['War ', 1], ['spy ', 1], ['John ', 1], ['Walker ', 2], ['dies ', 1], ['in ', 1], ['prison ', 2], ['Bad ', 1], ['goes ', 1], ['out ', 1], ['on ', 1], ['top ', 1], ['at ', 1], ['Primetime ', 3], ['Emmys ', 2], ['Saudi ', 2], ['terror ', 2], ['network ', 2], ['busted ', 2], ['government ', 3], ['says ', 1], ['Vivid ', 2], ['Sydney ', 2], ['lights ', 1], ['the ', 1], ['sails ', 1], ['ambodia ', 4], ['dark ', 1], ['past ', 1], ['on ', 1], ['show ', 1], ['Did ', 1], ['a ', 1], ['second ', 2], ['ISIS ', 2], ['militant ', 3], ['kill ', 1], ['James ', 1], ['Foley ', 2], ['Meet ', 1], ['Sobrr ', 1], ['the ', 1], ['app ', 1], ['Justin ', 2], ['Bieber ', 2], ['charged ', 1], ['with ', 1], ['assault ', 2], ['in ', 1], ['Canada ', 3], ['Tick ', 1], ['bite ', 1], ['almost ', 2], ['kills ', 1], ['Hampton ', 2], ['Iraqi ', 3], ['military ', 4], ['families ', 3], ['storm ', 1], ['parliament ', 3], ['Peak ', 1], ['rush ', 1], ['Paragliding ', 4], ['the ', 1], ['Swiss ', 1], ['Alps ', 1], ['an ', 1], ['meet ', 1], ['South ', 1], ['Sudan ', 2], ['challenge ', 2], ['Opinion ', 3], ['World ', 1], ['theme ', 1], ['parks ', 1], ['How ', 1], ['printing ', 2], ['is ', 1], ['changing ', 2], ['everything ', 3], ['KOI ', 1]]

def make_poem(wordlist): #wordlist should be a list that looks like what make_syll returns
	poem = str()
	wordlist = list(wordlist)
	syll_list = [5,7,5]

	def make_line(syll):
		integer_list = random.choice(xrange(len(wordlist)),size=len(wordlist),replace=False)
		line = [str(),0]		
		for j in xrange(len(integer_list)-2):
			i = integer_list[j]
			iplus1 = integer_list[j+1]
			item = wordlist[i]
			item_next = wordlist[iplus1]
			if item[0] == item_next[0]:
				pass
			if line[1] + item[1] > syll:
				pass
			elif line[1] + item[1] == syll:
				return {'line': str(line[0]), 'line_syll': int(line[1])}
			elif line[1] + item[1] < syll:
				line[0] += item[0]
				line[1] += item[1]

	#checking to see if the syllables are correct			
	for i in syll_list:
		line_info = make_line(i+1)
		line = line_info['line']
		line_num = line_info['line_syll']
		while line_num < int(i):
			line = str(make_line(i+1))
		poem = poem+line+'\n'

	return poem 

haiku = make_poem(word_list1)
print(haiku)

# twitter = Twitter_Tools()
# twitter.get_authorization()
# twitter.make_post(haiku)

# print(make_poem(word_list3))
