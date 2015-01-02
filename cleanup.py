import redis

r = redis.Redis('localhost')

mpattern = "tweet:trend:*"
grams = r.keys(pattern= mpattern)

for gram in grams:
	r.delete(gram)
