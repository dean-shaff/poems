import sys
from PyQt4 import QtGui
from tools import Text_Generator
from tools import Twitter_Tools
from tools import Stress_Poem
from tools import Haiku
from tools import InOut
import os
import time
import numpy

class Main_App(QtGui.QWidget):

	def __init__(self):
		super(Main_App, self).__init__()

		self.initUI()

	def initUI(self):

		grid = QtGui.QGridLayout()
		grid.setSpacing(10)

		self.choose_file = QtGui.QPushButton("Choose File...")
		grid.addWidget(self.choose_file,2,1)
		self.choose_file.clicked.connect(self.browse)

		self.text_box = QtGui.QTextEdit("Welcome to the poem generating app!\n\nIf no file is selected, will build using article titles.\n\n")
		grid.addWidget(self.text_box,1,1,1,2) #now it spans multiple columns

		self.haiku = QtGui.QPushButton("Generate Haiku")
		grid.addWidget(self.haiku,2,2) #row, column
		self.haiku.clicked.connect(self.make_haiku)

		self.post = QtGui.QPushButton("Post to twitter")
		grid.addWidget(self.post,3,1)
		self.post.clicked.connect(self.postit)

		self.setLayout(grid)

		self.setGeometry(300,300,300,300) 
		self.setWindowTitle("Poem Generator")
		self.show()

	def browse(self):
		filename = QtGui.QFileDialog.getOpenFileName()
		string = str()
		if filename != "":
			with open(filename,'r') as reader:
				for line in reader:
					if line == '\n':
						pass
					else:
						string += line.strip('\n')
			self.text_box.append("File built.")
		elif filename == "":
			self.text_box.append("You didn't pick a file!")
		self.string = string
		self.filename = filename

	def make_haiku(self):
		try:
			texter = Text_Generator(generate=False,text=self.string)
			word_list1 = texter.make_syll(python=True)
			haiku = Haiku(wordlist=word_list1).make_poem_ordered(diff_style=True)
			self.haiku = haiku
			self.text_box.append("{}\n\n".format(haiku))
		except AttributeError:
			texter = Text_Generator(generate=False,text=None)
			word_list1 = texter.make_syll(python=True)
			haiku = Haiku(wordlist=word_list1).make_poem_ordered(diff_style=True)
			self.haiku = haiku
			self.text_box.append("{}\n\n".format(haiku))
	
	def postit(self):
		try:
			twitter = Twitter_Tools()
			twitter.get_authorization()
			twitter.make_post(self.haiku)
			self.text_box.append("All done!\n\n")
		except AttributeError:
			self.text_box.append("Make a haiku first.\n\n")

def main():

	app = QtGui.QApplication(sys.argv)
	main_app = Main_App()
	sys.exit(app.exec_())

if __name__ =="__main__":
	main()