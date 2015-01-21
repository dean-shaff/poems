from tools import Article_Stuff
from tools import Twitter_Tools
from tools import Text_Generator
from tools import InOut
from tools import Haiku 
import os 
import time
import numpy
#===============================================
base_dir = os.path.dirname(__file__)
text_dir = os.path.join(base_dir, 'texts')
filename = "haikus-jterm-articles.txt"

fileconrad = "conrad.txt"
filekafka = "kafka.txt"
fileyellow = "yellow.txt"
filedickens = "DickensTaleofTwo.txt"
filechina = "china.txt"
filechristie = "christie.txt"
filedeadmen = "deadmen.txt"
filefairy = "fairy.txt"
filekant = "kant.txt"
filesteam = "steam.txt"
fileausten = "AustenPride.txt"
fileglass = "GlassbyEdwardDillon.txt"
#===============================================

files = [
	fileconrad,fileglass,fileausten,
	filesteam,filekant,filefairy,
	filedeadmen,filechristie,filechina,
	fileyellow,filekafka,filedickens 
	]

def build_textfile(filename):
	"""
	assumes file is in the text file directory.
	"""
	file_string = str()
	with InOut(text_dir):
		with open(filename, 'r') as reader:
			for line in reader:
				if line == '\n':
					pass
				else:
					file_string += line.strip('\n')
	return file_string

def gen_many(niter,string_from_file=None):
	if string_from_file != None:
		texter = Text_Generator(generate=False,text=string_from_file)
	elif string_from_file == None:
		texter = Text_Generator(generate=False,text=None)
	try:
		word_list = texter.make_syll(python=True)
		with open(filename, 'a') as haikus:
			for i in xrange(niter):
				# try:
				poem = Haiku(wordlist=word_list).make_poem_ordered(diff_style=True)
				haikus.write(poem)
				haikus.write('\n\n')
				print(poem)
				# except AssertionError:
				# 	continue
	except UnicodeDecodeError:
		pass

def main():
	# for book in files:
	# 	book_total = build_textfile(book)
	# 	gen_many(50,string_from_file=book_total)
	gen_many(100,string_from_file=None) #to get article titles as well

main()