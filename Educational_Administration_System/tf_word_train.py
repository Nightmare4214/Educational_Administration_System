import time
import tf_tools
import tensorflow as tf


if __name__ == '__main__':

    # Create the model
    # placeholder
    x = tf.placeholder(tf.float32, shape=[None, 16*16], name='input_x')
    y_ = tf.placeholder(tf.float32, shape=[None, 23], name='input_y')

    # first

    W_conv1 = tf_tools.weight_variable([5, 5, 1, 32])
    b_conv1 = tf_tools.bias_variable([32])
    x_image = tf.reshape(x, [-1, 16, 16, 1])
    h_conv1 = tf.nn.relu(tf_tools.conv_2d(x_image, W_conv1) + b_conv1)
    h_pool1 = tf_tools.max_pool_2x2(h_conv1)

    # second
    W_conv2 = tf_tools.weight_variable([5, 5, 32, 64])
    b_conv2 = tf_tools.bias_variable([64])
    h_conv2 = tf.nn.relu(tf_tools.conv_2d(h_pool1, W_conv2) + b_conv2)
    h_pool2 = tf_tools.max_pool_2x2(h_conv2)

    W_fc1 = tf_tools.weight_variable([4 * 4 * 64, 1024])
    b_fc1 = tf_tools.bias_variable([1024])
    h_pool2_flat = tf.reshape(h_pool2, [-1, 4 * 4 * 64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

    # dropout
    keep_prob = tf.placeholder(tf.float32, name='keep_prob')
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    # softmax
    W_fc2 = tf_tools.weight_variable([1024, 23])
    b_fc2 = tf_tools.bias_variable([23])

    y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

    cross_entropy = -tf.reduce_sum(y_*tf.log(y_conv))
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
    correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    tf.add_to_collection('pred_network', y_conv)

    array = tf_tools.get_files('./train_data')
    array = tf_tools.batches(array[0], array[1])
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver(max_to_keep=1)
        time_start = time.time()
        for i in range(2000):
            batch = tf_tools.get_batche(array, 100)
            if i % 100 == 0:
                train_accuracy = accuracy.eval(feed_dict={
                    x: batch[0], y_: batch[1], keep_prob: 1.0})
                print("step %d, training accuracy %f" % (i, train_accuracy))
            train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})
        x_data, y_data = tf_tools.get_batches(array)
        print("test accuracy %g" % accuracy.eval(feed_dict={x: x_data, y_: y_data, keep_prob: 1.0}))

        time_end = time.time()
        print('totally cost ' + str(time_end-time_start) + 's')
        saver.save(sess, './ckpt/mnist.ckpt', global_step=0)
