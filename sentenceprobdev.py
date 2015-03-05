"""
My testing ground for the sentence probabilty stuff
"""
from sentenceprob import Sentence_Probability
from sentenceprob import sentence_processor
import matplotlib.pyplot as plt 
import numpy as np 
import time

def main():
    filename = 'melville.txt'
    up_to1 = 7
    sentence = sentence_processor(write_to_file=False,
      sentence="he ate food in the house today.") 
    tagged = Sentence_Probability(filename, max_line=10000, 
            write_to_file=False,load_tagged=True,load_tot_prob=True) #note that I don't need to run "all_probs" method because I'm loading in the data. 
    prob = tagged.all_probs(up_to=up_to1,write_to_file=True)   
    print(tagged.calc_cumu_prob(sentence))

    # print(tagged.total_prob[:,:,1])
    def plot_errthing():
        plt.ion()
        for i in xrange(up_to1):
            tagged.image_plot(tagged.total_prob[:,:,i])
            plt.show()
            raw_input(">> ")
            plt.clf()

def genlots():
    """
    This just makes a big ole tagged and prob python file for me to load in later.
    """
    # filenames = ['melville.txt','AustenPride.txt','DickensTaleofTwo.txt']
    # tagged = Sentence_Probability(filenames, max_line='max', write_to_file=True,load_tagged=False,load_tot_prob=False,pos_freq=False)
    # tagged.all_probs(up_to=10,write_to_file=True)
    #now test to see it all worked. 
    filenames = ['melville.txt','AustenPride.txt','DickensTaleofTwo.txt']
    tagged = Sentence_Probability(filenames, max_line='max', write_to_file=False,load_tagged=True,load_tot_prob=True,pos_freq=True)

def feb26march3():
    filename = 'melville.txt'
    tagged = Sentence_Probability(filename, max_line=10000, 
            write_to_file=False, load_tagged=True,load_tot_prob=True,pos_freq=True)
    # prob = tagged.all_probs(up_to = 7, write_to_file=True)
    total_probs = np.zeros(len(tagged.sen_tag_pword))
    for index, sentence in enumerate(tagged.sen_tag_pword):
        if len(sentence) < 7:
            # print("Shorty sentence. Messing up probability.")
            continue
        prob = tagged.calc_cumu_prob(sentence)
        total_probs[index] = prob 
    #10 most probable sentences
    # print(tagged.blob_tagged_by_sentence[0:10])
    most_prob_sentences = []
    print("\n\n")
    for i in xrange(100):
        max_prob = np.max(total_probs)
        index_max = np.where(total_probs==np.max(total_probs))[0][0]
        most_prob_sentences.append([tagged.blob_tagged_by_sentence[index_max],max_prob])
        total_probs[index_max] = 0
        # print(" ".join(word[0] for word in tagged.sen_tag_pword[index_max]))
        # print("\n\n")
    for i in xrange(1,len(most_prob_sentences)):
        most_prob_sentences[i][1] += most_prob_sentences[i-1][1]
    # print(most_prob_sentences[-1][1])
    # print(" ".join(str(sentence[1]) for sentence in most_prob_sentences))    
    def make_sentence():
        rando = np.random.random()*most_prob_sentences[-1][1] 

        for sentence in most_prob_sentences:
            if rando < sentence[1]:
                model = sentence 
                break 
            else:
                pass 

        for i in xrange(10):        
            created = [tagged.random_word(pos)['word'] for pos in model[0]]
            print(" ".join(created))
            print("\n")
        print("\n\n")
    for i in xrange(10):
        make_sentence()
    # for sentence in most_prob_sentences:

    # print(most_prob_sentences)

    def make_lil_sentence():

        starting_word = tagged.random_word_no_pos()['tupleform']

        sentence = [starting_word]

        sentence_indices = [starting_word[1]] #just pos 

        for j in xrange(7):
            probs = np.zeros(len(tagged.list_pos))
            test_word_list = []
            for i, pos in enumerate(tagged.list_pos):
                test_word = tagged.random_word(pos)['tupleform']
                test_word_list.append(test_word)
                sentence.append(test_word)
                probs[i] = tagged.calc_cumu_prob(sentence)
                sentence.pop()
            index_spec = np.where(probs==np.max(probs))[0][0] #weird weird 
            sentence.append(test_word_list[index_spec])
            sentence_indices.append(index_max) 
        sentence_str = str() 
        for word in sentence:
            sentence_str += word[0] + " "

        return (sentence, sentence_indices, sentence_str)
    # final_sentence = None
    # for i in xrange(1000):
    #     # final_sentence = None
    #     test_sentence = make_lil_sentence()
    #     print(test_sentence[2])
    #     for sentence in most_prob_sentences:
    #         print(sentence)
    #         print(len(sentence[0][0:len(test_sentence[1])]), len(test_sentence[1]))
    #         if sentence[0][0:len(test_sentence[1])] == test_sentence[1]:
    #             final_sentence = test_sentence
    #             break
    #         else:
    #             continue
    #     if final_sentence != None:
    #         break

    # print(final_sentence)

def feb4():
    up_to1 = 8
    keyword = "love"
    article_file = "deadmen.txt"
    tagged = Sentence_Probability(article_file, 
        max_line="max",write_to_file=False)
    prob = tagged.all_probs(up_to=up_to1, write_to_file=False)
    imp_sen = []#important_sentences
    for sentence in tagged.sen_tag_pword:
        for word_pair in sentence:
            if keyword == word_pair[0]:
                imp_sen.append(sentence)
                break
    print(len(imp_sen))
    print(imp_sen[10])


if __name__ == "__main__":
    # feb26march3()
    genlots()
