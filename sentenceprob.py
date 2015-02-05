# -*- coding: ascii -*-
"""
4/12/2014

To do: I'm tired of waiting around to generate the tagged list. I need to make the Sentence_Probability
methods support loading in the tagged list from a separate Python file. 

I need to clean up the confusing mess that is the "up_to" variable name. I make a property of 
the class, but its not the same as the one that I use in the calc_cumulative_prob method... 

7/12/2014

The fact that I have two methods that calculate the same thing (the cumulative probability) is ridiculous.
I need to make this work differently. There is no need to calculate the total cumulative probability array right now,
because I have no plans to be updating probabilities until I can figure out how to update probabilities. 

3/2/2015

Added some logging support. I think that this is critical to having some idea what the hell I'm doing in the future.

Made a fundamental change in the cond_prob_v2 method that makes it so it actually works. I can suggest words now (insane).

To do:
    - consolidate the mess that is the __init__ method of Sentence_Probability. I need to think of
    a good way of actually being able to load in something, or to calculate a new...
    - make it so I can load in a shit ton of texts and tag them and calculate probabilities.
     This would ultimately increase accuracy. CHECK - 3/2/2015
    - When you're calculating the cumulative probability at a high position (eg 7 or higher) in a provided sentence 
    (using the sentence_processor function) you start to lose accuracy because the probabilty starts to approach zero.
    This makes sense, but it would be cool if I could reindex every so often. If the user says to find the probability
    at postion 7 or something, I would START from position 6 or 7 in the self.total_prob array. CHECK 4/2/2015

solved some unicode encoding errors I think
"""

from tools import InOut
import nltk
from nltk_contrib.readability.textanalyzer import syllables_en
from nltk.tokenize.punkt import PunktWordTokenizer, PunktSentenceTokenizer
from sentenceprocessor import sentence_processor
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
import logging
# blob = TextBlob("Simple is better than complex.", pos_tagger=PerceptronTagger())
# blob.tags
#=====================================================
base_dir = os.getcwd()
text_dir = "{}/texts".format(base_dir)

list_not_allow = ['SYM', 'TO', '$', "\'\'",
                  '(', ')', ',', '--', '.', ':', 'FW', 'LS', 'UH', "``"]

list_pos = ["CC", "CD", "DT", "EX", "IN", "JJ", "JJR", "JJS", "MD",
            "NN", "NNP", "NNPS", "NNS", "PDT", "POS", "PRP", "PRP$", "RB", "RBR",
            "RBS", "RP", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]

log_dir = "{}/logs/{}"
# class Sentence_Processor(object):
"""
I want this to be able to take a random sentence and to read in a file up to a certain point.
Right now there is no need for this to be a class, but I think there might be more methods later. 
"""

class Sentence_Probability(object):
    """
    This class is for creating the 'training' data. If I want to compare another sentence to the probabilities generated by this
    use the sentence_processor function 
    """
    def __init__(self, filenames, max_line, write_to_file=False,**kwargs):
        """
        Here we assume that the file to be read in is in the "texts" subdirectory
        Also this is a big old shit show. 

        kwargs:
            load_tagged: if True, will load in the previously tagged list of words from a book.
            load_tot_prob: if True, will load in the total probability array from a tagged book. 
            ***I should make these development kwargs or something...*** 
        """
        logging.basicConfig(filename = log_dir.format(base_dir,"log_sentenceprob{}.log".format(time.strftime("%d-%m-%Y"))), level = logging.INFO)
        logging.info('Started: {} {}'.format(time.strftime("%H:%M:%S"), time.strftime("%d/%m/%Y")))
        self.text_dir = text_dir

        if isinstance(filenames, list):
            self.filenames = list(filenames)
        elif isinstance(filenames, basestring):
            self.filenames = []
            self.filenames.append(filenames)

        if isinstance(max_line, basestring) and max_line == 'max':
            self.max_line = None
        elif isinstance(max_line, int):
            self.max_line = max_line

        self.list_pos = list_pos
        master_str = str()
        if write_to_file:
            for filename in self.filenames:
                with InOut(text_dir):
                    with open(filename, 'r') as reader:
                        for index, line in enumerate(reader):
                            try:
                                line = line.strip('\n').decode('ascii')
                                master_str += line
                                if index == max_line:
                                    break
                            except UnicodeDecodeError:
                                print("unicode encoding error")
                                continue

            self.master_str = master_str

            t1 = time.time()            
            blob = TextBlob(self.master_str, pos_tagger=PerceptronTagger())
            print("Time creating object: {:.2f}".format(time.time() - t1))
            logging.info("Time creating object: {:.2f}".format(time.time() - t1))
        else:
            pass
        try:
            sys.path.append(os.path.abspath(text_dir))
            import prob
            if kwargs['load_tot_prob']:
                self.total_prob = np.asarray(prob.var_list,dtype=float)
                self.up_to_all_probs = self.total_prob.shape[2]
                # self.total_prob = imp.load_source('var_list', '{}/prob{}.py'.format(text_dir,self.filename.strip('.txt')))               
            elif kwargs['load_cumu_prob']:
                self.cumu_prob = prob.var_cumu
                # self.cumu_prob = imp.load_source('var_cumu', '{}/prob{}.py'.format(text_dir,self.filename.strip('.txt')))
        except (ImportError, KeyError, SyntaxError) as err: #syntaxerror to be removed later...
            logging.exception(err)

        try:
            sys.path.append(os.path.abspath(text_dir))
            t1 = time.time()
            import token1
            # import token.var_token
            if kwargs['load_tagged']:
                self.blob_tagged_by_sentence = token1.var_token
                self.sen_tag_pword = token1.var_ptoken #with the words as well as the pos tags.
                write_to_file = False  
                print("Time loading tagged list: {:.2f} seconds".format(time.time()-t1))
                logging.info("Time loading tagged list: {:.2f} seconds".format(time.time()-t1))
            elif not kwargs['load_tagged']:
                self.blob_tagged_by_sentence = [[word[1] for word in sentence.tags if word[1] not in list_not_allow] for sentence in blob.sentences]
                self.sen_tag_pword = [[word for word in sentence.tags if word[1] not in list_not_allow] for sentence in blob.sentences]
                print("Time creating tagged list: {:.2f}".format(time.time() - t1))
                logging.info("Time creating tagged list: {:.2f}".format(time.time() - t1))
        
        except (KeyError, ImportError) as err:
            logging.exception(err)
            t2 = time.time()
            self.blob_tagged_by_sentence = [[word[1] for word in sentence.tags if word[1] not in list_not_allow] for sentence in blob.sentences]
            self.sen_tag_pword = [[word for word in sentence.tags if word[1] not in list_not_allow] for sentence in blob.sentences]
            print("Time creating tagged list: {:.2f}".format(time.time() - t2))
      
        if write_to_file:
            with InOut(text_dir):
                with open("token1.py", 'w') as writer:
                    writer.write("var_token = {}\n".format(str(self.blob_tagged_by_sentence)))
                    writer.write("var_ptoken = {}".format(str(self.sen_tag_pword)))
        else:
            pass

    def graph_prob(self,t_step=None):
        """
        This function is a modified version of the image_plot function above.
        """
        try:
            if t_step != None and t_step > self.up_to_all_probs:
                print("Can't plot for a time step that doesn't exist")
            elif t_step == None:
                plt.ion()
                for i in xrange(self.up_to_all_probs):
                    self.image_plot(self.scale(self.total_prob[:,:,i]))
                    plt.show()
                    raw_input(">> ")
            elif t_step != None and t_step >= 0 and t_step < self.up_to_all_probs:
                self.image_plot(self.scale(self.total_prob[:,:,t_step]))
                plt.show()
        except AttributeError:
            print("You didn't call the all_probs method")

    def image_plot(self,array,**kwargs):
        """
        Automatically scales array you pass to it. 
        """
        try:
            if kwargs["log"]:
                array = self.scale(array,log=True)
            elif kwargs["sqrt"]:
                array = self.scale(array,sqrt=True)
            elif kwargs["exp"]:
                array = self.scale(array,sqrt=True)
        except KeyError:
            array = self.scale(array)
        plot_options = {'cmap':'gray','vmin':0,'vmax':256}
        array = np.asarray(array,dtype=float)
        fig1 = plt.figure(figsize=(16,9))
        ax1 = fig1.add_subplot(111)
        ax1.matshow(array,**plot_options)
        return ax1

    def scale(self,array,**kwargs):
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

    # @classmethod
    def cond_prob_v2(self, magic_range, indexA, indexB, pA, pB):
        """
        this is zero indexed (like Python, chump)
        this function calculates the conditional probability P(A|B) 
        eg "The probability of there being pos "NN" in position 2 given that there is "VB" in position 1."
        tokenized_sentence_list is the list of sentences whose words have been tokenized and p.o.s. tagged.
        indexA is the index of A (in P(A|B)) in the list_pos list
        indexB is the index of B 
        pA is the position of A in the sentence
        pB is the position of B in the sentence 
        pA > pB, or else this is nonsense. (and method won't work)
        magic_range specifies the maximum length of an allowed sentence. 
        """
        magic_range = magic_range
        tokenized_sentence_list = self.blob_tagged_by_sentence
        total_prob = 0
        cond_prob = 0
        for index1, sentence in enumerate(tokenized_sentence_list):
            if len(sentence)-1 >= pA and len(sentence) <= magic_range: # dont worry about pB, as pA is always greater. 
                # for index_sen, word in enumerate(sentence):
                # if sentence[pB] == list_pos[indexB] and sentence[pA] == list_pos[indexA]:
                #     cond_prob += 1.0

                if sentence[pB] == list_pos[indexB]:
                    total_prob += 1.0
                    if sentence[pA] == list_pos[indexA]:
                        cond_prob += 1.0
                    else:
                        continue
                else:
                    continue
                    # if index_sen == pB and word == list_pos[indexB]:
                    #     total_prob += 1.0
                    # else:
                    #     continue

                    # elif (index_sen == pB and word == list_pos[indexB] and
                    #         sentence[pA] == list_pos[indexA]): #index_sen + (pA - pB) == pA and 
                    #     cond_prob += 1.0

            else:
                pass
        # print("total prob: {}".format(total_prob))
        # print("cond_prob: {}".format(cond_prob))
        if cond_prob > total_prob:
            logging.info("conditional probability was higher than total probability. Something isn't working right.")
        try:
            return float(cond_prob / total_prob)
        except ZeroDivisionError:
            return 0.0

    def all_probs(self,up_to=7,write_to_file=False,**kwargs):
        """
        Returns the probability for every A (ie, every part of speech) given every B at each sentence position. 
        There is a len(list_pos) x len(list_pos) array at each position. The indexing is (B,A). 

        kwargs:
            magic_range: maximum sentence length to use. name is a little deprecated now. 
        """
        try:
            magic_range = kwargs["magic_range"]
            if magic_range < up_to:
                print("magic_range keyword can't be less than up_to. Defaulting to up_to")
                magic_range = up_to+1
        except KeyError:
            magic_range = up_to+1
        self.up_to_all_probs = int(up_to)
        master = np.zeros((len(list_pos),len(list_pos),self.up_to_all_probs),dtype=float)
        masterdict = []
        for h in xrange(0, up_to):
            # position = master[:,:,h] #no need to do this like this. Just use master 
            t1 = time.time()
            A = {}
            for i in xrange(0, len(list_pos)):
                # A2 = position[i] #the row
                for j in xrange(0, len(list_pos)):
                    prob = self.cond_prob_v2(magic_range, j, i, h+1, h) #probability of j given i. This gives (B,A) indexing instead of the other way around.
                    A["{},{}".format(list_pos[j],list_pos[i])] = prob
                    master[i,j,h] = prob
                    # A2[j] = prob
            print("Position {} to {} took {:.1f} sec".format(h,h+1,time.time()-t1))
            logging.info("Position {} to {} took {:.1f} sec".format(h,h+1,time.time()-t1))
            masterdict.append(A)
        self.total_prob = master
        if write_to_file:
            with InOut(self.text_dir):
                with open("prob.py", 'a') as writer:
                    writer.write("var_list = {}\n".format(str(list(master))))
                    writer.write("var_dic = {}\n".format(str(masterdict)))
            return {'list':master,'dict':masterdict}
        else:
            return {'list':master,'dict':masterdict}

    def calc_cumulative_prob(self,coordinates):
        """
        coordinates are the coordinates of the parts of speech in the list_pos list.
        I don't want to crowd this function up with a bunch of stuff - it has to run quick!
        """
        length = len(coordinates)
        if length > self.total_prob.shape[2]:
            print("You need to make sure that the number of coordinates is equal to or less than the depth of non cumulative array")
        else:
            prob = 1
            for i in xrange(length-1):
                if coordinates[i] == None or coordinates[i+1] == None:
                    continue
                else:
                    posB = int(coordinates[i])
                    posA = int(coordinates[i+1])
                    prob *= self.total_prob[posB,posA,i]
            return prob

    def calc_cumu_prob(self,sentence,**kwargs):
        """
        This function calculates the cumulative probability of a sentence that you supply it. 
        The sentence should be a list whose elements are a tuple -- (word, p_o_s)
        This is the one I want to use outside of the class. The one above is to used in the calc_cumulative_prob method.

        **kwargs:
            - position: The position in the sentence about which you want it to calculate the probability. 
            If position is in the middle of the sentence, then it will calculate probability using the 
            3 previous words (if available) and the 3 after the word (if available). If position is the last word,
            it will use 3 previous entries to calculate probability. 
        """
        first_chunk = 3
        second_chunk = 3
        length = len(sentence[0])
        # print(sentence[0])
        try:
            position = int(kwargs['position'])
            coord = [None for i in xrange(length)]
            coord2 = tuple([list_pos.index(word[1]) for word in sentence[0]])
            # print(coord2)
            if position > length-1:
                print("Position argument provided is bigger than length of sentence. Defaulting to last position.")
                position = len(sentence[0])-1
            else:
                pass

            if length <= first_chunk+second_chunk: #sentence isn't long enough for this positional business to matter.
                coord = coord2
            elif position < first_chunk:
                coord[0:position+first_chunk+1] = coord2[0:position+first_chunk+1]
            elif position > length - second_chunk:
                coord[position-second_chunk:length] = coord2[position-second_chunk:length]
            else:
                coord[position-first_chunk:position+second_chunk+1] = coord2[position-first_chunk:position+second_chunk+1]
        
        except KeyError:
            coord = tuple([list_pos.index(word[1]) for word in sentence[0]])

        try:
            if len(sentence[0]) != len(self.cumu_prob.shape):
                raise ValueError("The sentence doesn't have the right length")
            else:
                prob = self.cumu_prob[coord]
                return prob

        except AttributeError:
            # this means the cumu_prob variable doesn't exist -- it hasn't been loaded in or the method 
            # above hasn't been called. Cumulative probabilty thing is deprecated as of now. 
            # print(coord)
            if len(sentence[0]) > self.up_to_all_probs:
                # raise ValueError("The sentence doesn't have the right length")
                coord = coord[0:self.up_to_all_probs]
                prob = self.calc_cumulative_prob(coord)
                return prob
            else:
                prob = self.calc_cumulative_prob(coord)
                return prob

    def total_cumulative_prob(self, up_to_cumu=3, write_to_file=False):
        """
        assumes the all_probs method has already been called. (fix)
        max_val = initial up_to
        """
        up_to_cumu = int(up_to_cumu)
        dimension = [len(list_pos) for i in xrange(up_to_cumu)]
        master = np.zeros(len(list_pos)**up_to_cumu,dtype=float)
        coord = [0 for i in xrange(up_to_cumu)]
        for j in xrange(0,len(list_pos)**up_to_cumu):
            if j % 50000 == 0:
                print("Only {} iterations to go!".format(len(list_pos)**up_to_cumu - j))
            val = j 
            for power in range(up_to_cumu)[::-1]:
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

def sentence_processor(sentence):
    """
    Update 4/2/2015 - Based on the way I've been using this function 
    (just to read in a sentence and tag it) I see no reason to have all 
    the other functionality, like reading in files. 
    """
    master_str = sentence
    t1 = time.time()
    blob = TextBlob(master_str, pos_tagger=PerceptronTagger())
    tagged_by_sen = [[word for word in sentence.tags if word[1] not in list_not_allow] for sentence in blob.sentences]
    print("Time loading in sentence {:.2f}".format(time.time() - t1))
    return tagged_by_sen



# if __name__=="__main__":
#     filename = 'melville.txt'
#     up_to1 = 7
#     sentence = sentence_processor(write_to_file=False,sentence="he ate food in the house today.") 
#     tagged = Sentence_Probability(filename, max_line=10000, write_to_file=False,load_tagged=True,load_tot_prob=False) #note that I don't need to run "all_probs" method because I'm loading in the data. 
#     prob = tagged.all_probs(up_to=up_to1,write_to_file=True)
#     #all_probs != to cumu_prob. cumu_prob is incredibly intensive to calculate and really kind of unnecessary right now. 
#     # cumu_prob = tagged.total_cumulative_prob(up_to=up_to1,write_to_file=True)
#     print(tagged.calc_cumu_prob(sentence))

    # print(tagged.calc_cumu_prob(sentence))
    # prob_list = prob['list']
    # cumu = tagged.total_cumulative_prob(up_to=3)
  


