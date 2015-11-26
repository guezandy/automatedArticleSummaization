import os
import json
import nltk
import numpy
from IPython.display import IFrame
from IPython.core.display import display

data_file = 'data/feed.json'
N = 100 #num of words to consider
cluster_threshold = 5 #distance between words
top_sentences = 5 #number of sentences to return for a top n summary

HTML_TEMPLATE = """<html>
	<head>
		<title>%s</title>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
	</head>
	<body>%s</body>
	</html>"""

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
	normalize_sentences = [s.lower() for s in sentences]

	words = [w.lower() for sentence in normalize_sentences for w in 
				nltk.tokenize.word_tokenize(sentence)]

	fdist = nltk.FreqDist(words)

	top_n_words = [w[0] for w in fdist.items()
					if w[0] not in nltk.corpus.stopwords.words('english')][:N]

	scored_sentences = score_sentences(normalize_sentences, top_n_words)

	#Return only the top N ranked sentences
	top_n_scored = sorted(scored_sentences, key=lambda s: s[1])[-top_sentences:]
	top_n_scored = sorted(top_n_scored, key=lambda s: s[0])

	return dict(top_n_summary=[sentences[index] for(index,score) in top_n_scored])


data = json.loads(open(data_file).read())

for post in data:
	post.update(summarize(post['content']))

	for summary_type in ['top_n_summary']:
		post[summary_type+ '_marked_up'] = '<p>%s</p>' % (post['content'],)
		for s in post[summary_type]:
			post[summary_type+'_marked_up'] = post[summary_type+'_marked_up'].replace(s, '<strong>%s</strong>' %(s,))

	filename = post['title'].replace("?", "") + '.summary.' + summary_type + '.html'
	f = open(os.path.join('data', filename), 'w')
	html = HTML_TEMPLATE % (post['title'] + ' Summary', post[summary_type+'_marked_up'],)

	f.write(html.encode('utf-8'))
	f.close()

	print "data written to", f.name

print "Displaying %s:" % f.name
display(IFrame('files/%s' %f.name, '100%', '600px'))
















