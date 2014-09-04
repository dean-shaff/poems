# -*- coding: utf-8 -*-

"""
This code takes the English dictionary, separated into syllables, 
and replaces all the weird yen characters with plus signs. 
It also makes a copy of the dictionary with no 
"""

filename2 = "mhyph.txt"
filename3 = "msyll.txt"
filename4 = "mdic.txt"

with open(filename2,'ra') as dic, open(filename3,'w') as replace:
	for index,line in enumerate(dic):		
		line = list(line)
		for index1, char in enumerate(line):
			try:
				char = char.encode('utf-8')
			except UnicodeDecodeError:
				line[index1] = "+"
		line = "".join(line)
		replace.write(line)

with open(filename2,'ra') as dic, open(filename4,'w') as replace:
	for index,line in enumerate(dic):		
		line = list(line)
		for index1, char in enumerate(line):
			try:
				char = char.encode('utf-8')
			except UnicodeDecodeError:
				line[index1] = ""
		line = "".join(line)
		replace.write(line)







			
