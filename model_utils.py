import pandas as pd
import nltk
import sqlite3
import string
import numpy as np
#SPECIAL VOCABULARY
BUCKETS = [(5,10),(20,30),(40,50)]
GO = np.array([-1],dtype=np.int32)
PAD = np.array([0],dtype=np.int32)
EOS = np.array([1],dtype=np.int32)
UNK = np.array([2],dtype=np.int32)
VOCAB_SIZE = 4000+3 #SIZE of GloVe Corpus and special vocab
conn = sqlite3.connect("f2db_out.db")
c = conn.cursor()


def tokenize_sentence(sentence):
	sentence = sentence.lower().strip().translate(dict.fromkeys(map(ord, string.punctuation)))
	word_arr = nltk.word_tokenize(sentence)
	sentence = []
	for i, word in enumerate(word_arr):
		row = c.execute("SELECT id FROM word_list WHERE word=?", (word, ))
		word_id = row.fetchone()
		if word_id is None:
			sentence.append(UNK)
		else:
			sentence.append(np.array(word_id[0]).astype(np.int32))
	return sentence
def get_training_batch(i):
	encode="this is an intro sentence"
	decode="this is an outro sentence"
	encode_inputs = tokenize_sentence(encode)
	decode_inputs = tokenize_sentence(decode)
	lengths = (len(encode_inputs), len(decode_inputs))
	bucket_id = 0
	for i in range(len(BUCKETS)):
		if lengths[0] <= BUCKETS[i][0] and lengths[1] < BUCKETS[i][1]:
			break
			print(BUCKETS[i][0])
			print(BUCKETS[i][1])
			print(lengths)
		else: 
			bucket_id = i+1	
	#if lengths > bucket_id:
		#TODO make clamp long sentences to max bucket
	en_pad = [PAD]*(BUCKETS[bucket_id][0]-lengths[0])
	encode_input = list(reversed(encode_inputs+en_pad))
	de_pad = [PAD]*(BUCKETS[bucket_id][1]-lengths[1]-1)
	decode_input = [GO]+decode_inputs+de_pad
	target_weights = np.ones([len(decode_input)])
	for i in range(len(decode_input)):
		if decode_input[i] == PAD:
			target_weights[i] = 0
	return encode_input, decode_input, target_weights, bucket_id

