import tweepy

npprff_gbxra = "2783510875-eCF7AdyV2NOt1HgVNKw0uWAMcPV6YCL5tWI5lqc"
npprff_gbxra_frperg = "YtCROvd2p9mCadHaopEoiqq8nAtInHZTbVQrRnJP7Abcw"

pbafhzre_xrl = "gdHAvtxB4bMDerTvXzR70V2oz"
pbafhzre_frperg = "IVhdPID2vAxueFqrktgOKvCOlKHDJrMW2cjloWWS1fGuPPkaF3"

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
