import tensorflow as tf
import os
import numpy as np
from PIL import Image
import random


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def conv_2d(x, w):
    return tf.nn.conv2d(x, w, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                          strides=[1, 2, 2, 1], padding='SAME')


def get_files(filename):  # 提取文件夹下文件名、目录
    class_train = []
    label_train = []
    word = 'ABCDEFGHJKLMNPRSTUVWXYZ'
    word = list(word)
    word_dirt = {}
    for i in range(len(word)):
        word_dirt[word[i]] = i
    for train_class in os.listdir(filename):
        for pic in os.listdir(filename + '/' + train_class):
            class_train.append(filename + '/' + train_class + '/' + pic)
            label_train.append(train_class)
    temp = np.array([class_train, label_train])
    temp = temp.transpose()
    # after transpose, images is in dimension 0 and label in dimension 1
    image_list = list(temp[:, 0])
    label_list = list(temp[:, 1])
    label_list = [word_dirt[i] for i in label_list]
    # print(label_list)
    return image_list, label_list


def batches(image_path, label):  # 生成cnn标签数据
    x = []
    for path, i in zip(image_path, label):
        image = np.array(Image.open(path).convert('L'))
        image_list = []
        rows = image.shape[0]
        cols = image.shape[1]
        image = abs(255 - image)
        max_px = np.max(image)
        for row in range(rows):
            for col in range(cols):
                image_list.append(image[row, col] / max_px)
        image_list.insert(0, i)
        x.append(image_list)
    return x


def get_batches(batches):
    x = []
    y = []
    for iter in batches:
        out = [0 for i in range(23)]
        out[iter[0]] = 1
        y.append(out)
        x.append(iter[1:])
    return np.array(x), np.array(y)


def get_batche(batches, num):
    batch = random.sample(batches, num)
    x = []
    y = []
    for iter in batch:
        out = [0 for i in range(23)]
        out[iter[0]] = 1
        y.append(out)
        x.append(iter[1:])
    return np.array(x), np.array(y)


