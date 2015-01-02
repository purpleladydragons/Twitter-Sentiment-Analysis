import sys
import redis
import tweepy
import json

r = redis.Redis('localhost')

class Tweet:
	def __init__(self, text, date, lng, lat):
		self.text = text
		self.date = date
		self.lng = lng
		self.lat = lat

def saveStatus(status):
	print saveStatus.i
	saveStatus.i+=1
	if saveStatus.i > 200:
		sys.exit()
	id_str = status.id_str
	text = status.text
	r.hset("tweet:trend:"+id_str, "date", status.created_at)
	r.hset("tweet:trend:"+id_str, "text", text)
	# get id str
	# then start looping thru json struct
	# every non-id key, value pair gets hset
	#r.set(id_str, field, value)
saveStatus.i = 0
	
class Listener(tweepy.StreamListener):
	def on_status(self, status):
		saveStatus(status)

CONSUMER_KEY = 'kV97tpcwLwXb61CdbOtoU2MWN'
CONSUMER_SECRET = 'QXP3VLxglEFOOAC7fGAMPrH0nveyB4HldlPWBB1smaOWxkxqCP'
OAUTH_TOKEN = '2868133637-NHFFVtglr2bGYdSikpvRJAH3SonZsqgkOT2jgyL'
OAUTH_TOKEN_SECRET = 'UpQvXliLRgl5DVEoSbnlwNsMKYYdGZr8ONcSU8gKZBl0m'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

streaming_api = tweepy.streaming.Stream(auth, Listener(), timeout=60)

api = tweepy.API(auth)

#streaming_api.filter(languages = ['en'], track=['#asknorman']) 

# search tweets from popular news sources to get objective tweets
#users = ['nytimes', 'washingtonpost', 'wsj', 'usatoday', 'latimes', 'nydailynews', 'nypost', 'chicagotribune', 'suntimes', 'denverpost', \
#			'thewest_com_au', 'readersdigest']
#users = ['nationaltrust', 'aarp', 'gameinformer', 'sinow', 'espn', 'wired', 'phillyinquirer', 'mercnews']

for status in api.search("kim kardashian", lang="en", rpp=100):
	saveStatus(status)

#for user in users:
#	for status in tweepy.Cursor(api.user_timeline, id=user).items(300):
#		saveStatus(status)
