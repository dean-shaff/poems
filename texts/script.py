# -*- coding: utf-8 -*-

"""
This code takes the English dictionary, separated into syllables, 
and replaces all the weird yen characters with plus signs. 
It also makes a copy of the dictionary with no syllable indication.
"""
filename2 = "mhyph.txt"
filename3 = "msyll.txt"
filename4 = "mdic.txt"

def make_dic(target_filename,char_to_replace):
	with open(filename2,'ra') as dic, open(target_filename,'w') as replace:
		for index,line in enumerate(dic):		
			line = list(line)
			for index1, char in enumerate(line):
				try:
					char = char.encode('utf-8')
				except UnicodeDecodeError:
					line[index1] = char_to_replace
			line = "".join(line)
			replace.write(line)
			









			
