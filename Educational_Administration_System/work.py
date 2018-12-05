#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import cv2
import os
import tensorflow as tf
import tf_tools as tf_t
import improcessing as im
import numpy as np


def get_word(file_path=r'SWE16004_imgcode.jpg'):
    dir_path = '.'
    save_path = './pic2'
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    ckpt = tf.train.get_checkpoint_state('./ckpt/')
    saver = tf.train.import_meta_graph(ckpt.model_checkpoint_path + '.meta')
    # array = tf_t.get_files('./train_data')
    # array = tf_t.batches(array[0], array[1])

    with tf.Session() as sess:
        saver.restore(sess, ckpt.model_checkpoint_path)
        y = tf.get_collection('pred_network')[0]
        graph = tf.get_default_graph()
        input_x = graph.get_operation_by_name('input_x').outputs[0]
        keep_prob = graph.get_operation_by_name('keep_prob').outputs[0]

        ver_num = 5  # 垂直投影阈值
        hor_num = 8  # 水平投影阈值
        min_area = 5  # 连通域面积阈值

        img = cv2.imread(dir_path + '\\' + file_path, flags=0)  # 读取图片
        img = im.process(img, min_area)

        __, wid = im.vertical(img, ver_num)  # 得到垂直投影标记
        pic = []
        cut_img = []
        test_word = ''
        datalist = []
        for i in range(len(wid)):  # 提取验证码四个字母特征点
            pic.append(img[:, wid[i][0]:wid[i][0] + 9])  # 垂直切割图像
            ___, hei = im.horizontal(pic[i], hor_num)  # 得到水平投影标记
            # print(hei)
            cut_img.append(pic[i][hei[0][0]:hei[0][0] + 11, :])  # 水平切割图像
            save_img = cv2.copyMakeBorder(cut_img[i], 3, 2, 4, 3, cv2.BORDER_CONSTANT,
                                          value=[255, 255, 255])  # 将图像大小扩充到16*16
            save_img = np.abs(255 - save_img)
            data = save_img / np.max(save_img)
            xt = []
            for row in range(data.shape[0]):
                for col in range(data.shape[1]):
                    xt.append(data[row, col])
            datalist.append(xt)
        x = np.array(datalist)
        result = sess.run(y, feed_dict={input_x: x, keep_prob: 1.0})
        for iter in result:
            i = np.where(iter == np.max(iter))[0][0]
            test_word += im.word_number[i]  # 将结果转为字母
        return test_word
        # cv2.imwrite(save_path + '/' + test_word + '.bmp', img)  # 保存结果


if __name__ == '__main__':
    print(get_word())
