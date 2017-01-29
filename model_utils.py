import pandas as pd
import nltk
import sqlite3
import string
import numpy as np
#SPECIAL VOCABULARY
BUCKETS = [(10,15),(20,30)]
GO = np.array([1],dtype=np.int32)
PAD = np.array([0],dtype=np.int32)
EOS = np.array([0],dtype=np.int32)
UNK = np.array([2],dtype=np.int32)
VOCAB_SIZE = 10002 #SIZE of GloVe Corpus and special vocab
conn = sqlite3.connect("word.db")
c = conn.cursor()
conn_dialog = sqlite3.connect("pcorn_out.db")
c_dialog = conn_dialog.cursor()

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
			sentence.append(np.array([word_id[0]]).astype(np.int32))
	return sentence

def translate_sentence(sentence):
	trans_sentence = []
	for i in sentence:
		a = c.execute("SELECT word FROM word_list WHERE id=?", (i, ))
		word = a.fetchone()
		if word is None:
			trans_sentence.append(" ")
		else:
			trans_sentence.append(word[0])
	return trans_sentence

def get_inf_sentence(sentence):
	sentence = tokenize_sentence(sentence)
	bucket_id = 0 
	for i in range(len(BUCKETS)):
		if len(sentence) <= BUCKETS[bucket_id][0]:
			break
		else: 
			bucket_id = i+1
	if bucket_id >= len(BUCKETS): bucket_id = len(BUCKETS)-1
	if len(sentence) > BUCKETS[bucket_id][0]:
		sentence = sentence[0:BUCKETS[bucket_id][0]]
	encode_inputs = sentence
	en_pad = [PAD]*(BUCKETS[bucket_id][0]-len(sentence))
	encode_input = list(reversed(encode_inputs+en_pad))
	return encode_input, bucket_id
	
def get_training_batch(step):
	reset_epoch = False
	speakerOne = c_dialog.execute("SELECT dialog FROM conversation WHERE speaker='0' LIMIT ?,?",(step,(step+1)))
	speakerTwo = c_dialog.execute("SELECT dialog FROM conversation WHERE speaker='1' LIMIT ?,?",(step,(step+1)))
	bucket_id=0
	encode_inputs = speakerOne.fetchone()
	decode_inputs = speakerTwo.fetchone()
	if encoder_inputs is None or decode_inputs is None:
		return False
	encode_inputs = tokenize_sentence(encode_inputs[0])
	decode_inputs = tokenize_sentence(decode_inputs[1])
	if(len(encode_inputs)>BUCKETS[0][0] or len(decode_inputs)>BUCKETS[0][1]:
		bucket_id = 1
	if(len(encode_inputs)>BUCKETS[1][0]: encode_inputs=encode_inputs[0:BUCKETS[1][0]]
	if(len(decode_inputs)>BUCKETS[1][1]: decode_inputs=decode_inputs[0:BUCKETS[1][1]]
	lengths = (len(encode_inputs), len(decode_inputs))
	en_pad = [PAD]*(BUCKETS[bucket_id][0]-lengths[0])
	encode_input = list(encode_inputs+en_pad)
	de_pad = [PAD]*(BUCKETS[bucket_id][1]-lengths[1])
	decode_input = [GO]+decode_inputs+de_pad
	target_weights = []
	for i in range(len(decode_input)):
		if decode_input[i] == PAD:
			target_weights.append(np.array([0]))
		else:
			target_weights.append(np.array([1]))
	return encode_input, decode_input, target_weights, bucket_id, reset_epoch
