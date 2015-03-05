import tweepy

U2FsdGVkX1/iTfZww3GUxoGWaBbNd7HkAzGtvmP1OUPG7lq0eJrX36UHkK87csIP
6dTAqpg71p7smt2ktyS6RsRJosP1LiSXykbMfY765qGXgpMdAQwob17aLzttC6LI
BDvzkGOZPk1MhGqawWGdaK+K6DZllcaZIA42uS28kxLrRnL+6iXm4Sps1G/NTtxq
+L1XmEqQjFFTJIbwzWPikitNmJeeouTUuBqjfhayV6ILFLGn/mRU1eK+t2e5Cozc
QqRdVO/ab7GmY4Tomvj4PLbVn5lxyNYzt8boqL6RHI9TxRSDvOzooej4P3yuCU9t
3lzwkx/mnKcubXiFpPAzICY2hzaj/TsmSDpCM6P5ItM=


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
