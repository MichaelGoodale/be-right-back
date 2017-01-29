import pandas as pd
import nltk
import sqlite3
import string
import numpy as np
#SPECIAL VOCABULARY
BUCKETS = [(10,15),(20,30),(30,40)]
GO = np.array([1],dtype=np.int32)
PAD = np.array([0],dtype=np.int32)
EOS = np.array([0],dtype=np.int32)
UNK = np.array([2],dtype=np.int32)
VOCAB_SIZE = 400000+3 #SIZE of GloVe Corpus and special vocab
conn = sqlite3.connect("f2db_out.db")
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
			trans_sentence.append("ERRORWORD")
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
	
def get_training_batch(step, BATCH_SIZE):
	reset_epoch = False
	speakerOne = c_dialog.execute("SELECT dialog FROM conversation WHERE speaker='0' LIMIT ?,?",(BATCH_SIZE*step,BATCH_SIZE*(step+1)))
	speakerOneSentences = [tokenize_sentence(i[0]) for i in speakerOne.fetchall()]
	speakerTwo = c_dialog.execute("SELECT dialog FROM conversation WHERE speaker='1' LIMIT ?,?",(BATCH_SIZE*step,BATCH_SIZE*(step+1)))
	speakerTwoSentences = [tokenize_sentence(i[0]) for i in speakerTwo.fetchall()]
	if len(speakerOneSentences) != len(speakerTwoSentences) or len(speakerOneSentences)<BATCH_SIZE or len(speakerTwoSentences)<BATCH_SIZE:
		if len(speakerOneSentences) < len(speakerTwoSentences):
			speakerTwoSentences=speakerTwoSentences[0:len(speakerOneSentences)]
		else:
			speakerOneSentences=speakerOneSentences[0:len(speakerTwoSentences)]
		reset_epoch = True
		BATCH_SIZE = len(speakerOneSentences)
	bucket_id=0
	encode_inputz = []
	decode_inputz = []
	target_weightz = []
	for j in range(BATCH_SIZE):
		encode_inputs = speakerOneSentences[j]
		decode_inputs = speakerTwoSentences[j]
		lengths = (len(encode_inputs), len(decode_inputs))
		for i in range(len(BUCKETS)):
			if lengths[0] <= BUCKETS[bucket_id][0] and lengths[1] < BUCKETS[bucket_id][1]:
				break
			else: 
				bucket_id = i+1
		if bucket_id >= len(BUCKETS): bucket_id = len(BUCKETS)-1
		if lengths[0] > BUCKETS[bucket_id][0] or lengths[1] > BUCKETS[bucket_id][1]:
			speakerOneSentences[j] = speakerOneSentences[j][0:BUCKETS[bucket_id][0]]
			speakerTwoSentences[j] = speakerTwoSentences[j][0:BUCKETS[bucket_id][1]]		
	for j in range(BATCH_SIZE):
		encode_inputs = speakerOneSentences[j]
		decode_inputs = speakerTwoSentences[j]
		lengths = (len(encode_inputs), len(decode_inputs))
		en_pad = [PAD]*(BUCKETS[bucket_id][0]-lengths[0])
		encode_input = list(reversed(encode_inputs+en_pad))
		de_pad = [PAD]*(BUCKETS[bucket_id][1]-lengths[1])
		decode_input = [GO]+decode_inputs+de_pad
		target_weights = []
		for i in range(len(decode_input)):
			if decode_input[i] == PAD:
				target_weights.append(np.array([0]))
			else:
				target_weights.append(np.array([1]))
		if len(encode_inputz)==0:
			encode_inputz = encode_input
			decode_inputz = decode_input
			target_weightz = target_weights
		else:
			for i in range(len(encode_input)):
				encode_inputz[i] = np.concatenate((encode_inputz[i],encode_input[i]))
			for i in range(len(decode_input)):
				decode_inputz[i] = np.concatenate((decode_inputz[i],decode_input[i]))
				target_weightz[i] = np.concatenate((target_weightz[i],target_weights[i]))
	return encode_inputz, decode_inputz, target_weightz, bucket_id, reset_epoch
