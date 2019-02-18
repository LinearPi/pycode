import tensorflow as tf
import torch 

hello = tf.constant("hello world")
sess = tf.Session()
print(sess.run(hello))
print(torch.__version__)