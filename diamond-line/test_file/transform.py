"""
@Project ：Hit
@File    ：transform.py
@IDE     ：PyCharm
@Author  ：xin700
@Date    ：2024/7/15 09:04
"""

import cv2
import numpy as np

# 读取图像
image = cv2.imread('testImg/04_27_16_13_33_4_OK.bmp')

# 定义选择点的回调函数
points = []


def select_point(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:
            points.append((x, y))
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
            cv2.imshow('image', image)


# 显示图像并选择四个点
cv2.imshow('image', image)
cv2.setMouseCallback('image', select_point)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 检查是否选择了四个点
if len(points) != 4:
    raise ValueError("4 points!")

# 目标平面的四个点，假设目标图像大小为300x300
pts_dst = np.array([[0, 0], [300, 0], [300, 300], [0, 300]], dtype='float32')

# 计算透视变换矩阵
pts_src = np.array(points, dtype='float32')
matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)

# 应用透视变换
transformed_image = cv2.warpPerspective(image, matrix, (300, 300))

# 显示变换后的图像
cv2.imshow('Transformed Image', transformed_image)
cv2.imwrite('testImg/transformed_image.png', transformed_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
