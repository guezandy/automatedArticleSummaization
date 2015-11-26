import json
import nltk
from nltk.tokenize import sent_tokenize


#nltk.download('stopwords')
#nltk.download()

data_file = 'data/feed.json'
data = json.loads(open(data_file).read())

#custom list of stop words

stop_words = nltk.corpus.stopwords.words('english') + [
	'.', ',','--','\'s','?',')','(',':','\'','\'re','"','-','}','{','-','=',
]

for post in data:
	sentences = nltk.tokenize.sent_tokenize(post['content'])
	words = [w.lower() for sentence in sentences for w in nltk.tokenize.word_tokenize(sentence)]

	fdist = nltk.FreqDist(words)
	#print fdist

	#basic stats
	num_words = sum([i[1] for i in fdist.items()])
	num_unique_words = len(fdist.keys())

	#haxapes words that only appear once
	num_hapaxes = len(fdist.hapaxes())

	top_10_words = [w for w in fdist.items() if w[0] not in stop_words][:10]

	print post['title']
	print '\tNum Sentences: '.ljust(25), len(sentences)
	print '\tNum Words: '.ljust(25), num_words
	print '\tNum Unique Words: '.ljust(25), num_unique_words
	print '\tNum haxapes: '.ljust(25), num_hapaxes
	print '\tTop 10 words:\n\t\t', '\n\t\t'.join(['%s'
		%(w[0]) for w in top_10_words])
	print



