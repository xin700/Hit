"""
@Project ：Hit 
@File    ：get_plot_data.py
@IDE     ：PyCharm 
@Author  ：xin700
@Date    ：2024/7/15 09:05
"""
import sys

import cv2
import numpy as np
import matplotlib.pyplot as plt
from func import *

start_point = None
end_point = None
drawing = False
map4len = 0.8625

left_lim, right_lim = 40.144, 40.344


# Callback function for mouse events
def draw_line(event, x, y, flags, param):
    global start_point, end_point, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        start_point = (x, y)
        drawing = True

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            temp_img = img.copy()
            cv2.line(temp_img, start_point, (x, y), (255, 0, 0), 1)
            cv2.imshow("image", temp_img)

    elif event == cv2.EVENT_LBUTTONUP:
        end_point = (x, y)
        drawing = False
        cv2.line(img_clone, start_point, end_point, (255, 0, 0), 1)
        cv2.imshow("image", img_clone)
        plot_line_values(start_point, end_point)


# Use plt to plot the pixel values along the line
def plot_line_values(start, end):
    line_points = get_line_points(start, end)
    values = [img[y, x] for x, y in line_points]
    values = np.array(values, dtype=np.float64)

    plt.figure()
    plt.plot(values)
    plt.title('Pixel values along the line')
    plt.xlabel('Distance along the line')
    plt.ylabel('Pixel value')
    plt.show()

    height_r = calc_height(values, left_lim)
    height_l = calc_height(values, right_lim)
    height_r = 49 + (height_r - 49) * 0.1
    height_l = 49 + (height_l - 49) * 0.1
    print(f'上边界:{round(height_r,3)}\n下边界:{round(height_l,3)}')


# Bresenham algorithm to get line_points
def get_line_points(start, end):
    points = []
    x1, y1 = start
    x2, y2 = end
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        points.append((x1, y1))
        if x1 == x2 and y1 == y2:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

    return points


# Check if the height is valid
def checker4plt(height, values, target):
    points = []
    if int(height) == height:
        for i, val in enumerate(values):
            if val == height:
                points.append(i)
        if len(points) <= 1:
            return False
        else:
            return (points[-1] - points[0]) * map4len > target
    else:
        for i, val in enumerate(values):
            if i + 1 != len(values) and (val <= height <= values[i + 1] or val >= height >= values[i + 1]):
                points.append(i)
        if len(points) <= 1:
            return False
        else:
            if values[points[0] + 1] - values[points[0]] != 0:
                left = points[0] + (height - values[points[0]]) / (values[points[0] + 1] - values[points[0]])
            else:
                left = points[0]
            if values[points[-1] - 1] - values[points[-1]] != 0:
                right = points[-1] + (height - values[points[-1]]) / (values[points[-1] - 1] - values[points[-1]])
            else:
                right = points[-1]
            return (right - left) * map4len > target


# Calculate the height answer of the line
def calc_height(values, target):
    left, right = 0, 255
    eps = 1e-6
    while right - left > eps:
        mid = (left + right) / 2
        if checker4plt(mid, values, target):
            left = mid
        else:
            right = mid
    return (left + right) / 2


img_path = '/Users/xin/Desktop/HIT/240719/线1/20240719180419654.bmp'

if len(sys.argv) > 1:
    img_path = sys.argv[1]

if len(sys.argv) > 2:
    left_lim = float(sys.argv[2]) - 0.1
    right_lim = float(sys.argv[2]) + 0.1

img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

if img is None:
    exit()

img = rotate(img)

img_clone = img.copy()

cv2.namedWindow("image")
cv2.setMouseCallback("image", draw_line)

cv2.imshow("image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
