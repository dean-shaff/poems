from sentenceprob import Sentence_Probability
from sentenceprocessor import sentence_processor
import matplotlib.pyplot as plt 
import numpy as np 

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


    #all_probs != to cumu_prob. cumu_prob is incredibly intensive to calculate and really kind of unnecessary right now. 
    # cumu_prob = tagged.total_cumulative_prob(up_to=up_to1,write_to_file=True)

main()