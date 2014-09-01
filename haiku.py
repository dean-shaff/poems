from nltk_contrib.readability.textanalyzer import syllables_en
from nltk.corpus import cmudict, wordnet as wn
from nltk import word_tokenize
import numpy.random as random
import urllib2
from bs4 import BeautifulSoup as bs 
import time
from tweepy_tools import Twitter_Tools
from tweepy_tools import Article_Stuff


text = """
agreement with the Emirate of Abu Dhabi to create NYU Abu Dhabi 
is the outcome of a shared understanding of the essential 
roles and 
challenges of higher education in the 21st century: a common belief in 
value of a liberal arts education, concurrence on the benefits a research 
university brings to the society that sustains it, a conviction that interaction with 
new ideas and people who are different is valuable and necessary, and a commitment 
to educating students who are true citizens of the world. As the first comprehensive 
liberal arts and science campus in the Middle East to be operated abroad by a major American 
research university, NYU Abu Dhabi has been built on the following principles:
NYU Abu Dhabi is a research university with a fully integrated liberal arts and science 
college. It draws students from around the world, and prepares them for the challenges and opportunities of our interconnected world.
NYU Abu Dhabi equips students for leadership in all arenas of human endeavor.
 It fosters curiosity, creativity, and critical reflection. At NYUAD, students extend
  themselves and the frontiers of knowledge.
The residential life of students is central to the University's academic mission. Learning 
takes place across the campus, not only in classrooms, but also in residential houses, through 
participation in clubs and sports, during informal campus gatherings, and being engaged with the wider community.
NYU Abu Dhabi stimulates advanced research. The NYUAD Institute is a major research center. 
Research is integral to the undergraduate experience at NYU Abu Dhabi, and it will also drive 
the University's graduate programs.
NYU Abu Dhabi and NYU New York form the backbone of a fully connected global network university. 
As one of the two major hubs in the global network, NYUAD creates a unique capacity for faculty and students to access the assets of the entire university system.
NYU Abu Dhabi advances the city of Abu Dhabi as a magnetic center of ideas and human talent.
"""

text1 = str()
articles = Article_Stuff()
title_list = articles.gen_article_titles()
for i in title_list:
	text1 += i

print(text1)

def find_syll(word): #VERY specific to the howmanysyllables.com website
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
			
def make_syll(): #Now I can use both sources! From the internet from the nltk
	time1 = 0
	words = word_tokenize(text)
	wording = []
	for word in words:
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
	return wording

# word_list1 = make_syll()
# print(word_list1)

word_list2 = [['agreement ', 3], ['with ', 1], ['the ', 1], ['Emirate ', 3], ['of ', 1], ['Abu ', 2], ['Dhabi ', 2], ['to ', 1], ['create ', 2], ['NYU', 1], ['Abu ', 2], ['Dhabi', 2], ['is ', 1], ['the ', 1], ['outcome ', 2], ['of ', 1], ['a ', 1], ['shared ', 1], ['understanding ', 4], ['of ', 1], ['the ', 1], ['essential ', 3], ['roles ', 1], ['and ', 1], ['challenges ', 3], ['of ', 1], ['higher ', 2], ['education ', 4], ['in ', 1], ['the ', 1], ['century ', 3], ['a ', 1], ['common ', 2], ['belief ', 2], ['in ', 1], ['value ', 2], ['of ', 1], ['a ', 1], ['liberal ', 3], ['arts ', 1], ['education ', 4], ['concurrence ', 3], ['on ', 1], ['the ', 1], ['benefits ', 3], ['a ', 1], ['research ', 2], ['university ', 5], ['brings ', 1], ['to ', 1], ['the ', 1], ['society ', 4], ['that ', 1], ['sustains ', 2], ['it ', 1], ['a ', 1], ['conviction ', 3], ['that ', 1], ['interaction ', 4], ['with ', 1], ['new ', 1], ['ideas ', 3], ['and ', 1], ['people ', 2], ['who ', 1], ['are ', 1], ['different ', 3], ['is ', 1], ['valuable ', 4], ['and ', 1], ['necessary ', 4], ['and ', 1], ['a ', 1], ['commitment ', 3], ['to ', 1], ['educating ', 4], ['students ', 2], ['who ', 1], ['are ', 1], ['true ', 1], ['citizens ', 3], ['of ', 1], ['the ', 1], ['As ', 1], ['the ', 1], ['first ', 1], ['comprehensive ', 4], ['liberal ', 3], ['arts ', 1], ['and ', 1], ['science ', 2], ['campus ', 2], ['in ', 1], ['the ', 1], ['Middle ', 2], ['East ', 1], ['to ', 1], ['be ', 1], ['operated ', 4], ['abroad ', 2], ['by ', 1], ['a ', 1], ['major ', 2], ['American ', 4], ['research ', 2], ['university ', 5], ['NYU', 1], ['Abu ', 2], ['Dhabi', 2], ['has ', 1], ['been ', 1], ['built ', 1], ['on ', 1], ['the ', 1], ['following ', 3], ['principles ', 3], ['NYU', 1], ['Abu ', 2], ['Dhabi', 2], ['is ', 1], ['a ', 1], ['research ', 2], ['university ', 5], ['with ', 1], ['a ', 1], ['fully ', 2], ['integrated ', 4], ['liberal ', 3], ['arts ', 1], ['and ', 1], ['science ', 2], ['It ', 1], ['draws ', 1], ['students ', 2], ['from ', 1], ['around ', 2], ['the ', 1], ['world ', 1], ['and ', 1], ['prepares ', 2], ['them ', 1], ['for ', 1], ['the ', 1], ['challenges ', 3], ['and ', 1], ['opportunities ', 5], ['of ', 1], ['our ', 1], ['interconnected ', 5], ['NYU', 1], ['Abu ', 2], ['Dhabi', 2], ['equips ', 2], ['students ', 2], ['for ', 1], ['leadership ', 3], ['in ', 1], ['all ', 1], ['arenas ', 3], ['of ', 1], ['human ', 2], ['endeavor ', 3]]


# wordinglist1 = [['agreement ', 3], ['with ', 1], ['the ', 1], ['Emirate ', 3], ['of ', 1], ['Abu ', 2], ['to ', 1], ['create ', 2], ['Abu ', 2], ['is ', 1], ['the ', 1], ['outcome ', 2], ['of ', 1], ['a ', 1], ['shared ', 1], ['understanding ', 4], ['of ', 1], ['the ', 1], ['essential ', 3]]

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
		while int(syllables_en.count(line)) < int(i):
			line = str(make_line(i+1))
		poem = poem+line+'\n'

	while syllables_en.count(poem) != 17:
		poem = make_poem(wordlist)

	return poem 

# print(make_poem(word_list2))
