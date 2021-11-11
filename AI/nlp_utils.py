import spacy 

def get_noun_chunks (text):

   nlp = spacy.load("en_core_web_sm")
   doc = nlp(text)
   noun_chunks = doc.noun_chunks
   noun_chunks = [n for n in noun_chunks if len(n) > 2]

   noun_chunks = [str(n).replace('\n',' ') for n in noun_chunks]
   noun_chunks = [str(n).replace('\t',' ') for n in noun_chunks]
   noun_chunks = [str(n).replace('\s+',' ') for n in noun_chunks]

   return noun_chunks

