from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


# width = 30
# height = 30
# font_path = "ocr\chinese_fonts\DroidSansFallbackFull.ttf"
# # char = '\u4e01'
# char = u'王'
# img = Image.new("RGB", (width, height), "black") # 黑色背景
# draw = ImageDraw.Draw(img)
# font = ImageFont.truetype(font_path, int(width * 0.9),)
# # 白色字体
# draw.text((0, 0), char, (255, 255, 255),
#             font=font)
# img.save("./a.jpg")

# word2dict = {}
# def open_word2dict(file_dir):
#     f = open(file_dir, 'r')

# --out_dir ./dataset --font_dir ./chinese_fonts --width 30 --height 30

# wod = []
# wod.extend([chr(i) for i in range(65,91)])
# wod.extend([chr(i)for i in range(97,123)])
# wod.extend([chr(i)for i in range(48,58)])


# for i,w in zip(list(range(3755,3755+10+26+26)), wod):
#     print(i, w)


# for i in range(2):

# #     print("sI3753\n
# #             V\u9f9a
# #             p3754")
# 796 p
# 3797 q
# 3798 r
# 3799 s
# 3800 t


def get_label_dict():
    label_dict = {}
    f = open('./done.txt','r')
    for v in f:
        index, key = v.split()
        label_dict[int(index)]= key
    
    print(label_dict)
   
    # return label_dict

label_dict = get_label_dict()
# print(label_dict)

def build_graph(top_k):
    keep_prob = tf.placeholder(dtype=tf.float32, shape=[], name='keep_prob') # dropout打开概率
    images = tf.placeholder(dtype=tf.float32, shape=[None, 64, 64, 1], name='image_batch')
    labels = tf.placeholder(dtype=tf.int64, shape=[None], name='label_batch')
    is_training = tf.placeholder(dtype=tf.bool, shape=[], name='train_flag')
    with tf.device('/gpu:5'):
    # network: conv2d->max_pool2d->conv2d->max_pool2d->conv2d->max_pool2d->conv2d->conv2d->
    # max_pool2d->fully_connected->fully_connected
    #给slim.conv2d和slim.fully_connected准备了默认参数：batch_norm
    with slim.arg_scope([slim.conv2d, slim.fully_connected],
    normalizer_fn=tf.layers.batch_normalization,
    normalizer_params={'training': is_training}):
    conv3_1 = slim.conv2d(images, 64, [3, 3], 1, padding='SAME', scope='conv3_1')
    max_pool_1 = slim.max_pool2d(conv3_1, [2, 2], [2, 2], padding='SAME', scope='pool1')
    conv3_2 = slim.conv2d(max_pool_1, 128, [3, 3], padding='SAME', scope='conv3_2')
    max_pool_2 = slim.max_pool2d(conv3_2, [2, 2], [2, 2], padding='SAME', scope='pool2')
    conv3_3 = slim.conv2d(max_pool_2, 256, [3, 3], padding='SAME', scope='conv3_3')
    max_pool_3 = slim.max_pool2d(conv3_3, [2, 2], [2, 2], padding='SAME', scope='pool3')
    conv3_4 = slim.conv2d(max_pool_3, 512, [3, 3], padding='SAME', scope='conv3_4')
    conv3_5 = slim.conv2d(conv3_4, 512, [3, 3], padding='SAME', scope='conv3_5')
    max_pool_4 = slim.max_pool2d(conv3_5, [2, 2], [2, 2], padding='SAME', scope='pool4')

    flatten = slim.flatten(max_pool_4)
    fc1 = slim.fully_connected(slim.dropout(flatten, keep_prob), 1024,
                                activation_fn=tf.nn.relu, scope='fc1')
    logits = slim.fully_connected(slim.dropout(fc1, keep_prob), FLAGS.charset_size, activation_fn=None,
                                    scope='fc2')
    # 因为我们没有做热编码，所以使用sparse_softmax_cross_entropy_with_logits
    loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=labels))
    accuracy = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(logits, 1), labels), tf.float32))

    # update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
    # if update_ops:
    #     updates = tf.group(*update_ops)
    #     loss = control_flow_ops.with_dependencies([updates], loss)

    global_step = tf.get_variable("step", [], initializer=tf.constant_initializer(0.0), trainable=False)
    optimizer = tf.train.AdamOptimizer(learning_rate=0.01)
    # train_op = slim.learning.create_train_op(loss, optimizer, global_step=global_step)

    update_ops = tf.get_collection (tf.GraphKeys.UPDATE_OPS)
    with tf.control_dependencies (update_ops):
        train_op = optimizer.minimize (loss, global_step=global_step)

    probabilities = tf.nn.softmax(logits)

    # 绘制loss accuracy曲线
    tf.summary.scalar('loss', loss)
    tf.summary.scalar('accuracy', accuracy)
    merged_summary_op = tf.summary.merge_all()
    # 返回top k 个预测结果及其概率；返回top K accuracy
    predicted_val_top_k, predicted_index_top_k = tf.nn.top_k(probabilities, k=top_k)
    accuracy_in_top_k = tf.reduce_mean(tf.cast(tf.nn.in_top_k(probabilities, labels, top_k), tf.float32))

    predicted_val_top_1, predicted_index_top_1 = tf.nn.top_k (probabilities, k=1)
    tf.add_to_collection ('pred_network', predicted_val_top_1)
    tf.add_to_collection ('pred_network', predicted_index_top_1)

return {'images': images,
        'labels': labels,
        'keep_prob': keep_prob,
        'top_k': top_k,
        'global_step': global_step,
        'train_op': train_op,
        'loss': loss,
        'is_training': is_training,
        'accuracy': accuracy,
        'accuracy_top_k': accuracy_in_top_k,
        'merged_summary_op': merged_summary_op,
        'predicted_distribution': probabilities,
        'predicted_index_top_k': predicted_index_top_k,
        'predicted_val_top_k': predicted_val_top_k}