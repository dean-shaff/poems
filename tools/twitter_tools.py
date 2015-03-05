import tweepy

access_token = "2783510875-rPS7NqlI2ABg1UtIAXj0hJNZpCI6LPY5gJV5ydp"
access_token_secret = "LgPEBiq2c9zPnqUnbcRbvdd8aNgVaUMGoIDeEaWC7Nopj"

consumer_key = "tqUNigkO4oZQreGiKmE70I2bm"
consumer_secret = "VIuqCVQ2iNkhrSdexgtBXiPByXUQWeZJ2pwybJJF1sThCCxnS3"


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
		try:
			api = self.api
			api.update_status(text)
		except tweepy.error.TweepError:
			print("Trouble making the post")
			pass
	def get_posts(self):
		public_tweets = api.home_timeline()
		tweets = []
		for tweet in public_tweets:
			tweets.append(tweet.text)
		return tweets
