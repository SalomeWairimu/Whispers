from collections import defaultdict
from gensim import corpora
from gensim import models
from gensim import similarities
import uuid
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

from cloud.integrated import *

# Retrieve all (id,audio_text) for all audios on the current pi.
def retrieve_audio_texts():
    piId = hex(uuid.getnode())
    audio_ids, audio_texts = retrieveByRasberryPiId(hex(uuid.getnode()))
    return audio_ids, audio_texts

# Clean up text by removing stop words and words that may not be relevant.
def clean_audio_texts(documents):
    # remove common words and tokenize
    stoplist = set('for a of the and to in'.split())
    # stop_words_nltk = set(stopwords.words('english'))
    texts = [
        [word for word in document.lower().split() if word not in stoplist]
        for document in documents
    ]

    # remove words that appear only once
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    texts = [
        [token for token in text if frequency[token] > 1]
        for text in texts
    ]
    return texts

def create_lsi_model(texts):
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)
    return dictionary, corpus, lsi

def get_best_answer_audio_id(question):
    # Retrieve all texts related to the current art piece.
    audio_ids, audio_texts = retrieve_audio_texts()
    texts = clean_audio_texts(audio_texts)
    dictionary, corpus, lsi = create_lsi_model(texts)
    vec_bow = dictionary.doc2bow(question.lower().split())
    vec_lsi = lsi[vec_bow]  # convert the query to LSI space
    index = similarities.MatrixSimilarity(lsi[corpus])
    index.save('/tmp/deerwester.index')
    index = similarities.MatrixSimilarity.load('/tmp/deerwester.index')
    sims = index[vec_lsi]  # perform a similarity query against the corpus
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    #print(sims)
    for i, s in sims:
        print(s, audio_texts[i])
    return audio_ids[sims[0][0]]

#print(get_best_answer_audio_id("What was fascinating about the cat?"))