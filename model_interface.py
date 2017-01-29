import model
import tensorflow as tf
conv_model = model.Conversation_Model(True)
sess = tf.Session()
conv_model.saver.restore(sess, './the-model')

def get_reply(sentence):
	sentence_arr = conv_model.inference(sentence, sess)
	return ' '.join(sentence_arr)



