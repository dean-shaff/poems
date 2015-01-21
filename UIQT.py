import sys
from PyQt4 import QtGui, QtCore
from tools import Text_Generator
from tools import Twitter_Tools
from tools import Stress_Poem
from tools import Haiku
from tools import InOut
import threading
import os
import time
import numpy
"""
17/1/2015 It'd be cool to get the continous post button working. Also, it would be cool 
to make it so it periodically changes which text file it uses. 
"""

class Main_Window(QtGui.QMainWindow):

	def __init__(self,parent=None):
		super(Main_Window,self).__init__(parent)
		self.initwindow()

	def initwindow(self):

		self.widget = App_Widgets(self)
		self.setCentralWidget(self.widget)
		
		exitAction = QtGui.QAction('&Exit',self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.triggered.connect(QtGui.qApp.quit) #just quitting

		choosefileaction = QtGui.QAction('&Choose File...',self)
		choosefileaction.triggered.connect(self.widget.browse)

		menubar = self.menuBar()
		filemenu = menubar.addMenu('&File')
		filemenu.addAction(exitAction)
		filemenu.addAction(choosefileaction)

		self.setGeometry(300,300,300,300) 
		self.setWindowTitle("Poem Generator")
		self.show()

class App_Widgets(QtGui.QWidget):

	def __init__(self,parent):
		super(App_Widgets, self).__init__(parent)
		# QtGui.QWidget.__init__(self)
		# QtGui.QMainWindow.__init__(self)
		self.initUI()

	def initUI(self):

		grid = QtGui.QGridLayout()
		grid.setSpacing(10)
		self.grid = grid

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

		self.post_continuous = QtGui.QPushButton("Post continously")
		grid.addWidget(self.post_continuous,3,2)
		self.post_continuous.clicked.connect(self.post_continuous_fn)

		self.setLayout(grid)

		self.threadPool = []
	
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

	def post_continuous_fn(self):

		def stop():
			self.threadPool[0].stopped = True
			self.post_continuous.setText("Stop")
			self.post_continuous.clicked.connect(return_original)
			QtGui.QApplication.processEvents()

		def post_cont():
			thread2 = MyThread(function=stop)
			self.threadPool.append(thread2)
			thread2.start()
			print(self.threadPool)
			# while True:
			# 	QtGui.QApplication.processEvents()
			# 	print("Hey")
			# 	time.sleep(1)

		thread1 = MyThread(function=post_cont)
		self.threadPool.append(thread1)
		thread1.start()

		def return_original():
			self.post_continuous.setText("Post continuously")
			# self.post_continuous.clicked.connect(self.post_continuous_fn)
			return False


class MyThread(threading.Thread):

	def __init__(self, function, *args, **kwargs):
		
		self.function = function
		self.args = args
		self.kwargs = kwargs
		self.stopped = False
		threading.Thread.__init__(self)

	def run(self):

		if not self.stopped:
			self.function(*self.args, **self.kwargs)






			# QtGui.QApplication.processEvents()

# class GenericThread(QtCore.QThread):

# 	def __init__(self, function, *args, **kwargs):

# 		QtCore.QThread.__init__(self)
# 		self.function = function
# 		self.args = args
# 		self.kwargs = kwargs

# 	def __del__(self):
# 		self.wait()

# 	def run(self):
# 		self.function(*self.args, **self.kwargs)
# 		return 

def main():

	app = QtGui.QApplication(sys.argv)
	main_app = Main_Window()
	sys.exit(app.exec_())

if __name__ =="__main__":
	main()