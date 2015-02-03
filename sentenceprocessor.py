"""
The function sentence_processor takes a phrase or text file and does two things:
1) tokenizes the phrase/text file by sentence.
2) for each word in the tokenized sentence it also provides the part of speech.
It returns a list of lists. Each sub list represents a sentence. Each element of the sentence 
sublist is a tuple containing the word and it's corresponding part of speech. 
"""

from tools import InOut
import nltk
from nltk_contrib.readability.textanalyzer import syllables_en
from nltk.tokenize.punkt import PunktWordTokenizer, PunktSentenceTokenizer
import numpy as np
import numpy.random as random
import time
import imp
import sys
from textblob import TextBlob
from textblob_aptagger import PerceptronTagger
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


text_dir = "{}/texts".format(os.getcwd())

list_not_allow = ['SYM', 'TO', '$', "\'\'",
                  '(', ')', ',', '--', '.', ':', 'FW', 'LS', 'UH', "``"]

list_pos = ["CC", "CD", "DT", "EX", "IN", "JJ", "JJR", "JJS", "MD",
            "NN", "NNP", "NNPS", "NNS", "PDT", "POS", "PRP", "PRP$", "RB", "RBR",
            "RBS", "RP", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]


def sentence_processor(write_to_file=False, **kwargs):
    """
    file_info is a tuple or list containing the name of the file and the number of lines to read in.
    If the second element is 0 or None, then it reads the whole file.
    sentence is just a random string you pass to the function.
    """
    master_str = None
    try:
        filename = kwargs['file_info'][0]
        up_to = kwargs['file_info'][1]
        master_str = str()
        if up_to == 0 or up_to == None:
            with InOut(text_dir):
                with open(filename, 'r') as reader:
                    for index, line in enumerate(reader):
                        line = line.strip('\n')
                        master_str += line
        else:
             with InOut(text_dir):
                with open(filename, 'r') as reader:
                    for index, line in enumerate(reader):
                        line = line.strip('\n')
                        master_str += line
                        if index == up_to:
                            break
        master_str = master_str
    except KeyError:
        pass
    try:
        master_str = kwargs['sentence']
    except KeyError:
        pass
    if master_str == None:
        print("You didn't instantiate the class with anything!")

    t1 = time.time()
    blob = TextBlob(master_str, pos_tagger=PerceptronTagger())
    print("Time creating object: {:.2f}".format(time.time() - t1))
    t2 = time.time()
    #Note that here I take the entire word, instead of just the part of speach!
    tagged_by_sen = [[word for word in sentence.tags if word[1] not in list_not_allow] for sentence in blob.sentences]
    print("Time creating tagged list: {:.2f}".format(time.time() - t2))
    if write_to_file:
        with InOut(text_dir):
            with open("token.py", 'w') as writer:
                writer.write("var1 = {}".format(str(tagged_by_sen)))
        return tagged_by_sen
    else:
        return tagged_by_sen









