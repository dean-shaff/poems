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

def feb26march4():
    filename = 'melville.txt'
    tagged = Sentence_Probability(filename, max_line=10000, 
            write_to_file=False, load_tagged=True,load_tot_prob=True)
    # prob = tagged.all_probs(up_to = 7, write_to_file=True)
    for sentence in tagged.sen_tag_pword:
        if len(sentence) < 7:
            print("Shorty sentence. Messing up probability.")
            time.sleep(1)
        prob = tagged.calc_cumu_prob(sentence)
        print(prob)

# Let's do something totally naive. 
# Let's take the article titles and catalogue the words that are associated
# with some keyword. 
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
    feb26()