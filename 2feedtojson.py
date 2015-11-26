import os
import sys
import json
import feedparser
import nltk
from BeautifulSoup import BeautifulStoneSoup
from nltk import clean_html

FEED_URL = 'http://feeds.feedburner.com/oreilly/radar/atom'

def cleanHtml(html):
	return BeautifulStoneSoup(html).getText()

fp = feedparser.parse(FEED_URL)

print "Fetched %s entries from '%s'" % (len(fp.entries[0].title), fp.feed.title)

blog_posts = []
for e in fp.entries:
	sentences = nltk.tokenize.sent_tokenize(cleanHtml(e.content[0].value))
	#print len(sentences)
	if len(sentences) > 5:
		blog_posts.append({'title': e.title, 
							'content' : cleanHtml(e.content[0].value), 
							'link' : e.links[0].href})
out_file = os.path.join('data','feed.json')
f = open(out_file, 'w');
f.write(json.dumps(blog_posts, indent=1))
f.close()

print 'Wrote output file to %s' % (f.name,)