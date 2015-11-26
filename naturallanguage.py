#5 main things:
#1. EOS detection
#2. Tokenization
#3. Part of speech tagging
#4. Chunking
#5. Extraction

#Sentences are predictable we can turn a paragraph into an array of sentences using
import nltk

txt = "Mr. Green killed Colonel Mustard in the study with the candlestick. Mr Green is not a very nice fellow"
sentences = nltk.tokenize.sent_tokenize(txt)

print sentences

#get words from each sentence
tokens = [nltk.tokenize.words_tokenize(s) for s in sentences]

#part of speech
pos_tagged_tokens = [nltk.pos_tag(t) for t in tokens]

#Extraction
ne_chunks = ntlk.batch_ne_chunk(pos_tagged_tokens)