import feedparser

FEED_URL = 'http://feeds.feedburner.com/oreilly/radar/atom'

fp = feedparser.parse(FEED_URL)

for e in fp.entries:
	print e.title
	print e.links[0].href
	print e.content[0].value
	print 
	print 
	print 
	print