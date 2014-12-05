# -*- coding: ascii -*-
"""
4/12/2014

To do: I'm tired of waiting around to generate the tagged list. I need to make the Sentence_Probability
methods support loading in the tagged list from a separate Python file. 

I need to clean up the confusing mess that is the "up_to" variable name. I make a property of 
the class, but its not the same as the one that I use in the calc_cumulative_prob method... 
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
# blob = TextBlob("Simple is better than complex.", pos_tagger=PerceptronTagger())
# blob.tags
#=====================================================
text_dir = "{}/texts".format(os.getcwd())

list_not_allow = ['SYM', 'TO', '$', "\'\'",
                  '(', ')', ',', '--', '.', ':', 'FW', 'LS', 'UH', "``"]

list_pos = ["CC", "CD", "DT", "EX", "IN", "JJ", "JJR", "JJS", "MD",
            "NN", "NNP", "NNPS", "NNS", "PDT", "POS", "PRP", "PRP$", "RB", "RBR",
            "RBS", "RP", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]

filename = 'melville.txt'


# class Sentence_Processor(object):
"""
I want this to be able to take a random sentence and to read in a file up to a certain point.
Right now there is no need for this to be a class, but I think there might be more methods later. 
"""

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

class Sentence_Probability(object):

    def __init__(self, filename, max_line, write_to_file=False,**kwargs):
        self.text_dir = text_dir
        self.filename = filename
        self.max_line = max_line
        master_str = str()
        with InOut(text_dir):
            with open(filename, 'r') as reader:
                for index, line in enumerate(reader):
                    line = line.strip('\n')
                    master_str += line
                    if index == max_line:
                        break
        self.master_str = master_str
        t1 = time.time()            
        blob = TextBlob(master_str, pos_tagger=PerceptronTagger())
        print("Time creating object: {:.2f}".format(time.time() - t1))
        try:
            sys.path.append(os.path.abspath(text_dir))
            import probmelville
            if kwargs['load_tot_prob']:
                self.total_prob = probmelville.var_list
                # self.total_prob = imp.load_source('var_list', '{}/prob{}.py'.format(text_dir,self.filename.strip('.txt')))               
            elif kwargs['load_cumu_prob']:
                self.cumu_prob = probmelville.var_cumu
                # self.cumu_prob = imp.load_source('var_cumu', '{}/prob{}.py'.format(text_dir,self.filename.strip('.txt')))
        except (ImportError, KeyError, SyntaxError): #syntaxerror to be removed later...
            pass

        try:
            sys.path.append(os.path.abspath(text_dir))
            t1 = time.time()
            import tokenmelvile
            if kwargs['load_tagged']:
                self.blob_tagged_by_sentence = tokenmelvile.var_token
                write_to_file = False  
                print("Time loading tagged list: {} seconds".format(time.time()-t1))             
        except (KeyError, ImportError):
            t2 = time.time()
            self.blob_tagged_by_sentence = [[word[1] for word in sentence.tags if word[1] not in list_not_allow] for sentence in blob.sentences]
            self.sen_tag_pword = [[word for word in sentence.tags if word[1] not in list_not_allow] for sentence in blob.sentences]
            print("Time creating tagged list: {:.2f}".format(time.time() - t2))
            if write_to_file:
                with InOut(text_dir):
                    with open("token{}.py".format(filename.strip('.txt')), 'w') as writer:
                        writer.write(
                            "var_token = {}".format(str(self.blob_tagged_by_sentence)))
            else:
                pass


    @staticmethod
    def image_plot(array):
        """
        Assumes array is already scaled the way you want it to be displayed
        """
        plot_options = {'cmap':'gray','vmin':0,'vmax':256}
        array = np.asarray(array,dtype=float)
        fig1 = plt.figure(figsize=(16,9))
        ax1 = fig1.add_subplot(111)
        ax1.matshow(array,**plot_options)
        return ax1

    @staticmethod
    def scale(array,**kwargs):
        """
        assuming that the array has no complex numbers
        """
        try:
            if kwargs["log"]:
                array = np.log(np.absolute(array))
            elif kwargs["sqrt"]:
                array = np.sqrt(np.absolute(array))
            elif kwargs["exp"]:
                array = np.exp(array)
        except KeyError:
            pass
        if array.dtype == 'complex':    
            array = np.asarray(array,dtype=complex)
            return 256.*(np.absolute(array))/np.amax(np.fabs(np.absolute(array)))
        else:
            array = np.asarray(array,dtype=float)
            return 256.*(array)/np.amax(array)

    def cond_prob_v2(self, magic_range, indexA, indexB, p1, p2):
        """
        this function calculates the conditional probability P(A|B) 
        eg "The probability of there being pos "NN" in position 2 given that there is "VB" in position 1."
        tokenized_sentence_list is the list of sentences whose words have been tokenized and p.o.s. tagged.
        indexA is the index of A (in P(A|B)) in the list_pos list
        indexB is the index of B 
        p1 is the position of A in the sentence
        p2 is the position of B in the sentence 
        p1 > p2, or else this is nonsense. 
        magic_range is a tuple or list with the allowed sentence length. 
        """
        magic_range = list(magic_range)
        tokenized_sentence_list = self.blob_tagged_by_sentence
        total_prob = 0
        cond_prob = 0
        for index1, sentence in enumerate(tokenized_sentence_list):
            if len(sentence) >= magic_range[0] and len(sentence) <= magic_range[1]:
                for index_sen, word in enumerate(sentence):
                    if index_sen == p1 and word == list_pos[indexA]:
                        total_prob += 1.0
                    elif (index_sen == p2 and word == list_pos[indexB] and
                            index_sen + (p1 - p2) == p1 and sentence[p1] == list_pos[indexA]):
                        cond_prob += 1.0
            else:
                pass
        try:
            return float(cond_prob / total_prob)
        except ZeroDivisionError:
            return 0.0

    def all_probs(self,up_to=7,write_to_file=False):
        """
        Returns the probability for every A (ie, every part of speech) given every B at each sentence position. 
        There is a len(list_pos) x len(list_pos) array at each position. The indexing is (B,A). 
        """
        self.up_to = int(up_to)
        master = np.zeros((len(list_pos),len(list_pos),self.up_to),dtype=float)
        masterdict = []
        for h in xrange(0, up_to):
            position = master[:,:,h]
            t1 = time.time()
            A = {}
            for i in xrange(0, len(list_pos)):
                A2 = position[i] #the row
                for j in xrange(0, len(list_pos)):
                    prob = self.cond_prob_v2([10, 25], j, i, h, h+1) #probability of j given i. This gives (B,A) indexing instead of the other way around.
                    A["{},{}".format(list_pos[j],list_pos[i])] = prob
                    A2[j] = prob
            print("Position {} to {} took {:.1f} sec".format(h,h+1,time.time()-t1))
            masterdict.append(A)
        self.total_prob = master
        if write_to_file:
            with InOut(self.text_dir):
                with open("prob{}.py".format(self.filename.strip('.txt')), 'a') as writer:
                    writer.write("var_list = {}\n".format(str(master)))
                    writer.write("var_dic = {}\n".format(str(masterdict)))
            return {'list':master,'dict':masterdict}
        else:
            return {'list':master,'dict':masterdict}

    def calc_cumulative_prob(self,coordinates):
        """
        coordinates are the coordinates of the parts of speech in the list_pos list.
        This method is basically to be used by the total_cumulative_prob below.
        """
        length = len(coordinates)
        if length != self.total_prob.shape[2]:
            print("You need to make sure that the number of coordinates equals the depth of non cumulative array")
        else:
            prob = 1
            for i in xrange(length-1):
                posB = int(coordinates[i])
                posA = int(coordinates[i+1])
                prob *= self.total_prob[posB,posA,i]
            return prob

    def total_cumulative_prob(self, up_to=3, write_to_file=False):
        """
        assumes the all_probs method has already been called. (fix)
        max_val = initial up_to
        """
        up_to = int(up_to)
        dimension = [len(list_pos) for i in xrange(up_to)]
        master = np.zeros(len(list_pos)**up_to,dtype=float)
        coord = [0 for i in xrange(up_to)]
        for j in xrange(0,len(list_pos)**up_to):
            if j % 50000 == 0:
                print("Only {} iterations to go!".format(len(list_pos)**up_to - j))
            val = j 
            for power in range(up_to)[::-1]:
                coord[power] = val/(len(list_pos)**power)
                val = val%(len(list_pos)**power)
            master[j] = self.calc_cumulative_prob(coord[::-1])
        self.cumu_prob = master.reshape(dimension)
        if write_to_file:
            with InOut(self.text_dir):
                with open("prob{}.py".format(self.filename.strip('.txt')), 'a') as writer:
                    writer.write("var_cumu = {}\n".format(str(master.reshape(dimension))))

            return self.cumu_prob
        else:
            return self.cumu_prob

    def random_word(self,p_o_s):
        """
        p_o_s can either be an integer corresponding to the position in the list_pos list,
        or the name of the part of speech itself.
        """
        if isinstance(p_o_s, int):
            p_o_s = list_pos[p_o_s]
        elif isinstance(p_o_s, basestring):
            p_o_s = str(p_o_s)
        tot_sen = self.sen_tag_pword
        start_point = random.randint(0,(len(tot_sen)*3)/4)
        for index in xrange(start_point,len(tot_sen)-1):
            for word in tot_sen[index]:
                if word[1] == p_o_s:
                    return {'word': word[0], 'pos': word[1], 'index': list_pos.index(word[1])} 

    def calc_cumu_prob(self,sentence):
        """
        This function calculates the cumulative probability of a sentence that you supply it. 
        The sentence should be a list whose elements are a tuple -- (word, p_o_s)
        """
        try:
            if len(sentence[0]) != len(self.cumu_prob.shape):
                raise ValueError
        except AttributeError:
            print("You didn't call the total_cumulative_prob method! (Or load in the cumulative probability array)")
        coord = tuple([list_pos.index(word[1]) for word in sentence[0]])
        prob = self.cumu_prob[coord]
        return prob

    def graph_prob(self,t_step=None):
        """
        This function is a modified version of the image_plot function above.
        """
        try:
            if t_step != None and t_step > self.up_to:
                print("Can't plot for a time step that doesn't exist")
            elif t_step == None:
                plt.ion()
                for i in xrange(self.up_to):
                    self.image_plot(self.scale(self.total_prob[:,:,i]))
                    plt.show()
                    raw_input(">> ")
            elif t_step != None and t_step >= 0 and t_step < self.up_to:
                self.image_plot(self.scale(self.total_prob[:,:,t_step]))
                plt.show()
        except AttributeError:
            print("You didn't call the all_probs method")

if __name__=="__main__":
    up_to1 = 3
    sentence = sentence_processor(write_to_file=False,sentence="I ate sandwiches") 
    tagged = Sentence_Probability(filename, max_line=2000, write_to_file=False)
    # print(tagged.blob_tagged_by_sentence)
    prob = tagged.all_probs(up_to=up_to1,write_to_file=True)
    cumu_prob = tagged.total_cumulative_prob(up_to=up_to1,write_to_file=True)
    print(cumu_prob[10,10,10])
    print(tagged.calc_cumu_prob(sentence))
    # prob_list = prob['list']
    # cumu = tagged.total_cumulative_prob(up_to=3)
  


