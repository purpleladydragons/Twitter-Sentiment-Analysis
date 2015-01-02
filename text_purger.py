import re
from nltk.corpus import stopwords

class Purger:
	stop = stopwords.words('english')

	def stripLinks(self, text):
		return re.sub(r'https?://(\S+)', '', text)

	def stripUsers(self, text):
		return re.sub(r'@(\S+)', '', text)

	def stripHashtags(self, text):
		return text.replace("#", "")

	def stripEmoticons(self, text):
		return text.replace(":)", "").replace(":(", "")

	def stripRT(self, text):
		return text.replace(" RT", " ").replace("RT ", " ")

	def stripPunctuation(self, text):
		return text.replace(".", " ").replace(",", " ").replace('"', " ").replace(" '", " ").replace("' ", " ").replace("!", " ").replace("?", " ")\
			.replace(":", " ").replace(";", " ").replace("]", " ").replace("[", " ").replace(")", " ").replace("(", " ").replace(" -", " ").replace("- ", " ")

	def tokenize(self, text):
		return text.split()

	def removeStopwords(self, words):
		copy = []
		for word in words:
			if word not in self.stop:
				copy.append(word)
		return copy

	def purge(self, text):
		text = self.stripLinks(text)
		text = self.stripUsers(text)
		text = self.stripHashtags(text)
		text = self.stripEmoticons(text)
		text = self.stripRT(text)
		text = self.stripPunctuation(text)
		return text

