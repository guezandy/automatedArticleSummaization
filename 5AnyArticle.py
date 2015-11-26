#The automatic creation of literature Abstracts
#IBM Journal 1958
#H.P. Luhn
#Algorithm principles: filter out sentences containing frequently occuring words
#that appear near eachother

import json
import nltk
import numpy
from boilerpipe.extract import Extractor 


data_file = "data/feed.json"
N = 100 #num of words to consider
cluster_threshold = 5 #distance between words
top_sentences = 5 #number of sentences to return for a top n summary

def score_sentences(sentences, important_words): 
	scores = []
	sentence_index = -1

	#tokenize the sentences into words
	for s in [nltk.tokenize.word_tokenize(s) for s in sentences]:
		sentence_index += 1
		word_idx = []

		#for each word
		for w in important_words:
			try:
				word_idx.append(s.index(w))
			except ValueError, e: #word not in particular sentece
				pass
			word_idx.sort()

			#if sentence doesn't contain any important words
			if len(word_idx) == 0: continue

			#using word index cluster by using a max distance threshold
			#for 2 consecutive words
			clusters = []
			cluster = [word_idx[0]]
			i = 1
			while i < len(word_idx):
				#are words near eachother
				if word_idx[i] - word_idx[i-1] < cluster_threshold:
					cluster.append(word_idx[i])
				else:
					clusters.append(cluster[:])
					cluster = [word_idx[i]]
				i += 1
			clusters.append(cluster)
			#score each cluster, max score of any cluster that the sentence is in is it's max score

			max_cluster_score = 0
			if clusters:
				for c in clusters:
					significant_word_in_cluster = len(c)
					total_words_in_cluster = c[-1] - c[0] + 1
					score = 1.0*significant_word_in_cluster * significant_word_in_cluster / total_words_in_cluster

					if score > max_cluster_score:
						max_cluster_score = score 
					scores.append((sentence_index, score))
			return scores 


def summarize(txt):
	sentences = [s for s in nltk.tokenize.sent_tokenize(txt)]
	#print sentences
	normalize_sentences = [s.lower() for s in sentences]

	words = [w.lower() for sentence in normalize_sentences for w in 
				nltk.tokenize.word_tokenize(sentence)]

	fdist = nltk.FreqDist(words)

	print fdist

	top_n_words = [w[0] for w in fdist.items()
					if w[0] not in nltk.corpus.stopwords.words('english')][:N]

	scored_sentences = score_sentences(normalize_sentences, top_n_words)

	#Return only the top N ranked sentences
	top_n_scored = sorted(scored_sentences, key=lambda s: s[1])[-top_sentences:]
	top_n_scored = sorted(top_n_scored, key=lambda s: s[0])

	return dict(top_n_summary=[sentences[index] for(index,score) in top_n_scored])


URL = 'http://espn.go.com/blog/detroit-lions/post/_/id/20681/matthew-stafford-vs-mark-sanchez-a-battle-of-2009-top-5-picks'

extractor = Extractor(extractor='ArticleExtractor', url=URL)
data = extractor.getText()
print data

data = summarize(data)

print 'Top N Summary'
print '-------------'
print ' '.join(data['top_n_summary'])
print







