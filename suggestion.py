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

filename = 'melville.txt'
t1 = time.time()
up_to1 = 7
sentence = sentence_processor(write_to_file=False,sentence="his name is John, but that's not") 
tagged = Sentence_Probability(filename, max_line=10000, write_to_file=False,load_tot_prob=True,load_tagged=True) 
probs = np.zeros(len(tagged.list_pos))
for i in xrange(len(tagged.list_pos)):
	# print(time.time() - t1)
	ran_word = tagged.random_word(i)
	sentence[0][up_to1-1] = (ran_word['word'],ran_word['pos'])
	probs[i] = tagged.calc_cumu_prob(sentence)
	# print(tagged.calc_cumu_prob(sentence))

index_max = np.where(probs == np.amax(probs))[0][0]

sentence_coherent = str()
for word_pair in sentence[0][0:up_to1-1]:
	sentence_coherent += word_pair[0] + " "

for i in xrange(100):
	ran_word1 = tagged.random_word(index_max)
	print(sentence_coherent + ran_word1['word'])
	raw_input(">> ")