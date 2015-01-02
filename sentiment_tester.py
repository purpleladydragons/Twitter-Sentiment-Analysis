import re
import time
import redis
import nltk
from text_purger import Purger

r = redis.Redis('localhost')

pos_tests = r.mget(r.keys(pattern="tweet:test:pos*"))
neg_tests = r.mget(r.keys(pattern="tweet:test:neg*"))

right = 0
wrong = 0
sents = ['obj', 'pos', 'neg']

# for each sentiment
# calc pos score 
# calc bigram score

bigram = True

purger = Purger()
for test in neg_tests:
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
			prob = prob * (float(p))


		if bigram:
			for i in range(len(words)-1):
				gram = (words[i] + " " + words[i+1]).lower()	
				p = r.get("gram:"+sent+":"+gram)
				if p is not None:
					prob *= (float(p) + .001)
		else:
			for i in range(len(words)):
				gram = words[i]	
				p = r.get("gram:"+sent+":"+gram)
				if p is not None:
					prob *= (float(p) + .001)


		scores.append(prob)	

	if scores[1] < scores[2]:
		right += 1
	else:
		wrong += 1

print right, wrong
