#using boilerpipe
#contains different kinds of extractors: LargestCOntentExtractor or DefaultExtractor

#step 1 extract http://radar.oreilly.com/2010/07/louvre-industrial-age-henry-ford.html
#article extractor extracts the largest piece of text in a site

from boilerpipe.extract import Extractor 

URL = 'http://radar.oreilly.com/2010/07/louvre-industrial-age-henry-ford.html'

extractor = Extractor(extractor='ArticleExtractor', url=URL)

print extractor.getText()