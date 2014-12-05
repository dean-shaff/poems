 # -*- coding: ascii -*-
"""
Parts of speech test
"""
import os
import nltk
from tools import InOut, Text_Generator #now I can use with statement to move between directories!
import string
from nltk.tokenize.punkt import PunktWordTokenizer, PunktSentenceTokenizer
from nltk_contrib.readability.textanalyzer import syllables_en

#====================================

punctuation = ["\"\"","(",")",",","--",".",":",';']
punctuation1 = string.punctuation
punctuation2 = [char for char in punctuation1]
text_dir = "/home/dean/python_stuff_ubuntu/poems/texts"
file1 = "harperlee.txt"
file2 = "haiku.txt"

def list_test(teststring, list_of_strings):
	list_of_strings = list(list_of_strings)
	for i in list_of_strings:
		if teststring == i:
			return True 
		else:
			pass
	return False

def make_dict(text):
	text_tokenized = nltk.word_tokenize(text)
	text_pos = nltk.pos_tag(text_tokenized)
	# print(text_pos[0:20])
	noun_list = dict()
	for index in xrange(0,len(text_pos)-1):
		word_pair = text_pos[index]
		if word_pair[1] == 'NN' or word_pair[1] == 'NNS' or word_pair[1] == 'NNP' or word_pair[1] == 'NNPS':
			if noun_list.has_key(word_pair[0]) and list_test(text_pos[index+1][1],punctuation) == False:
				noun_list[word_pair[0]].append(text_pos[index+1][0]) #appending next element to dictionary
			elif not noun_list.has_key(word_pair[0]) and list_test(text_pos[index+1][1],punctuation) == False:
				noun_list[word_pair[0]] = [text_pos[index+1][0]]
	return noun_list

# print(make_dict(text1))

def make_sentence_dic(filename):
	"""
	This function assumes that you feed it a file_name.txt file with a bunch of text.
	It will tokenize it by sentence and then tokenize that by parts of speech. I'm trying 
	to recognize patterns in sentences. 
	It will return a ?dictionary? containing the sentence type? 
	"""
	master_str = str()
	with InOut(text_dir):
		with open(filename,'r') as reader:
			for line in reader:
				line = line.strip('\n')
				master_str += line
	sentences = PunktSentenceTokenizer().tokenize(master_str)
	sentences_by_word = [nltk.word_tokenize(sentence) for sentence in sentences]
	sentences_tokenized = [[word for word in nltk.pos_tag(nltk.word_tokenize(sentence))] for sentence in sentences]
	sentences_tokenized_pos = [[word[1] for word in nltk.pos_tag(nltk.word_tokenize(sentence))] for sentence in sentences]

	same_sentences = []

	for index1, sentence1 in enumerate(sentences_tokenized_pos):
		for index2, sentence2 in enumerate(sentences_tokenized_pos):
			if sentence1 == sentence2 and index1 != index2:
				print("success!")
				same_sentences.append(sentences_by_word[index1])

	print(same_sentences)
	return (sentences_tokenized_pos, sentences_tokenized)

def count_syll(word):
	if word.isalpha():
		return syllables_en.count(word)

def make_haiku_dic(filename):
	master_list = []
	with InOut(text_dir):
		with open(filename,'r') as reader:
			for index,line in enumerate(reader):
				master_list.append(line)

	poem_list = []
	for i in xrange(1,len(master_list)/4+2):
		index = 4*i
		poem = str()
		for j in xrange(index-4,index-1):
			poem += " {}".format(master_list[j].strip('\n'))
		poem_list.append(poem)		

	poem_list = [nltk.pos_tag(nltk.word_tokenize(haiku)) for haiku in poem_list]
	poem_list_pos = [[(word[1],count_syll(word[0])) for word in poem] for poem in poem_list]	

	print(poem_list_pos)

# print(Text_Generator(text='building').make_syll(python=False))

# make_haiku_dic(file2)
# make_sentence_dic(file1)
# print(make_sentence_dic(file1)[0])
# print(make_sentence_dic(file1)[1])


