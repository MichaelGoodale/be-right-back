import pandas as pd
import nltk
import sqlite3
import string
import numpy as np
#SPECIAL VOCABULARY
BUCKETS = [(5,10),(20,30),(40,50)]
GO = np.array[-1]
PAD = np.array([0])
EOS = np.array([1])
UNK = np.array([2])
VOCAB_SIZE = 4000+3 #SIZE of GloVe Corpus and special vocab
conn = sqlite3.connect("f2db_out.db")
c = conn.cursor()


def tokenize_sentence(sentence):
	sentence = sentence.lower().strip().translate(dict.fromkeys(map(ord, string.punctuation)))
	word_arr = nltk.word_tokenize(sentence)
	sentence = []
	print(word_arr)
	for i, word in enumerate(word_arr):
		row = c.execute("SELECT id FROM word_list WHERE word=?", (word, ))
		word_id = row.fetchone()
		if word_id is None:
			sentence.append(UNK)
		else:
			sentence.append(np.array(word_id[0]).astype(np.float32))
	print(sentence)
def get_training_batch(i):
	encode="this is an intro sentence"
	decode="thise is an outro sentence"
	encode_inputs = tokenize_sentence(encode)
	decode_inputs = tokenize_sentence(decode)
	lengths = (len(encode_input), len(decode_inputs))
	bucket_id = 0
	for i in range(len(BUCKETS)):
		if lengths < BUCKETS[i]:
			break
		else 
			bucket_id = i	
	if lengths > bucket_id:
		#TODO make clamp long sentences to max bucket
	en_pad = [PAD]*(lengths[0]-BUCKETS[bucket_id][0])
	encode_input = reversed(encode_inputs+en_pad)
	de_pad = [PAD]*(lengths[1]-BUCKETS[bucket_id][1]-1)
	decode_input = [GO]+decode_inputs+de_pad
	

		
