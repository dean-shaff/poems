import newspaper 
import os
from bs4 import BeautifulSoup as bs 
import urllib2
import httplib
import time 
import subprocess
from inoutsoft import InOut

home = os.path.expanduser("~")
path_to_memorized = "{}/.newspaper_scraper/memoized".format(home)
path_current = os.getcwd() #'/home/dean/python_stuff_ubuntu/poems'
cnnfilename = "cnn.com.txt"
textdir = "{}/texts".format(os.getcwd())
title_filename = "article_titles.txt"

class Article_Stuff(object): 
	def __init__(self,source='http://cnn.com'):
		self.source = source
		self.path_current = path_current
		self.textdir = textdir
		self.title_filename = title_filename
	def gen_article_titles(self): 
		"""
		This function generates returns a list of article titles from CNN
		It also appends the article titles to an "article_titles.txt" file.
		This only works for cnn right now. 
		"""
		paper = newspaper.build(self.source) #this just updates the contents of the page
		with InOut(path_to_memorized):
			urls = []
			titles = []
			with open(cnnfilename,'r') as reader:
				for line in reader:
					line = line.strip("\n")
					urls.append(line)
			assert len(urls) != 0, "You didn't correctly extract the urls!"
		
		with InOut(textdir):
			with open(title_filename,"a") as articletitles:
				for index, url in enumerate(urls):
					try:
						if index % 10 == 0 and index != 0:
							articletitles.flush()
							print("Flushing")
						print("Running...")
						r = urllib2.urlopen(url)
						data = r.read()
						with open('temp.html','w') as temp:
							temp.write(data)
						soup = bs(open('temp.html'))
						if soup.title != None:
							try:
								if self.source == 'http://cnn.com':
									title = soup.title.string.rstrip("- CNN.com Vide") #just want to use the end
								articletitles.write("{}\n".format(title))
								titles.append(title)
							except UnicodeEncodeError:
								pass
					except (urllib2.HTTPError, httplib.HTTPException, urllib2.URLError): 
						pass
		return titles

	def gen_article_text(self): #Not currently functioning. 
		paper = newspaper.build(self.source)
		articles = paper.articles
		texts = []
		with open("article_text.txt","a") as articletexts:
			for i in articles:
				i.download()
				i.parse()
				titles.append(i.texts)
				articletitles.write("{}\n".format(i.text))
		return texts