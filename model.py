import tensorflow as tf
import numpy as np
import model_utils

SIZE = 50
VOCABULARY_SIZE = model_utils.VOCAB_SIZE
BATCH_SIZE = 50
BUCKETS = model_utils.BUCKETS 
NUMBER_OF_LAYERS = 2
NUMBER_OF_SAMPLES = 512 
class Conversation_Model(object):
	def __init__(self, training):
		def get_cell():
			return tf.nn.rnn_cell.LSTMCell(SIZE)

		self.multicell = tf.nn.rnn_cell.MultiRNNCell([get_cell()]* NUMBER_OF_LAYERS)

		self.encoder_inputs = []
		self.decoder_inputs = []
		self.target_weights = []

		for i in range(BUCKETS[-1][0]):
			self.encoder_inputs.append(tf.placeholder(tf.int32, shape=[None],name="encoder{}".format(i)))
		for i in range(BUCKETS[-1][1]+1):
			self.decoder_inputs.append(tf.placeholder(tf.int32, shape=[None], name="decoder{}".format(i)))
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
			outputs, states = tf.nn.seq2seq.model_with_buckets(self.encoder_inputs, self.decoder_inputs, self.targets, self.target_weights, BUCKETS, lambda x, y: seq2seq_function(x, y, forward_pass), softmax_loss_function=sampled_loss)
			if forward_pass:
				for bucket in range(len(BUCKETS)):
					for i, output in enumerate(outputs[bucket]):
						outputs[bucket][i] = tf.matmul(output, output_projection[0])+output_projection[1] ##Multiplies output by weight and biases of projection
			return outputs, states
		if training:
			self.outputs, self.states = seq2seq_buckets(True)
			self.train_ops = []
			for bucket in range(len(BUCKETS)):
				self.train_ops.append(tf.train.AdamOptimizer(1e-4).minimize(self.states[bucket]))
		else:
			self.outputs, self.losses = seq2seq_buckets(False)
			
		#self.saver = tf.train.Saver()

	def step(self, i, session, give_outs):
		encoder_inputs, decoder_inputs, target_weights, bucket_id = model_utils.get_training_batch(i)
		feed_dict = {}
		for i in range(BUCKETS[bucket_id][0]):
			feed_dict[self.encoder_inputs[i].name] = encoder_inputs[i]
		for i in range(len(decoder_inputs)):
			feed_dict[self.decoder_inputs[i].name] = decoder_inputs[i]
			feed_dict[self.target_weights[i].name] = target_weights[i]
		session.run(self.train_ops[bucket_id], feed_dict=feed_dict)
		if give_outs:
			return session.run(self.outputs[bucket_id],feed_dict=feed_dict)
print("Loading Model")
model = Conversation_Model(True)
sess=tf.Session()
print("Initialising Variables")
sess.run(tf.global_variables_initializer())
print("Training")
for i in range(10):
	print(i)
	model.step(i, sess, False)
a = model.step(i, sess, True)
sentence = [int(np.argmax(a, axis=1)) for i in output]
print(sentence)
print(model_utils.translate_sentence(sentence))

