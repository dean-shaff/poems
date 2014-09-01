import tweepy
import newspaper 

npprff_gbxra = "2783510875-eCF7AdyV2NOt1HgVNKw0uWAMcPV6YCL5tWI5lqc"
npprff_gbxra_frperg = "YtCROvd2p9mCadHaopEoiqq8nAtInHZTbVQrRnJP7Abcw"

pbafhzre_xrl = "gdHAvtxB4bMDerTvXzR70V2oz"
pbafhzre_frperg = "IVhdPID2vAxueFqrktgOKvCOlKHDJrMW2cjloWWS1fGuPPkaF3"
path_to_memorized = '/home/dean/.newspaper_scraper/memoized'
#====================================

class Twitter_Tools(object):
	def __init__(self):
		pass
	def get_authorization(self):
		try:
			auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
			auth.set_access_token(access_token, access_token_secret)
		except tweepy.error.TweepError:
			print("Trouble authenticating")

		api = tweepy.API(auth)
		self.api = api 
		#return api
	def make_post(self,text):
		api = self.api
		api.update_status(text)
	def get_posts(self):
		public_tweets = api.home_timeline()
		tweets = []
		for tweet in public_tweets:
			tweets.append(tweet.text)
		return tweets

class Article_Stuff(object):
	def __init__(self,source='http://cnn.com'):
		self.source = source
	def gen_article_titles(self):
		paper = newspaper.build(self.source)
		articles = paper.articles
		titles = []
		with open("article_titles.txt","a") as articletitles:
			for i in articles:
				i.download()
				i.parse()
				titles.append(i.title)
				try:
					articletitles.write(u'{}\n'.format(i.title))
				except UnicodeEncodeError:
					pass
		return titles
	def gen_article_text(self):
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



# twitter = Twitter_Tools()
# api = twitter.get_authorization()
# twitter.make_post("and on citizens\nscience fully in the in\nare of century")