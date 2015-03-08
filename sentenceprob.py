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

26/2/2015

I'm trying to construct a sentence model from the inputted text. This means that I go through all the sentences 
in a book/text and find the "most probable" sentence. 

4/3/2015

pos, or p.o.s. = part of speech. 

I'm trying to make a random word generator that generates words but weighted by pos frequency in the 
given text. 

7/3/2015

I want to experiment with pickling the objects to make my life easier -- hopefully this would 
allow me to forgo the bullshit of writing to files and such. 

I also want to jump balls deep -- starting calculating probabilites like I do by pos but by individual word.
Lets stop messing around, son. THIS IS TOO SLOW. DUH OF COURSE 
"""

from tools import InOut
import nltk
from nltk_contrib.readability.textanalyzer import syllables_en
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.tokenize import RegexpTokenizer
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
#=====================================================
base_dir = os.getcwd()
text_dir = "{}/texts".format(base_dir)

list_not_allow = ['SYM', 'TO', '$', "\'\'",
                  '(', ')', ',', '--', '.', ':', 'FW', 'LS', 'UH', "``"]

list_pos = ["CC", "CD", "DT", "EX", "IN", "JJ", "JJR", "JJS", "MD",
            "NN", "NNP", "NNPS", "NNS", "PDT", "POS", "PRP", "PRP$", "RB", "RBR",
            "RBS", "RP", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ","WRB","WDT","WP","WP$"]

log_dir = "{}/logs/{}"


# class Prob_Tester(object):
#     """
#     eventually the goal is to incorporate this into the class below. 
#     """
#     def __init__(self, filenames):
#         """
#         This is assuming that you'll use the entire text file.  
#         """
#         if isinstance(filenames,list):
#             self.filenames = filenames
#         if isinstance(filenames, basestring):
#             self.filenames = [filenames]

#         self.text_dir = text_dir
#         self.master_str = self.build_master_str(self.filenames)
#         senttokenizer = PunktSentenceTokenizer()
#         wordtokenizer = RegexpTokenizer(r'\w+')
#         self.master_sen = senttokenizer.tokenize(self.master_str)
#         self.master_word = [word.lower().strip() for word in wordtokenizer.tokenize(self.master_str)]
#         self.unique_word = list(set(self.master_word))
#         self.num_words = len(self.unique_word)
#         self.tknbywrdsent = [[word.lower().strip() for word in wordtokenizer.tokenize(sent)] for sent in self.master_sen]

#     def calc_prob_single(self, max_length, wordA, wordB, positionA, positionB):
#         """
#         calculates probability of word A at position A given that word B is at position B.
#         """
#         totalB = 0.0
#         totalAgivenB = 0.0
#         # positionBarray = [sentence[positionB] for sentence in self.tknbywrdsent if len(sentence)-1 >= positionA and len(sentence) <= max_length:]
#         # positionAarray = [sentence[positionB] for sentence in self.tknbywrdsent if len(sentence)-1 >= positionA and len(sentence) <= max_length:]
#         # if wordB not in positionBarray:
#         #     return 0.0
#         # else:
#         #     totalB = float(positionBarray.count(wordB))

#         for sentence in self.tknbywrdsent:
#             if len(sentence)-1 >= positionA and len(sentence) <= max_length:
#                 if sentence[positionB] == wordB:
#                     totalB += 1.0 
#                     if sentence[positionA] == wordA:
#                         totalAgivenB += 1.0
#         try:
#             prob = np.float64(totalAgivenB/totalB)
#         except ZeroDivisionError:
#             prob = 0.0
#         return prob

#     def calc_prob_all(self, up_to, **kwargs):
#         """
#         carbon copy of the method in Sentence_Probability class.
#         """
#         max_length=25
#         self.up_to_all_probs = up_to
#         master = np.zeros((self.num_words,self.num_words,self.up_to_all_probs),dtype=float)
#         for h in xrange(0, up_to):
#             t1 = time.time()
#             for i in xrange(0, self.num_words):
#                 t2 = time.time()
#                 for j in xrange(0, self.num_words):
#                     prob = self.calc_prob_single(max_length, self.unique_word[j], self.unique_word[i], h+1, h) #probability of j given i. This gives (B,A) indexing instead of the other way around.
#                     master[i,j,h] = prob
#                 print("One row down, so many more to go! took {} seconds".format(time.time()-t2))
#             print("Position {} to {} took {} seconds!".format(h, h+1, time.time()-t1))

#         self.total_prob = master

#         return master 

#     def build_master_str(self,filenames):
#             master_str = str()
#             for filename in self.filenames:
#                 with InOut(text_dir):
#                     with open(filename, 'r') as reader:
#                         for index, line in enumerate(reader):
#                             try:
#                                 line = line.strip('\n').decode('ascii')
#                                 master_str += line
#                                 # if index == max_line:
#                                 #     break
#                             except UnicodeDecodeError:
#                                 print("unicode encoding error")
#                                 continue
#             t1 = time.time()            
#             # blob = TextBlob(master_str, pos_tagger=PerceptronTagger())
#             # print("Time creating object: {:.2f}".format(time.time() - t1))
#             # logging.info("Time creating object: {:.2f}".format(time.time() - t1))

#             return master_str



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
            pos_freq: if provided will calculate the frequency of each part of speech
            in the provided text 
        """
        logging.basicConfig(filename = log_dir.format(base_dir,"log_sentenceprob{}.log".format(time.strftime("%d-%m-%Y"))), level = logging.INFO)
        logging.info('Started: {} {}'.format(time.strftime("%H:%M:%S"), time.strftime("%d/%m/%Y")))
        self.text_dir = text_dir
        """Checking if filenames is a list of strings or just a string"""
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

        try:
            if kwargs['load_tagged']:
                pass
            elif not kwargs['load_tagged']:
                self.master_str, blob = self.build_master_str(self.filenames)
        except KeyError:
            self.master_str, blob = self.build_master_str(self.filenames)
        
        """total_prob is a big 3-D array containing all the combinations of probabilities of parts of 
            speech given all other parts of speech, at each position in the sentence."""
        try:
            sys.path.append(os.path.abspath(text_dir))
            if len(self.filenames) > 1:
                exec("import probmulti as prob")
            elif len(self.filenames) == 1:
                exec("import prob{} as prob".format(self.filenames[0].strip(".txt")))

            if kwargs['load_tot_prob']:
                t0 = time.time()
                self.total_prob = np.asarray(prob.var_list,dtype=float)
                self.up_to_all_probs = self.total_prob.shape[2]
                print("Time loading total probability array: {:.2f}".format(time.time()-t0))
                # self.total_prob = imp.load_source('var_list', '{}/prob{}.py'.format(text_dir,self.filename.strip('.txt')))               
            elif kwargs['load_cumu_prob']:
                self.cumu_prob = prob.var_cumu
                # self.cumu_prob = imp.load_source('var_cumu', '{}/prob{}.py'.format(text_dir,self.filename.strip('.txt')))
        except (ImportError, KeyError, SyntaxError) as err: #syntaxerror to be removed later...
            logging.exception(err)
        """Below I just load in the pos tagged list from a .py file. This is faster than generating it 
            every time you call the method. """
        try:
            sys.path.append(os.path.abspath(text_dir))
            t1 = time.time()
            if len(self.filenames) > 1:
                exec("import token1multi as token1")
            elif len(self.filenames) == 1:
                exec("import token1{} as token1".format(self.filenames[0].strip(".txt")))
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
                if len(self.filenames) > 1:
                    tokenfile = "token1multi.py"
                elif len(self.filenames) == 1:
                    tokenfile = "token1{}.py".format(self.filenames[0].strip(".txt"))
                with open(tokenfile, 'w') as writer:
                    writer.write("var_token = {}\n".format(str(self.blob_tagged_by_sentence)))
                    writer.write("var_ptoken = {}".format(str(self.sen_tag_pword)))
        else:
            pass

        """Below I create the pos frequency dictionary"""
        try:
            if kwargs['pos_freq']:
                pos_freq = {}
                total_words = 0 
                t3 = time.time()
                for pos in list_pos:
                    pos_freq[pos] = 1.0 
                for sentence in self.blob_tagged_by_sentence:
                    for pos in sentence:
                        try:
                            pos_freq[pos] += 1.0 
                            total_words += 1.0
                        except KeyError:
                            print("There are part of speech tags in self.blob_tagged_by_sentence that shouldn't be there, namely: "+pos)
                for pos in list_pos:
                    pos_freq[pos] = float(pos_freq[pos]/total_words)
                print("Time creating pos frequency dictionary: {:.2f}".format(time.time()-t3))
                self.total_words = total_words
                self.pos_freq = pos_freq
                self.cumu_pos_freq = self.pos_freq
                for i in xrange(1,len(self.list_pos)):
                    self.cumu_pos_freq[self.list_pos[i]] += self.cumu_pos_freq[self.list_pos[i-1]]
            else:
                pass 

        except KeyError:
            pass            

    def build_master_str(self,filenames):
        master_str = str()
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
        t1 = time.time()            
        blob = TextBlob(master_str, pos_tagger=PerceptronTagger())
        print("Time creating object: {:.2f}".format(time.time() - t1))
        logging.info("Time creating object: {:.2f}".format(time.time() - t1))

        return master_str, blob

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
        # magic_range = magic_range
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
                if len(self.filenames) == 1:
                    prob_file = "prob{}.py".format(self.filenames[0].strip(".txt"))
                elif len(self.filenames) > 1:
                    prob_file = "probmulti.py"
                with open(prob_file, 'a') as writer:
                    master_str = str(list(master))
                    master_str = master_str.replace("array(","")
                    master_str = master_str.replace(")","")
                    writer.write("var_list = {}\n".format(master_str))
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
        if len(sentence) == 1 and isinstance(sentence[0],list):
            sentence = sentence[0]
        if len(sentence) == 1 and isinstance(sentence[0],tuple):
            print("One word sentence: Returning 0.0")
            return 0.0
        elif len(sentence) != 1: 
            sentence = sentence 
        length = len(sentence)

        # print(sentence[0])
        try:
            position = int(kwargs['position'])
            coord = [None for i in xrange(length)]
            coord2 = tuple([list_pos.index(word[1]) for word in sentence])
            # print(coord2)
            if position > length-1:
                print("Position argument provided is bigger than length of sentence. Defaulting to last position.")
                position = len(sentence)-1
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
        
        except (KeyError,ValueError):
            coord = tuple([list_pos.index(word[1]) for word in sentence])

        try:
            if len(sentence) != len(self.cumu_prob.shape):
                raise ValueError("The sentence doesn't have the right length")
            else:
                prob = self.cumu_prob[coord]
                return prob

        except AttributeError:
            # this means the cumu_prob variable doesn't exist -- it hasn't been loaded in or the method 
            # above hasn't been called. Cumulative probabilty thing is deprecated as of now. 
            # print(coord)
            if len(sentence) > self.up_to_all_probs:
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
                    return {'word': word[0], 'pos': word[1], 'index': list_pos.index(word[1]), 'tupleform':word} 


    def random_word_no_pos(self):
        """
        I need this to be part of the class because I need access to the words in the 
        blob_tagged_by_sentence and sen_tag_pword
        This method just generates a random word. It does it in a weighted manner, however. 
        This means that if p.o.s. 1 occurs more frequently in the text than p.o.s. 2 it 
        will be more likely to choose pos 1. 
        """
        rando = np.random.random()
        for pos in self.list_pos:
            if rando <= self.cumu_pos_freq[pos]:
                special_pos = pos 
                break 
        tot_sen = self.sen_tag_pword
        start_point = random.randint(0,(len(tot_sen)*3)/4)
        for index in xrange(start_point,len(tot_sen)-1):
            for word in tot_sen[index]:
                if word[1] == special_pos:
                    return {'word': word[0], 'pos': word[1], 'index': list_pos.index(word[1]),'tupleform':word} 


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




