import json
import redis

r = redis.Redis('localhost')

class Point:
	def __init__(self, sent, time):
		self.sent = sent
		self.time = time
# get all the sentiments and their times
tweets = r.keys(pattern="tweet:trend:*")
points = []
for key in tweets:
	p = Point(r.hget(key, "sentiment"), r.hget(key, "date"))
	points.append(p)
	
# write these in json format to a json file
with open('data.json', 'w') as f:
	f.write("[")
	for i,point in enumerate(points):
		f.write("{")
		f.write('"sentiment":' + '"'+point.sent + '"')
		f.write(",")
		f.write('"time":' + '"' + point.time + '"')
		f.write("}")
		if i < len(points)-1:
			f.write(",")
	f.write("]")
