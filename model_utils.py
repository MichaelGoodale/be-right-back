import pandas as pd
import nltk
#SPECIAL VOCABULARY

VECTOR_SIZE = 100
_PAD = np.ones(VECTOR_SIZE)
_EOS = np.zeros(VECTOR_SIZE)
_UNK = np.ones(VECTOR_SIZE)*3
VOCAB_SIZE = 400000+3 #SIZE of GloVe Corpus and special vocab

def tokenize_sentence(sentence):
	tokens = nltk.word_tokenize(sentence)
	cur = get_db().cursor()
	sentence = in_sentence.lower().strip()
	word_arr = nltk.word_tokenize(sentence)
	sentence = []
	for i, word in enumerate(word_arr):
		word_string = (word,)
		cur.execute("SELECT * FROM glove WHERE field1=?", word_string)
		row = cur.fetchone()
		if row is None:
			sentence.append(_UNK)
		else:
			sentence.append(np.array(row[1:]).astype(np.float32))

def get_training_batch(VECTOR_SIZE, BATCH_SIZE):
	
	return np.zeros
	
