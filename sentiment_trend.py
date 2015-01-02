import re
import time
import redis
import nltk
from text_purger import Purger

r = redis.Redis('localhost')

tweets = r.keys(pattern="tweet:trend:*")
pipe = r.pipeline()
for key in tweets:
	pipe.hget(key, "text")

texts = pipe.execute()


sents = ['pos', 'neg']
# for each sentiment
# calc pos score 
# calc bigram score

sentiments = [0,0,0]

purger = Purger()
for j,test in enumerate(texts):
	scores = []
	test = test.decode('utf8')
	test = purger.purge(test)
	words = purger.tokenize(test)
	for sent in sents:
		prob = 1.0

		# get pos tags
		tags = [tag for (word, tag) in nltk.pos_tag(words)]
		for tag in tags:
			p = r.get("tag:"+sent+":"+tag)
			prob = prob * float(p)

		for i in range(len(words)-1):
			gram = words[i] + " " + words[i+1]	
			p = r.get("gram:"+sent+":"+gram)
			if p is not None:
				prob *= float(p)

		scores.append(prob)	

	r.hset(tweets[j], "sentiment", sents[scores.index(max(scores))])
