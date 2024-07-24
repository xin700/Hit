"""
@Project ：test
@File    ：rotate.py
@IDE     ：PyCharm
@Author  ：xin700
@Date    ：2024/7/23 10:16
"""

import cv2
from func import *


def rotate(image):
    image_original = image.copy()
    sharpen_kernel = np.array([[-1, -1, -1],
                               [-1, 9, -1],
                               [-1, -1, -1]])

    enhanced_image = cv2.filter2D(image, -1, sharpen_kernel)

    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    width = image.shape[1]
    height = image.shape[0]
    # print(f'width:{width},height:{height}')

    x_list = []
    for i in range(500):
        x_list.append(random.randint(0, width - 1))

    x_list.sort()
    x_list = list(set(x_list))
    data_list = []
    top_points = []
    bottom_points = []

    for x in x_list:

        y_top, y_bottom, length = (0, 0, 0)
        for y in range(height):
            if image[y, x] != 255:
                y_top = y
                break

        for y in range(height - 1, 0, -1):
            if image[y, x] != 255:
                y_bottom = y
                break
        length = abs(y_top - y_bottom)
        data_list.append((y_top, y_bottom, length))
        top_points.append((x, y_top))
        bottom_points.append((x, y_bottom))

        # visible
        # cv2.rectangle(image, (x, 0), (x, height), (0, 0, 0), 1)

    points = top_points

    image_clone = image.copy()
    points = np.array(points)
    x = points[:, 0]
    y = points[:, 1]
    A = np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(A, y, rcond=None)[0]

    return rotate_image4horizonal(-m, image_original)


image = cv2.imread('/Users/xin/Desktop/HIT/240719/线1/20240719180419654.bmp', cv2.IMREAD_GRAYSCALE)

image_clone = image.copy()

image = rotate(image.copy())

cv2.imshow('image',image_clone)
cv2.waitKey(0)
cv2.imshow('image',image)
cv2.waitKey(0)
cv2.destroyAllWindows()