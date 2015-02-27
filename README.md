poems
=====

Python code that generates poetry using found text 

Requirements:

-tweepy

-newspaper

-numpy version 1.7+

-nltk

-nltk_contrib

-Beautiful Soup

-textblob

-textblob-aptagger

Basic Usage:

	from sentenceprob import Sentence_Probability
	filename = 'melville.txt'
	tagged = Sentence_Probability(filename, max_line='max', 
    	        write_to_file=False, load_tagged=False,load_tot_prob=False)
	tagged.all_probs(up_to=10,write_to_file=True) #calculates total probabilities 

