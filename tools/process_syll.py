import os
from tools import InOut

base_dir = os.path.dirname(__file__)
if os.path.exists(os.path.join(os.getcwd(),'texts')):
	text_dir = os.path.join(base_dir,'texts')
else:
	text_dir = base_dir

def main():
	with InOut(text_dir):
		with open('syll_count.py','w') as count:
			count.write('syll_dic = {\n')
			with open('mdic.txt', 'r') as dic, open('msyll.txt', 'r') as syll:
				for index, (linedic, linesyll) in enumerate(zip(dic,syll)):
					syll_total = 1
					for char in linesyll:
						if char == "+" or char == " ":
							syll_total += 1
					count.write("\"{}\":{},\n".format(linedic.lower().strip('\r\n'),syll_total))
					# if index > 10:
					# 	break
			count.write('}')

from tools.syll_count import syll_dic
print(syll_dic["hegemony"])
print(syll_dic["cup"])

# main()


