import tensorflow as tf
import numpy as np
import model_utils

STATE_SIZE = 3 #placeholder
VECTOR_SIZE = model_utils.VECTOR_SIZE
VOCABULARY_SIZE = model_utils.VOCAB_SIZE
BATCH_SIZE = 50
BUCKETS =  [(5,10), (10,15), (20,25), (40,50)]
NUMBER_OF_LAYERS = 2

print(VOCABULARY_SIZE)
cell = tf.nn.rnn_cell.LSTMCell
multi_cell = tf.nn.rnn_cell.MultiRNNCell([cell]* NUMBER_OF_LAYERS)


