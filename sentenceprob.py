 # -*- coding: ascii -*-
from tools import InOut
import nltk
from nltk_contrib.readability.textanalyzer import syllables_en
from nltk.tokenize.punkt import PunktWordTokenizer, PunktSentenceTokenizer
import numpy as np
import time 
import imp
#=====================================================
text_dir = '/home/dean/python_stuff_ubuntu/poems/texts'

list_not_allow = [
	'SYM', 'TO','$',"\'\'",'(',')',',','--','.',':','FW','LS','UH',"``"
]

list_pos = [["CC"],["CD"],["DT"],["EX"],["IN"],["JJ","JJR","JJS"],["MD"],
	["NN","NNP","NNPS","NNS"],["PDT"],["POS"],["PRP","PRP$"],["RB","RBR",
	"RBS"],["RP"],["VB","VBD","VBG","VBN","VBP","VBZ"]] #,["WDT"],["WP"],["WRB"],["WP$"]]


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
	with InOut(text_dir):
		with open("token.py".format(filename),'w') as writer:
			writer.write("var1 = {}".format(str(sentences_tokenized_pos)))
	return sentences_tokenized_pos

# tokenize_text('testtext.txt',8700)

def cond_prob(magic_range,index1,index2,p1,p2):
	"""
	tokenized_sentence_list is the list of sentences whose words have been tokenized, as read in from a text file.
	index1 is the index of A (in P(A|B))
	index2 is the index of B 
	p1 is the position of A in the sentence
	p2 is the position of B in the sentence 
	"""
	magic_range = list(magic_range)
	special_index = index1 #A
	special_index2 = index2 #B
	foo = imp.load_source('tokentesttext', '{}/tokentesttext.py'.format(text_dir))
	tokenized_sentence_list = foo.var1
	def make_matrix(index_to_start):	
		for index1, sentence in enumerate(tokenized_sentence_list):
			if index1 <= index_to_start:
				pass
			else:
				if len(sentence) >= magic_range[0] and len(sentence) <= magic_range[1]: 
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
					while len(sentence_matrix) < magic_range[1]:
						sentence_matrix.append(np.zeros(len(list_pos))) 
					return (sentence_matrix,freq_given_special,index1)
				else:
					pass
	A = np.zeros(magic_range[1]*len(list_pos)).reshape((magic_range[1],len(list_pos)))
	B = np.zeros(len(list_pos))
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
	# print(B)
	row2 = A[p2]
	# print(row2)
	numerator = ((row2[special_index2])/np.sum(row2))*(B[special_index2]/np.sum(B))
	denominator = 0
	for i in xrange(0,len(B)):
		denominator += ((row2[i])/np.sum(A[p2]))*(B[i]/np.sum(B))

	return numerator/denominator
def all_probs():
	gazelle = 'tokentesttext.txt'
	master_prob = []
	master = []
	for h in xrange(0,7):
		position = []
		for i in xrange(0,len(list_pos)):
			A = []
			t1 = time.time()
			for j in xrange(0,len(list_pos)):
				A.append(cond_prob([10,25],i,j,h,h+1)) #i is A, j is B. this is backwards. 
			print(time.time()-t1)
			print(A)
			position.append(A)
		master.append(position)

def independent():
	foo = imp.load_source('prob', '{}/prob.py'.format(text_dir))
	dic = {}
	for h in xrange(0,7):
		position = foo.var1[h]
		maxB = []
		max_index = []
		for B in position:
			maxB.append(max(B))
			max_index.append(B.index(max(B)))
		dic[str(h)] = (max(maxB),maxB.index(max(maxB)),max_index[maxB.index(max(maxB))]) #(maxprob,A,B)
		print(h, dic[str(h)], list_pos[dic[str(h)][1]], list_pos[dic[str(h)][2]])
	
	return dic 

def dependent():
	foo = imp.load_source('prob', '{}/prob.py'.format(text_dir))
	dic = {}
	new_B = 0
	for h in xrange(0,7):
		if h == 0:		
			position = foo.var1[h]
			maxB = []
			max_index = []
			for A in position:
				maxB.append(max(A))
				max_index.append(A.index(max(A)))
			new_B = maxB.index(max(maxB))
			dic[str(h)] = (max(maxB),maxB.index(max(maxB)),max_index[maxB.index(max(maxB))]) #(maxprob,A,B)
			print(h, dic[str(h)], list_pos[dic[str(h)][1]], list_pos[dic[str(h)][2]])
		else:
			print(new_B)
			position = foo.var1[h]
			special = [position[i][new_B] for i in xrange(0,len(position))]
			old_B = new_B
			new_B = special.index(max(special)) 
			dic[str(h)] = (max(special),new_B,old_B) #maxprob, A, B
			print(h, dic[str(h)], list_pos[dic[str(h)][1]], list_pos[dic[str(h)][2]])

	return dic 	
dependent()
