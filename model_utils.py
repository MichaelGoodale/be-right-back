import pandas as pd
import nltk
#SPECIAL VOCABULARY

PAD = 0
EOS = 1
UNK = 2
VOCAB_SIZE = 4000+3 #SIZE of GloVe Corpus and special vocab

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

