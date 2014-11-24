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

# def image_plot(array):
#     """
#     Assumes array is already scaled the way you want it to be displayed
#     """
#     plot_options = {'cmap':'gray','vmin':0,'vmax':256}
#     array = np.asarray(array,dtype=float)
#     fig1 = plt.figure(figsize=(16,9))
#     ax1 = fig1.add_subplot(111)
#     ax1.matshow(array,**plot_options)
#     return ax1

# def scale(array,**kwargs):
#     """
#     assuming that the array has no complex numbers
#     """
#     try:
#         if kwargs["log"]:
#             array = np.log(np.absolute(array))
#         elif kwargs["sqrt"]:
#             array = np.sqrt(np.absolute(array))
#         elif kwargs["exp"]:
#             array = np.exp(array)
#     except KeyError:
#         pass
#     if array.dtype == 'complex':    
#         array = np.asarray(array,dtype=complex)
#         return 256.*(np.absolute(array))/np.amax(np.fabs(np.absolute(array)))
#     else:
#         array = np.asarray(array,dtype=float)
#         return 256.*(array)/np.amax(array)

class Sentence_Probability(object):

    def __init__(self, filename, up_to, write_to_file=False):
        self.text_dir = text_dir
        self.filename = filename
        master_str = str()
        with InOut(text_dir):
            with open(filename, 'r') as reader:
                for index, line in enumerate(reader):
                    line = line.strip('\n')
                    master_str += line
                    if index == up_to:
                        break
        self.master_str = master_str
        t1 = time.time()
        blob = TextBlob(master_str, pos_tagger=PerceptronTagger())
        print("Time creating object: {:.2f}".format(time.time() - t1))
        t2 = time.time()
        self.blob_tagged_by_sentence = [[word[1] for word in sentence.tags if word[1] not in list_not_allow] for sentence in blob.sentences]
        print("Time creating tagged list: {:.2f}".format(time.time() - t2))
        if write_to_file:
            with InOut(text_dir):
                with open("token{}.py".format(filename.strip('.txt')), 'w') as writer:
                    writer.write(
                        "var1 = {}".format(str(self.blob_tagged_by_sentence)))
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
        index1 is the index of A (in P(A|B)) in the list_pos list
        index2 is the index of B 
        p1 is the position of A in the sentence
        p2 is the position of B in the sentence 
        Ideally p1 > p2, as you're finding the 
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
        self.up_to = int(up_to)
        master = np.zeros((len(list_pos),len(list_pos),self.up_to),dtype=float)
        masterdict = []
        for h in xrange(0, up_to):
            position = master[:,:,h]
            t1 = time.time()
            A = {}
            for i in xrange(0, len(list_pos)):
                A2 = position[i]
                for j in xrange(0, len(list_pos)):
                    prob = self.cond_prob_v2([10, 25], i, j, h, h+1) #probability of i given j. 
                    A["{},{}".format(list_pos[i],list_pos[j])] = prob
                    A2[j] = prob
            print("Position {} to {} took {:.1f} sec".format(h,h+1,time.time()-t1))
            masterdict.append(A)
        self.total_prob = master
        if write_to_file:
            with InOut(self.text_dir):
                with open("prob{}.py".format(self.filename.strip('.txt')), 'a') as writer:
                    writer.write("var1 = {}\n".format(str(master)))
                    writer.write("var2 = {}\n".format(str(masterdict)))
            return {'list':master,'dict':masterdict}
        else:
            return {'list':master,'dict':masterdict}

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

    def independent(self):
        """
        This function returns a dictionary of the most probable pairs at each position in the sentence.
        """
        dic = {}
        try:
            test = self.total_prob
        except NameError:
            self.all_probs()
        for h in xrange(self.up_to):
            position = self.total_prob[h]
            maxB = []
            max_index = []
            for B in position:
                maxB.append(max(B))
                max_index.append(B.index(max(B)))
            dic[str(h)] = (max(maxB), list_pos[maxB.index(max(maxB))],
                           list_pos[max_index[maxB.index(max(maxB))]])  # (maxprob,A,B)
            # print(h, dic[str(h)], list_pos[dic[str(h)][1]],
            #       list_pos[dic[str(h)][2]])
        return dic

    def naive_dependent(self):
        """
        This function returns a dictionary of the most probable pairs,
        using the A from the previous step as the new B. 
        """
        try:
            test = self.total_prob
        except NameError:
            self.all_probs()
        dic = {}
        new_B = 0
        for h in xrange(self.up_to):
            if h == 0:
                position = self.total_prob[h]
                maxB = []
                max_index = []
                for A in position:
                    maxB.append(max(A))
                    max_index.append(A.index(max(A)))
                new_B = maxB.index(max(maxB))
                dic[str(h)] = (max(maxB), list_pos[maxB.index(max(maxB))],
                               list_pos[max_index[maxB.index(max(maxB))]])  # (maxprob,A,B)
                # print(h, dic[str(h)], list_pos[dic[str(h)][1]],
                #       list_pos[dic[str(h)][2]])
            else:
                position = self.total_prob[h]
                special = [position[i][new_B] for i in xrange(0, len(position))]
                old_B = new_B
                new_B = special.index(max(special))
                dic[str(h)] = (max(special), list_pos[new_B], list_pos[old_B])  # maxprob, A, B
                # print(h, dic[str(h)], list_pos[dic[str(h)][1]],
                #       list_pos[dic[str(h)][2]])
        return dic

    def smart_dependent(self):
        """
        This function generates the sentence with the highest probability. 
        """
        try:
            test = self.total_prob
        except NameError:
            self.all_probs()

        def calc_prob(A,B):
            prob = float(self.total_prob[0][A][B])
            new_B = A
            size = len(self.total_prob[0])
            dic = {'0': (prob, list_pos[A],list_pos[B])}
            for h in xrange(1,self.up_to):
                special = [self.total_prob[h][i][new_B] for i in xrange(size)]
                old_B = new_B
                new_B = special.index(max(special))
                dic[str(h)] = (max(special),list_pos[new_B],list_pos[old_B])
                prob *= max(special)
            return {'prob':prob,'dict':dic}

        current_A = 0
        current_B = 0
        current_prob = calc_prob(current_A,current_B)['prob']
        for A in xrange(len(list_pos)):
            for B in xrange(len(list_pos)):
                test_prob = calc_prob(A,B)['prob']
                # print(test_prob)
                if test_prob > current_prob:
                    current_prob = test_prob
                    current_A = A
                    current_B = B
                else:
                    pass
        return {"total prob": current_prob, 'dict': calc_prob(current_A,current_B)['dict']}

if __name__=="__main__":

    tagged = Sentence_Probability(filename, up_to=5000, write_to_file=False)
    prob = tagged.all_probs(write_to_file=False)
    prob_list = prob['list']
    tagged.graph_prob(t_step=4)
    # Sentence_Probability.image_plot(Sentence_Probability.scale(prob_list[:,:,0]))
    # plt.show()
# print(tagged.independent())
# print(tagged.naive_dependent())
# most_prob_sentence = tagged.smart_dependent()['dict']
# for i in xrange(7):
#     print(most_prob_sentence[str(i)])
# for i in xrange(7):
#   print("Probability of VB given NN: {:.4f}".format(prob_dict[i]["VB,NN"]))
#   print("Probability of VB given NNS: {:.4f}".format(prob_dict[i]["VB,NNS"]))
#   print("Probability of CC given NN: {:.4f}".format(prob_dict[i]["CC,NN"]))

# foo = imp.load_source('prob', '{}/probmelville.py'.format(text_dir))


# def cond_prob(tagged_text, magic_range, index1, index2, p1, p2):
#     """
#     tokenized_sentence_list is the list of sentences whose words have been tokenized and p.o.s. tagged.
#     index1 is the index of A (in P(A|B))
#     index2 is the index of B 
#     p1 is the position of A in the sentence
#     p2 is the position of B in the sentence 
#     """
#     magic_range = list(magic_range)
#     special_index = index1  # A
#     special_index2 = index2  # B
#     tokenized_sentence_list = tagged_text
#     # foo = imp.load_source('tokentesttext', '{}/tokentesttext.py'.format(text_dir))
#     # tokenized_sentence_list = foo.var1

#     def make_matrix(index_to_start):
#         for index1, sentence in enumerate(tokenized_sentence_list):
#             if index1 <= index_to_start:
#                 pass
#             else:
#                 if len(sentence) >= magic_range[0] and len(sentence) <= magic_range[1]:
#                     sentence_matrix = []
#                     freq_given_special = np.zeros(len(list_pos))
#                     for index_sen, word in enumerate(sentence):
#                         row = np.zeros(len(list_pos))
#                         # Below I'm constructing a vector that will allow me to
#                         # calculate P(B|A)
#                         # At position p1 and the part of speech is the one
#                         # we're testing.
#                         if index_sen == p1 and word in list_pos[special_index]:
#                             for index, p_o_s in enumerate(list_pos):
#                                 if sentence[p2] in p_o_s:
#                                     freq_given_special[index] += 1
#                                     break
#                         for index, pos in enumerate(list_pos):
#                             if word in pos:
#                                 row[index] = int(1)
#                                 sentence_matrix.append(row)
#                                 break
#                             else:
#                                 pass
#                         # this is to ensure that the row gets appended no
#                         # matter what
#                         if list(row) == list(np.zeros(len(list_pos))):
#                             sentence_matrix.append(row)
#                     while len(sentence_matrix) < magic_range[1]:
#                         sentence_matrix.append(np.zeros(len(list_pos)))
#                     return (sentence_matrix, freq_given_special, index1)
#                 else:
#                     pass
#     A = np.zeros(
#         magic_range[1] * len(list_pos)).reshape((magic_range[1], len(list_pos)))
#     B = np.zeros(len(list_pos))
#     t = 1
#     factor = float(3.0 / 4.0)
#     while t < int(float(len(tokenized_sentence_list)) * factor):
#         stuff = make_matrix(t)
#         matrix = stuff[0]
#         freq_B_A = stuff[1]
#         t = stuff[2]
#         B = np.add(B, freq_B_A)
#         A = np.add(A, matrix)
#     # calculating P(A|B)
#     # print(B)
#     row2 = A[p2]
#     # print(row2)
#     numerator = ((row2[special_index2]) / np.sum(row2)) * \
#         (B[special_index2] / np.sum(B))
#     denominator = 0
#     for i in xrange(0, len(B)):
#         denominator += ((row2[i]) / np.sum(A[p2])) * (B[i] / np.sum(B))

#     return numerator / denominator


# dependent()
