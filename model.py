import tensorflow as tf
import numpy as np
import model_utils

SIZE = 512
VOCABULARY_SIZE = model_utils.VOCAB_SIZE
BATCH_SIZE = 50
BUCKETS =  [(5,10),(20,30),(40,50)]
NUMBER_OF_LAYERS = 2
NUMBER_OF_SAMPLES = 512 

def get_cell():
	return tf.nn.rnn_cell.LSTMCell(SIZE)

multi_cell = tf.nn.rnn_cell.MultiRNNCell([get_cell()]* NUMBER_OF_LAYERS)

encoder_inputs = []
decoder_inputs = []
target_weights = []

for i in range(BUCKETS[-1][0]):
	encoder_inputs.append(tf.placeholder(tf.int64, shape=[None],name="encoder{}".format(i)))
for i in range(BUCKETS[-1][1]+1):
	decoder_inputs.append(tf.placeholder(tf.int64, shape=[None], name="decoder{}".format(i)))
	target_weights.append(tf.placeholder(tf.float32, shape=[None], name="tar_weight{}".format(i)))
targets = [decoder_inputs[i+1] for i in range(BUCKETS[-1][1])]

w = tf.get_variable("project_weights", [SIZE, VOCABULARY_SIZE])
w_t = tf.transpose(w)
b =  tf.get_variable("project_biases", [VOCABULARY_SIZE])
output_projection = (w, b)

def sampled_loss(inputs, labels):
	inputs = tf.cast(inputs, tf.float32)
	labels = tf.cast(tf.reshape(labels, [-1, 1]), tf.float32)
	return tf.nn.sampled_softmax_loss(w_t, b, inputs, labels, NUMBER_OF_SAMPLES, VOCABULARY_SIZE)


def seq2seq_function(encoder_inputs, decoder_inputs, feed_previous):
	return tf.nn.seq2seq.embedding_attention_seq2seq(encoder_inputs, decoder_inputs, multi_cell, 
		num_encoder_symbols=VOCABULARY_SIZE, 
		num_decoder_symbols=VOCABULARY_SIZE,
		embedding_size=SIZE, 
		feed_previous=feed_previous,
		output_projection=output_projection,
		dtype=tf.float32)

def seq2seq_buckets(forward_pass):
	outputs, states = tf.nn.seq2seq.model_with_buckets(encoder_inputs, decoder_inputs, targets, target_weights, BUCKETS, lambda x, y: seq2seq_function(x, y, forward_pass), softmax_loss_function=sampled_loss)
	if forward_pass:
		for bucket in range(len(BUCKETS)):
			for i, output in enumerate(outputs[bucket]):
				outputs[bucket][i] = tf.matmul(output, output_projection[0])+output_projection[1] ##Multiplies output by weight and biases of projection
	return outputs, states
outputs, states = seq2seq_buckets(True)
train_ops = []
for bucket in range(len(BUCKETS)):
	train_ops.append(tf.train.AdamOptimizer(1e-4).minimize(states[bucket]))
feed_dict = {}
for i in range(5):
	feed_dict[encoder_inputs[i].name] = np.array([i])
for i in range(11):	
	feed_dict[decoder_inputs[i].name] = np.array([i])
	feed_dict[target_weights[i].name] = np.array([i])
sess=tf.Session()
sess.run(tf.global_variables_initializer())
sess.run(train_ops[0], feed_dict=feed_dict)
output = sess.run(outputs[0], feed_dict=feed_dict)
sentence = [int(np.argmax(i, axis=1) for i in output)]
print(sentence)

#for bucket in range(len(BUCKETS))
#	trains_ops.append(tf.train.AdamOptimizer(1e-4).minimize(losses[bucket])

