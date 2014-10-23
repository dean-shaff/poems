 # -*- coding: ascii -*-
from tools import InOut
import nltk
from nltk_contrib.readability.textanalyzer import syllables_en
from nltk.tokenize.punkt import PunktWordTokenizer, PunktSentenceTokenizer
import numpy as np
import time 
import imp
from textblob import TextBlob
from textblob_aptagger import PerceptronTagger
import os
# blob = TextBlob("Simple is better than complex.", pos_tagger=PerceptronTagger())
# blob.tags
#=====================================================
text_dir = "{}/texts".format(os.getcwd())

list_not_allow = [
	'SYM', 'TO','$',"\'\'",'(',')',',','--','.',':','FW','LS','UH',"``"
]

list_pos = [["CC"],["CD"],["DT"],["EX"],["IN"],["JJ"],["JJR"],["JJS"],["MD"],
	["NN"],["NNP"],["NNPS"],["NNS"],["PDT"],["POS"],["PRP"],["PRP$"],["RB"],["RBR"],
	["RBS"],["RP"],["VB"],["VBD"],["VBG"],["VBN"],["VBP"],["VBZ"]] #,["WDT"],["WP"],["WRB"],["WP$"]]


def tag_text(filename,up_to,write_to_file=False):
	master_str = str()
	with InOut(text_dir):
		with open(filename,'r') as reader:
			for index, line in enumerate(reader):
				line = line.strip('\n')
				master_str += line
				if index == up_to:
					break
	t1 = time.time()
	blob = TextBlob(master_str, pos_tagger=PerceptronTagger())
	print("Time creating object: {}".format(time.time()-t1))
	t2 = time.time()
	blob_tagged_by_sentence = [[word[1] for word in sentence.tags if word[1] not in list_not_allow] for sentence in blob.sentences]
	print("Time creating tagged list: {}".format(time.time()-t2))
	if write_to_file:
		with InOut(text_dir):
			with open("token{}.py".format(filename.strip('.txt')),'w') as writer:
				writer.write("var1 = {}".format(str(blob_tagged_by_sentence)))
	else:
		pass
	return blob_tagged_by_sentence

filename = 'melville.txt'
melville_tagged = tag_text('melville.txt',10000)

def cond_prob(tagged_text,magic_range,index1,index2,p1,p2):
	"""
	tokenized_sentence_list is the list of sentences whose words have been tokenized and p.o.s. tagged.
	index1 is the index of A (in P(A|B))
	index2 is the index of B 
	p1 is the position of A in the sentence
	p2 is the position of B in the sentence 
	"""
	magic_range = list(magic_range)
	special_index = index1 #A
	special_index2 = index2 #B
	tokenized_sentence_list = tagged_text
	# foo = imp.load_source('tokentesttext', '{}/tokentesttext.py'.format(text_dir))
	# tokenized_sentence_list = foo.var1
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

def all_probs(write_to_file=False):
	master_prob = []
	master = []
	for h in xrange(0,7):
		position = []
		for i in xrange(0,len(list_pos)):
			A = []
			t1 = time.time()
			for j in xrange(0,len(list_pos)):
				A.append(cond_prob(melville_tagged,[10,25],i,j,h,h+1)) 
			print(time.time()-t1)
			position.append(A)
		master.append(position)
	if write_to_file:
		with InOut(text_dir):
			with open("prob{}.py".format(filename.strip('.txt')),'a') as writer:
				writer.write("var1 = {}".format(str(master)))
	else:
		return master

print(all_probs(write_to_file=True))

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
# dependent()
