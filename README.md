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

Basic Usage (making haiku and posting to twitter):
	
	"""
	***IMPORTANT***
	Note that this will not work unless you go into tools/twitter_tools.py 
	and remove the encrpyted text and replace with own auth keys.
	I'm working on a better means of dealing with this.
	"""
	from tools import Article_Stuff
	from tools import Twitter_Tools
	from tools import Text_Generator
	from tools import InOut
	from tools import Haiku 

	texter = Text_Generator(generate=False,text=None) #text = None means we use articles
	word_list4 = texter.make_syll(python=False)
	orderedpoem = Haiku(wordlist=word_list4).make_poem_ordered(diff_style=True)
	twitter = Twitter_Tools()
	twitter.get_authorization()
	twitter.make_post(orderedpoem)

Basic Usage (word probability stuff):

	from sentenceprob import Sentence_Probability
	filename = 'melville.txt'
	tagged = Sentence_Probability(filename, max_line='max', 
    	        write_to_file=False, load_tagged=False,load_tot_prob=False)
	tagged.all_probs(up_to=10,write_to_file=True) #calculates total probabilities 

