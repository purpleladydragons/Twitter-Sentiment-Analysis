import time
import redis
import nltk
from text_purger import Purger

r = redis.Redis('localhost')

# pos and gram funcs
sent_tags = {}
sent_tags['obj'] = {}
sent_tags['pos'] = {}
sent_tags['neg'] = {}
def updatePOScounts(terms, sent):
	tags = [tag for (word, tag) in terms]	
	for tag in tags:
		if tag in sent_tags[sent]:
			sent_tags[sent][tag] += 1
		else:
			sent_tags[sent][tag] = 1

sent_grams = {}
sent_grams['obj'] = {}
sent_grams['pos'] = {}
sent_grams['neg'] = {}

def updateUnigramPresence(words, sent):
	for i in range(len(words)):
		gram = words[i].lower()
		if gram in sent_grams[sent]:
			sent_grams[sent][gram] += 1
		else:
			sent_grams[sent][gram] = 1

def updateBigramPresence(words, sent):
	for i in range(len(words)-1):
		gram = (words[i]+" "+words[i+1]).lower()
		if gram in sent_grams[sent]:
			sent_grams[sent][gram] += 1
		else:	
			sent_grams[sent][gram] = 1

purger = Purger()
# populate each tag and gram dict
sents = ['obj', 'pos', 'neg']
for sent in sents:
	for key in r.keys(pattern="tweet:"+sent+":*"):
		# get text of tweet
		text = r.get(key).decode('utf8')
		text = purger.purge(text)
		words = purger.tokenize(text)
		updatePOScounts(nltk.pos_tag(words), sent)
		updateBigramPresence(words, sent)


# reverse the sent-tag/gram direction
tags = {}
for sent in sent_tags:
	for tag in sent_tags[sent]:
		#inc its sent presence
		if tag in tags:
			tags[tag][sent] += sent_tags[sent][tag]
		else:
			tags[tag] = {}
			for sentiment in sent_tags:
				tags[tag][sentiment] = 0
			tags[tag][sent] += sent_tags[sent][tag]
grams = {}
for sent in sent_grams:
	for gram in sent_grams[sent]:
		#inc its sent presence
		if gram in grams:
			grams[gram][sent] += sent_grams[sent][gram]
		else:
			grams[gram] = {}
			for sentiment in sent_grams:
				grams[gram][sentiment] = 0
			grams[gram][sent] += sent_grams[sent][gram]

# save probability to redis
for tag in tags:
	total = 0
	for sent in tags[tag]:
		total += tags[tag][sent]
	for sent in tags[tag]:
		r.set("tag:"+sent+":"+tag, float(tags[tag][sent])/total)

for gram in grams:
	total = 0
	for sent in grams[gram]:
		total += grams[gram][sent]
	for sent in grams[gram]:
		r.set("gram:"+sent+":"+gram, float(grams[gram][sent])/total)


