import Tkinter 
from Tkinter import N, S, E, W
import ScrolledText
import tkFileDialog
from tools import Text_Generator
from tools import Twitter_Tools
from tools import Stress_Poem
from tools import Haiku
from tools import InOut
import os

class App(object):

	def __init__(self,master):
		self.master = master
		frame = Tkinter.Frame(master)

		self.button_opt = {}
		self.button_opt["padx"] = 0
		self.button_opt["pady"] = 0
		self.button_opt["anchor"] = Tkinter.CENTER
		# self.button_opt["sticky"] = Tkinter.W
		self.button_opt["width"] = 18
		self.button_opt["height"] = 2

		self.nrow = 4
		self.ncolumn = 4
		for i in xrange(self.nrow):
			Tkinter.Grid.grid_rowconfigure(master,i,pad=5)
			Tkinter.Grid.grid_columnconfigure(master,i,pad=0)

		#Below are my widgets
		self.choose_file = Tkinter.Button(master,text='Choose File...',command=self.askopenfilename,**self.button_opt)
		self.choose_file.grid(row=1,column=0,sticky=Tkinter.W)
		
		self.build = Tkinter.Button(master,text='Build Text File',command=self.buildfile,**self.button_opt)
		self.build.grid(row=1,column=1,sticky=Tkinter.W)

		self.haiku = Tkinter.Button(master,text='Generate Haiku',command=self.make_haiku,**self.button_opt)
		self.haiku.grid(row=3,column=0,sticky=W)
		
		self.post_it = Tkinter.Button(master,text="Post to twitter!",command=self.post_it,**self.button_opt)
		self.post_it.grid(row=4,column=0,sticky=W)

		# self.check = Tkinter.IntVar()
		self.check = 0
		self.check_haiku = Tkinter.Checkbutton(master,text="Check to make haiku\nusing article titles",
			command=self.checkboxhaiku,variable=self.check)
		self.check_haiku.grid(row=3,column=1,sticky=W)
		
		self.quit = Tkinter.Button(master,text='Quit',command=master.quit,width=9,height=2)
		self.quit.grid(row=self.nrow,column=self.ncolumn)
		
		self.text1 = ScrolledText.ScrolledText(master,height=15,width=50,wrap=Tkinter.WORD) 
		self.text1.insert(Tkinter.END,
			"Welcome to the poem generating app!\nTo begin, either select a file with which to make poems or check the box at the bottom.\n\n")
		self.text1.grid(row=0,column=0,columnspan=4,rowspan=1,sticky=N+S+W+E)

		self.file_opt = {}
		self.file_opt['defaultextension'] = '.txt'
		self.file_opt['initialdir'] = os.getcwd()
		self.file_opt['title'] = "Choose a file"

	def checkboxhaiku(self):
		self.check = 1

	def askopenfilename(self):
		filename = tkFileDialog.askopenfilename(**self.file_opt)
		self.filename = filename
		if filename == "":
			self.text1.insert(Tkinter.END,"You didn't select a file!".format(filename))
		else:
			self.text1.insert(Tkinter.END,"To build the file \'{}\', press the \'Build Text File\' button.".format(filename))

	def buildfile(self):
		string = str()
		try:
			with open(self.filename,'r') as reader:
				for line in reader:
					if line == '\n':
						pass
					else:
						string += line.strip('\n')
			self.string = string
			self.text1.insert(Tkinter.END,"\n\nFinished building.\n\n")
		except AttributeError:
			self.text1.insert(Tkinter.END,"Make sure to select a file first")

	def make_haiku(self):
		if self.check == 0:
			try:
				texter = Text_Generator(generate=False,text=self.string)
			except AttributeError:
				self.text1.insert(Tkinter.END,"Make sure to select and build a file first")
			word_list1 = texter.make_syll(python=True)
			haiku = Haiku(wordlist=word_list1).make_poem_ordered(diff_style=True)
			self.haiku = haiku
			self.text1.insert(Tkinter.END,"{}\n\n".format(haiku))
		elif self.check == 1:
			texter = Text_Generator(generate=False,text=None)			
			word_list1 = texter.make_syll(python=True)
			haiku = Haiku(wordlist=word_list1).make_poem_ordered(diff_style=True)
			self.haiku = haiku
			self.text1.insert(Tkinter.END,"{}\n\n".format(haiku))

	def post_it(self):
		twitter = Twitter_Tools()
		twitter.get_authorization()
		twitter.make_post(self.haiku)
		self.text1.insert(Tkinter.END,"All done!\n\n")

def main():
	root = Tkinter.Tk()

	app = App(master=root)
	app.master.title("Poem Generator")
	root.mainloop()
	root.destroy()
if __name__ == '__main__':
	main()