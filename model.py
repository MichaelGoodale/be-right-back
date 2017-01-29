import tensorflow as tf
import numpy as np
import model_utils

SIZE = 512
VOCABULARY_SIZE = model_utils.VOCAB_SIZE
BATCH_SIZE = 50
BUCKETS = model_utils.BUCKETS 
NUMBER_OF_LAYERS = 2
NUMBER_OF_SAMPLES = 512 
class ConversationModel(object):
	def __init__(self, training):
		def get_cell():
			return tf.nn.rnn_cell.LSTMCell(SIZE)

		self.multicell = tf.nn.rnn_cell.MultiRNNCell([get_cell()]* NUMBER_OF_LAYERS)

		self.encoder_inputs = []
		self.decoder_inputs = []
		self.target_weights = []

		for i in range(BUCKETS[-1][0]):
			self.encoder_inputs.append(tf.placeholder(tf.int64, shape=[None],name="encoder{}".format(i)))
		for i in range(BUCKETS[-1][1]+1):
			self.decoder_inputs.append(tf.placeholder(tf.int64, shape=[None], name="decoder{}".format(i)))
			self.target_weights.append(tf.placeholder(tf.float32, shape=[None], name="tar_weight{}".format(i)))
		self.targets = [self.decoder_inputs[i+1] for i in range(BUCKETS[-1][1])]

		w = tf.get_variable("project_weights", [SIZE, VOCABULARY_SIZE])
		w_t = tf.transpose(w)
		b =  tf.get_variable("project_biases", [VOCABULARY_SIZE])
		output_projection = (w, b)

		def sampled_loss(inputs, labels):
			inputs = tf.cast(inputs, tf.float32)
			labels = tf.cast(tf.reshape(labels, [-1, 1]), tf.float32)
		return tf.nn.sampled_softmax_loss(w_t, b, inputs, labels, NUMBER_OF_SAMPLES, VOCABULARY_SIZE)


		def seq2seq_function(encoder_inputs, decoder_inputs, feed_previous):
			return tf.nn.seq2seq.embedding_attention_seq2seq(encoder_inputs, decoder_inputs, self.multicell, 
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
		if training:
			self.outputs, self.losses = seq2seq_buckets(True)
			self.train_ops = []
			for bucket in range(len(BUCKETS)):
				self.train_ops.append(tf.train.AdamOptimizer(1e-4).minimize(states[bucket]))
		else:
			self.outputs, self.losses = seq2seq_buckets(False)
			
		self.saver = tf.train.Saver()

	def step(self, i, session):
		encoder_inputs, decoder_inputs, target_weights, bucket_id = model_utils.get_batch(i)
		feed_dict = {}
		for i in range(BUCKETS[bucket_id][0]):
			feed_dict[encoder_inputs[i].name] = np.array([i])
		for i in range(BUCKETS[bucket_id][1]):	
			feed_dict[decoder_inputs[i].name] = np.array([i])
			feed_dict[target_weights[i].name] = np.array([i])
		feed_dict[decoder_inputs[BUCKET[bucket_id][1]+1]] = model_utils.EOS
		session.run(self.train_ops[bucket_id], feed_dict=feed_dict)

model = Conversation_Model(True)
sess=tf.Session()
sess.run(tf.global_variables_initializer())
for i in range(10):
	model.step(i, sess)
sentence = [int(np.argmax(i, axis=1)) for i in output]
print(sentence)
