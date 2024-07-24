"""
@Project ：Hit 
@File    ：get_plot_data.py
@IDE     ：PyCharm 
@Author  ：xin700
@Date    ：2024/7/15 09:05
"""

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
    print(f'height_r:{height_r},height_l:{height_l}')


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
    # print(f'height:{height}')
    points = []
    if int(height) == height:
        for i, val in enumerate(values):
            if val == height:
                points.append(i)
        if len(points) <= 1:
            # print('1111111111111111111 False')
            return False
        else:
            # print(f'2222222222222222222 {bool((points[-1] - points[0]) * map4len > target)}')
            return (points[-1] - points[0]) * map4len > target
    else:
        for i, val in enumerate(values):
            if i + 1 != len(values) and (val <= height <= values[i + 1] or val >= height >= values[i + 1]):
                points.append(i)
        if len(points) <= 1:
            # print('3333333333333333333 False')
            return False
        else:
            if values[points[0] + 1] - values[points[0]] != 0:
                left = points[0] + (height - values[points[0]]) / (values[points[0] + 1] - values[points[0]])
            else:
                left = points[0]
            # print(f'points[0]:{points[0]},points[-1]:{points[-1]}')
            if values[points[-1] - 1] - values[points[-1]] != 0:
                right = points[-1] + (height - values[points[-1]]) / (values[points[-1] - 1] - values[points[-1]])
            else:
                right = points[-1]
            # print(f'values[points[0]]:{values[points[0]]},values[points[0] + 1]:{values[points[0] + 1]}')
            # print(f'values[points[-1]]:{values[points[-1]]},values[points[-1] - 1]:{values[points[-1] - 1]}')
            # print(f'points[0]:{points[0]},points[-1]:{points[-1]}')
            # print(f'len(values){len(values)} len(points){len(points)}')
            # print(f'left:{left},right:{right},right-left:{right - left}')
            # print(f'4444444444444444444{bool((right - left) * map4len > target)}')
            return (right - left) * map4len > target


# Calculate the height answer of the line
def calc_height(values, target):
    left, right = 0, 255
    eps = 1e-6
    while right - left > eps:
        # print(f'left:{left},right:{right}')
        mid = (left + right) / 2
        if checker4plt(mid, values, target):
            left = mid
        else:
            right = mid
        # print(f'\n\n')
    return (left + right) / 2


img = cv2.imread('/Users/xin/Desktop/HIT/240719/线1/20240719180419654.bmp', cv2.IMREAD_GRAYSCALE)

if img is None:
    exit()

img = rotate(img)

img_clone = img.copy()

cv2.namedWindow("image")
cv2.setMouseCallback("image", draw_line)

cv2.imshow("image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
