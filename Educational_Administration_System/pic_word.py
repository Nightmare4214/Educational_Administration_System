import cv2
import os
import improcessing as im
import numpy as np
import tensorflow as tf
import tf_tools as tf_t

word_count = {}


if __name__ == '__main__':
    dir_path = './imgcode2'
    save_path = './pic'
    if not os.path.exists(save_path):  # 创建文件夹
        os.mkdir(save_path)
    for ch, i in zip(range(ord('A'), ord('Z') + 1), range(26)):  # 创建分类文件夹
        word_count[chr(ch)] = 0
        path = save_path + '/' + chr(ch)
        if not os.path.exists(path):
            os.mkdir(path)
    error_path = save_path + '/error'
    if not os.path.exists(error_path):  # 创建错误文件夹
        os.mkdir(error_path)
    ckpt = tf.train.get_checkpoint_state('./ckpt/')
    saver = tf.train.import_meta_graph(ckpt.model_checkpoint_path + '.meta')
    print(ckpt.model_checkpoint_path)
    array = tf_t.get_files('./train_data')
    array = tf_t.batches(array[0], array[1])

    with tf.Session() as sess:
        saver.restore(sess, ckpt.model_checkpoint_path)
        y = tf.get_collection('pred_network')[0]
        graph = tf.get_default_graph()
        input_x = graph.get_operation_by_name('input_x').outputs[0]
        keep_prob = graph.get_operation_by_name('keep_prob').outputs[0]

        ver_num = 5
        hor_num = 8
        min_area = 5
        for file_path in os.listdir(dir_path):  # 遍历文件夹
            print(file_path + '\t->\t', end='')
            img = cv2.imread(dir_path + '\\' + file_path, flags=0)
            img = im.process(img, min_area)
            word = []

            __, wid = im.vertical(img, ver_num)
            pic = []
            cut_img = []
            error_img = 0
            for i in range(len(wid)):
                try:
                    pic.append(img[:, wid[i][0]:wid[i][0] + 9])
                    ___, hei = im.horizontal(pic[i], hor_num)
                    # print(hei)
                    cut_img.append(pic[i][hei[0][0]:hei[0][0] + 11, :])
                    save_img = cv2.copyMakeBorder(cut_img[i], 3, 2, 4, 3, cv2.BORDER_CONSTANT,
                                                  value=[255, 255, 255])
                    error_img = save_img
                    test_img = save_img.copy()
                    test_img = np.abs(255 - test_img)
                    data = test_img / np.max(test_img)
                    x = []
                    for row in range(data.shape[0]):
                        for col in range(data.shape[1]):
                            x.append(data[row, col])
                    x = np.array(np.mat(x))
                    result = sess.run(y, feed_dict={input_x: x, keep_prob: 1.0})
                    number = np.where(result == np.max(result))[1][0]
                    simple_word = im.word_number[number]  # 将结果转为字母
                    word.append(simple_word)
                    count = word_count[simple_word]
                    count += 1
                    word_count[simple_word] = count  # 计数
                    cv2.imwrite(save_path + '/' + simple_word + '/' + str(word_count[simple_word]) + '.bmp', save_img)
                # 保存图片
                except IndexError:
                    print(hei)
                    word_count[26] += 1
                    cv2.imwrite(save_path + '/error/' + str(word_count[26]) + '.bmp', error_img)
            print(''.join(word) + '\t', end='')
            print(word_count)
