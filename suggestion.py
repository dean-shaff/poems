"""
3/2/2015
By some grace of Jesus on the cross this actually works. 

"""
from sentenceprob import Sentence_Probability
from sentenceprocessor import sentence_processor
import os 
import time 
import numpy as np
import time 
text_dir = "{}/texts".format(os.getcwd())

list_pos = ["CC", "CD", "DT", "EX", "IN", "JJ", "JJR", "JJS", "MD",
            "NN", "NNP", "NNPS", "NNS", "PDT", "POS", "PRP", "PRP$", "RB", "RBR",
            "RBS", "RP", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]

filenames = ['melville.txt','AustenPride.txt','DickensTaleofTwo.txt']
t1 = time.time()
up_to1 = 7
tagged = Sentence_Probability(filenames, max_line="max", write_to_file=False,load_tagged=True,load_tot_prob=True) 
# tagged.all_probs(up_to=20, write_to_file=True, magic_range=40)
# sentence = sentence_processor(write_to_file=False,sentence="My name is Dean and I like eat cheese.")
# print(tagged.calc_cumu_prob(sentence,position=4))

def word_suggestion(test_sentence, sentence_probability_object, **kwargs):

	tagged = sentence_probability_object	
	sentence = sentence_processor(write_to_file=False,sentence=test_sentence) 
	try:	
		position = int(kwargs['position'])
		if position > len(sentence[0]) - 1:
			raise ValueError("Position keyword longer than sentence!")
	except KeyError:
		position = len(sentence[0]) - 1

	probs = np.zeros(len(tagged.list_pos))
	for i in xrange(len(tagged.list_pos)):
		ran_word = tagged.random_word(i)
		sentence[0][position] = (ran_word['word'],ran_word['pos'])
		probs[i] = tagged.calc_cumu_prob(sentence,position=position)

	# below I build a list the most probable indices, in descending probability
	probs2 = np.copy(probs)
	max_indices = []
	for i in xrange(len(probs)-1):
		index_max = np.where(probs2 == np.amax(probs2))[0][0]
		max_indices.append((index_max, probs2[index_max], list_pos[index_max]))
		probs2[index_max] = 0

	first_half = str()
	second_half = str()

	for word_pair in sentence[0][0:position]:
		first_half += word_pair[0] + " "

	if position != len(sentence[0]) - 1:
		for word_pair in sentence[0][position+1:len(sentence[0])-1]:
			second_half += word_pair[0] + " "
	else:
		pass

	for i in xrange(10):
		ran_word1 = tagged.random_word(max_indices[i][0])
		print("{}**{}** {} {}".format(first_half,ran_word1['word'],second_half, max_indices[i][2]))
		# print(first_half + ran_word1['word'] + " " + second_half + " " + max_indices[i][2])
		raw_input(">> ")

word_suggestion("I was walking down the street last Tuesday but then this girl saw me and I said hold up", tagged, position=4)







