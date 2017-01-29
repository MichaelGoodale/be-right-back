import model
import tensorflow as tf
conv_model = model.Conversation_Model(True)
sess = tf.Session()
#conv_model.saver.restore(sess, './the-model')
sess.run(tf.global_variables_initializer())
i=0
for fake_num in range(1):
	print(fake_num)
	reset_epoch = model.step(i, sess, False)
	i=i+1
	if reset_epoch: i = 0
model.saver.save(sess, 'the-model')


