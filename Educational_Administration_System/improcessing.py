#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import cv2

word_num = 'ABCDEFGHJKLMNPRSTUVWXYZ'
word_num = list(word_num)
word_number = {}
for i in range(len(word_num)):
    word_number[i] = word_num[i]


def process(img, min_area):
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)  # 全局大津二值化
    img = clear_background(img, min_area)  # 去除噪点
    return img


def mark_clear_area(img, data, col, row, dire, flag):  # dfs深度搜索 dire为记录搜索的方向
    if row >= img.shape[0] or col >= img.shape[1] or col < 0 or row < 0:
        return data
    if not flag:
        if img[row, col] == 0:
            img[row, col] = 127  # 标记像素
            data += 1  # 连通像素点数量
            # dire = 1 = 0001为上
            # dire = 2 = 0010为下
            # dire = 4 = 0100为左
            # dire = 8 = 1000为右
            if dire & 1 != 1:
                data = mark_clear_area(img, data, col, row + 1, 2, flag)  # 向上搜索
            if dire & 8 != 8:
                data = mark_clear_area(img, data, col + 1, row, 4, flag)  # 向右搜索
            if dire & 2 != 2:
                data = mark_clear_area(img, data, col, row - 1, 1, flag)  # 向下搜索
            if dire & 4 != 4:
                data = mark_clear_area(img, data, col - 1, row, 8, flag)  # 向左搜索
    else:
        if img[row, col] == 127:
            img[row, col] = 255  # 设置为背景色
            if dire & 1 != 1:
                data = mark_clear_area(img, data, col, row + 1, 2, flag)  # 向上搜索
            if dire & 8 != 8:
                data = mark_clear_area(img, data, col + 1, row, 4, flag)  # 向右搜索
            if dire & 2 != 2:
                data = mark_clear_area(img, data, col, row - 1, 1, flag)  # 向下搜索
            if dire & 4 != 4:
                data = mark_clear_area(img, data, col - 1, row, 8, flag)
    return data


def clear_background(image, num):  # 去除噪点
    for row in range(0, image.shape[0]):
        for col in range(0, image.shape[1]):
            if image[row, col] == 0:
                number = mark_clear_area(image, 0, col, row, 0, False)  # 连通数量
                # print(number)
                if number < num:
                    mark_clear_area(image, 0, col, row, 0, True)  # 消除连通区域
    for row in range(0, image.shape[0]):
        for col in range(0, image.shape[1]):
            if image[row, col] == 127:
                image[row, col] = 0
    return image


def horizontal(image, hor_num):  # 水平投影
    img = image.copy()
    (h, w) = img.shape  # 返回高和宽
    # print(h,w)#s输出高和宽
    H = [0 for z in range(0, h)]
    # 记录每一行的波峰
    for i in range(0, h):  # 遍历一行
        for j in range(0, w):  # 遍历一列
            if img[i, j] != 255:  # 如果改点为黑点
                H[i] += 1  # 该列的计数器加一计数
    Hei = []
    i = 0
    while i != h:  # 标记水平投影非0点的起始点和长度
        if H[i] != 0:
            start = i
            count = 0
            while i != h:
                if H[i] == 0:
                    break
                else:
                    count += 1
                i += 1
            Hei.append([start, count])
        else:
            i += 1

    index = 0
    while index < len(Hei):  # 去除长度小于阈值的标记
        if Hei[index][1] < hor_num:
            del Hei[index]
            index -= 1
        index += 1

    return H, Hei


def vertical(image, ver_num):  # 垂直投影
    img = image.copy()
    (h, w) = img.shape  # 返回高和宽
    # print(h,w)#s输出高和宽
    W = [0 for z in range(0, w)]
    # 记录每一列的波峰
    for j in range(0, w):  # 遍历一列
        for i in range(0, h):  # 遍历一行
            if img[i, j] != 255:  # 如果改点为黑点
                W[j] += 1  # 该列的计数器加一计数
    Wid = []
    i = 0
    while i != w:  # 标记垂直投影非0点的起始点和长度
        if W[i] != 0:
            start = i
            count = 0
            while i != w:
                if W[i] == 0:
                    break
                else:
                    count += 1
                i += 1
            Wid.append([start, count])
        else:
            i += 1

    index = 0
    while index < len(Wid):  # 去除长度小于阈值的标记
        if Wid[index][1] < ver_num:
            del Wid[index]
            index -= 1
        index += 1

    return W, Wid


if __name__ == '__main__':
    import os
    import matplotlib.pyplot as plt
    from matplotlib import animation
    import seaborn as sns
    import cv2

    dir_path = './imgcode2'
    image = cv2.imread(dir_path + '\\' + os.listdir(dir_path)[2], 0)  # 读取图片[0]为第一张图片
    _, image = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU)  # 全局大津二值化
    sns.set_style("whitegrid")  # 设置图形主图
    # 创建画布
    fig = plt.figure()
    im = plt.imshow(image, cmap='gray')
    plt.grid(False)

    def animate(i):
        for row in range(0, image.shape[0]):
            for col in range(0, image.shape[1]):
                if image[row, col] == 0:
                    number = mark_clear_area(image, 0, col, row, 0, False)  # 连通数量
                    if number < 5:
                        mark_clear_area(image, 0, col, row, 0, True)  # 消除连通区域
                    im.set_array(image)
                    return [im]

    ani = animation.FuncAnimation(fig, animate, frames=50, interval=500, blit=False)
    plt.show()
    image = clear_background(image, 5)

    w, wid = vertical(image, 5)
    plt.bar([i + 1 for i in range(len(w))], w)
    plt.show()
    error_img = 0
    fig = plt.figure()
    ax1 = fig.add_subplot(3, 4, 1)
    ax2 = fig.add_subplot(3, 4, 2)
    ax3 = fig.add_subplot(3, 4, 3)
    ax4 = fig.add_subplot(3, 4, 4)
    ax5 = fig.add_subplot(3, 4, 5)
    ax6 = fig.add_subplot(3, 4, 6)
    ax7 = fig.add_subplot(3, 4, 7)
    ax8 = fig.add_subplot(3, 4, 8)
    ax9 = fig.add_subplot(3, 4, 9)
    ax10 = fig.add_subplot(3, 4, 10)
    ax11 = fig.add_subplot(3, 4, 11)
    ax12 = fig.add_subplot(3, 4, 12)
    ax = [[ax1, ax2, ax3, ax4], [ax5, ax6, ax7, ax8], [ax9, ax10, ax11, ax12]]
    for i in range(len(wid)):
        pic = image[:, wid[i][0]:wid[i][0] + 9]
        ax[0][i].imshow(pic)
        ax[0][i].grid(False)
        h, hei = horizontal(pic, 8)
        h = h[::-1]
        ax[1][i].barh([i + 1 for i in range(len(h))], h)
        ax[1][i].grid(False)
        cut_img = pic[hei[0][0]:hei[0][0] + 11, :]
        ax[2][i].imshow(cut_img)
        ax[2][i].grid(False)
    plt.show()
