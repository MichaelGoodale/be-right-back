import tensorflow as tf
import numpy as np
import model_utils

SIZE = 512
VOCABULARY_SIZE = model_utils.VOCAB_SIZE
BATCH_SIZE = 50
BUCKETS =  [(5,10), (10,15), (20,25), (40,50)]
NUMBER_OF_LAYERS = 2
NUMBER_OF_SAMPLES = 512 

cell = tf.nn.rnn_cell.LSTMCell(SIZE)
multi_cell = tf.nn.rnn_cell.MultiRNNCell([cell]* NUMBER_OF_LAYERS)

encoder_inputs = []
decoder_inputs = []
target_weights = []

for i in range(BUCKETS[-1][1]):
	encoder_inputs.append(tf.placeholder(tf.int64, shape=[None]))
for i in range(BUCKETS[-1][0]):
	decoder_inputs.append(tf.placeholder(tf.int64, shape=[None]))
	target_weights.append(tf.placeholder(tf.float32, shape=[None]))
targets = [decoder_inputs[i+1] for i in range(BUCKETS[-1][0]-1)]

w = tf.get_variable("proj_w", [size, self.target_vocab_size])
w_t = tf.transpose(w)
b = tf.get_variable("proj_b", [self.target_vocab_size])
output_projection = (w, b)
def sampled_loss(inputs, labels):
	labels = tf.reshape(labels, [-1, 1])
	return tf.nn.sampled_softmax_loss(w_t, b, inputs, labels, NUMBER_OF_SAMPLES, VOCABULARY_SIZE)


def seq2seq(feed_previous):
	return tf.nn.seq2seq.embedding_rnn_seq2seq(encoder_inputs, decoder_inputs, cell, num_encoder_symbols=VOCABULARY_SIZE, num_decoder_symbols=VOCABULARY_SIZE, embedding_size=SIZE,feed_previous=feed_previous, dtype=tf.float32)


sess=tf.Session()
sess.run(tf.global_variables_initializer())
trains_ops = []
#for bucket in range(len(BUCKETS))
#	trains_ops.append(tf.train.AdamOptimizer(1e-4).minimize(losses[bucket])

