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

for i in range(BUCKETS[-1][0]):
	encoder_inputs.append(tf.placeholder(tf.int64, shape=[None]))
for i in range(BUCKETS[-1][1]):
	decoder_inputs.append(tf.placeholder(tf.int64, shape=[None]))
	target_weights.append(tf.placeholder(tf.float32, shape=[None]))
targets = [decoder_inputs[i+1] for i in range(BUCKETS[-1][0]-1)]

w = tf.Variable([SIZE, VOCABULARY_SIZE], dtype=tf.float32, name="weights")
w_t = tf.transpose(w)
b = tf.Variable([VOCABULARY_SIZE],dtype=tf.float32, name="biases")
output_projection = (w, b)

def sampled_loss(inputs, labels):
	inputs = tf.cast(inputs, tf.float32)
	labels = tf.reshape(labels, [-1, 1])
	return tf.nn.sampled_softmax_loss(weights = w_t, biases=b, labels=labels, inputs=inputs, num_sampled=NUMBER_OF_SAMPLES, num_classes=VOCABULARY_SIZE)


def seq2seq_function(x, y, feed_previous):
	return tf.nn.seq2seq.embedding_rnn_seq2seq(x, y, cell, num_encoder_symbols=VOCABULARY_SIZE, num_decoder_symbols=VOCABULARY_SIZE, embedding_size=SIZE,feed_previous=feed_previous, dtype=tf.float32)

def seq2seq_buckets(forward_pass):
	outputs, states = tf.nn.seq2seq.model_with_buckets(encoder_inputs, decoder_inputs, targets, target_weights, BUCKETS, lambda x, y: seq2seq(x, y, forward_pass), softmax_loss_function=sampled_loss)
	if forward_pass:
		for bucket in range(len(BUCKETS)):
			for i, output in enumerate(outputs[bucket]):
				outputs[i] = tf.matmul(output, output_projection[0])+output_project[1] ##Multiplies output by weight and biases of projection
	return outputs, states
forpass_seq = seq2seq_buckets(True)
sess=tf.Session()
sess.run(tf.global_variables_initializer())
trains_ops = []
#for bucket in range(len(BUCKETS))
#	trains_ops.append(tf.train.AdamOptimizer(1e-4).minimize(losses[bucket])

