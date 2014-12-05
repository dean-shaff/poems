 # -*- coding: ascii -*-
from tools import InOut
import nltk
from nltk_contrib.readability.textanalyzer import syllables_en
from nltk.tokenize.punkt import PunktWordTokenizer, PunktSentenceTokenizer
import numpy as np
import time 
#=====================================================
text_dir = '/home/dean/python_stuff_ubuntu/poems/texts'

list_not_allow = [
	'SYM', 'TO','$',"\'\'",'(',')',',','--','.',':','FW','LS','UH',"``"
]

dic_pos = {
	"CC":1, "CD":2, "DT":3,"EX":4,"FW":5,"IN":6,"JJ":7,"JJR":8,"JJS":9,"LS":10,"MD":11,
	"NN":12,"NNP":13,"NNPS":14,"NNS":15,"PDT":16,"POS":17,"PRP":18,"PRP$":19,"RB":20,"RBR":21,
	"RP":22,"UH":23,"VB":24,"VBD":25,"VBG":26,"VBN":27,"VBP":28,"VBZ":29,"WDT":30,"WP":31,"WRB":32,
	"RBS":33
}

list_pos = [["CC"],["CD"],["DT"],["EX"],["IN"],["JJ","JJR","JJS"],["MD"],
	["NN","NNP","NNPS","NNS"],["PDT"],["POS"],["PRP","PRP$"],["RB","RBR",
	"RBS"],["RP"],["VB","VBD","VBG","VBN","VBP","VBZ"]] #,["WDT"],["WP"],["WRB"],["WP$"]]


def make_sentence_matrix(filename,magic_num):
	t1 = time.time()
	master_str = str()
	with InOut(text_dir):
		with open(filename,'r') as reader:
			for line in reader:
				line = line.strip('\n')
				master_str += line
	print(time.time()-t1)
	sentences = PunktSentenceTokenizer().tokenize(master_str)
	sentences_tokenized_pos = [[word[1] for word in nltk.pos_tag(nltk.word_tokenize(sentence))] for sentence in sentences]
	sentence_no_break = []
	for sen in sentences_tokenized_pos:
		for pos in sen:
			sentence_no_break.append(pos)
	for pos in dic_pos.keys():
		dic_pos[pos] = 0.0
	for pos in sentence_no_break:
		if pos in dic_pos.keys():
			dic_pos[pos] += float(1.0/(float(len(sentence_no_break))))
	print(dic_pos)
	sentence_matrix = []
	def add_to_matrix():
		for sentence in sentences_tokenized_pos:
			sentence_num = []
			for index,pos_tag in enumerate(sentence):
				if pos_tag in list_not_allow:
					sentence.pop(index)
				elif pos_tag in dic_pos.keys():
					sentence_num.append(dic_pos[pos_tag])
			if len(sentence_matrix) < magic_num and len(sentence_num) == magic_num:
				sentence_matrix.append(sentence_num)
			elif len(sentence_matrix) >= magic_num:
				break
		return len(sentence_matrix)
	add_to_matrix()	
	sentence_matrix = np.array(sentence_matrix)
	w, v = np.linalg.eig(sentence_matrix)
	for i in xrange(0,magic_num):
		print((np.real(v[i])*10))
		print('\n')
	print(w)
	
def tokenize_text(filename,up_to):
	master_str = str()
	with InOut(text_dir):
		with open(filename,'r') as reader:
			for index, line in enumerate(reader):
				line = line.strip('\n')
				master_str += line
				if index == up_to:
					break
	sentences = PunktSentenceTokenizer().tokenize(master_str)
	sentences_tokenized_pos = [[word[1] for word in nltk.pos_tag(nltk.word_tokenize(sentence))] for sentence in sentences]
	for sentence in sentences_tokenized_pos:
		for index, word in enumerate(sentence):
			if word in list_not_allow:
				sentence.pop(index)
	return sentences_tokenized_pos


def cond_prob(tokenized_sentence_list,magic_num,index1,index2,p1,p2):
	"""
	tokenized_sentence_list is the list of sentences whose words have been tokenized.
	index1 is the index of A (in P(A|B))
	index2 is the index of B 
	p1 is the position of A in the sentence
	p2 is the position of B in the sentence 
	"""
	# magic_range = list(magic_range)
	special_index = index1 #A
	special_index2 = index2 #B
	def make_matrix(index_to_start):	
		for index1, sentence in enumerate(tokenized_sentence_list):
			if index1 <= index_to_start:
				pass
			else:
				if len(sentence) == magic_num:#magic_range[0] and len(sentence) <= magic_range[1]: 
					sentence_matrix = []
					freq_given_special = np.zeros(len(list_pos))
					for index_sen,word in enumerate(sentence):
						row = np.zeros(len(list_pos))
						#Below I'm constructing a vector that will allow me to calculate P(B|A)
						if index_sen == p1 and word in list_pos[special_index]: #At position p1 and the part of speech is the one we're testing. 
							for index, p_o_s in enumerate(list_pos):
								if sentence[p2] in p_o_s:
									freq_given_special[index] += 1
									break
						for index,pos in enumerate(list_pos):
							if word in pos:
								row[index] = int(1)
								sentence_matrix.append(row)
								break
							else:
								pass 
						if list(row) == list(np.zeros(len(list_pos))): #this is to ensure that the row gets appended no matter what
							sentence_matrix.append(row) 
					return (sentence_matrix,freq_given_special,index1)
				else:
					pass
	A = np.zeros(magic_num**2).reshape((magic_num,magic_num))
	B = np.zeros(magic_num)
	t = 1
	factor = float(3.0/4.0)
	while t < int(float(len(tokenized_sentence_list))*factor):
		stuff = make_matrix(t)
		matrix = stuff[0]
		freq_B_A = stuff[1]
		t = stuff[2]
		B = np.add(B,freq_B_A)
		A = np.add(A,matrix)
	#calculating P(A|B)
	row2 = A[p2]
	numerator = ((row2[special_index2])/np.sum(row2))*(B[special_index2]/np.sum(B))
	denominator = 0
	for i in xrange(0,len(B)):
		denominator += ((row2[i])/np.sum(A[p2]))*(B[i]/np.sum(B))

	return numerator/denominator

gazelle = 'testtext.txt'
t1 = time.time()
token_sen = tokenize_text(gazelle,1000)
print(time.time()-t1)
prob = cond_prob(token_sen,14,0,1,7,13)
print(prob)

