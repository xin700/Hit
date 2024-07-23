import cv2, re
import numpy as np
import random
import matplotlib.pyplot as plt


# 图像锐化
def enhance(image):
    sharpen_kernel = np.array([[-1, -1, -1],
                               [-1, 9, -1],
                               [-1, -1, -1]])

    enhanced_image = cv2.filter2D(image, -1, sharpen_kernel)

    return enhanced_image


# get number from filename
def extract_number_from_filename(filename):
    return int(re.findall(r'\d+', filename)[0])


# draw line by points
def draw_line_by_points(image, points, thickness=1):
    image_clone = image.copy()
    points = np.array(points)
    x = points[:, 0]
    y = points[:, 1]
    A = np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(A, y, rcond=None)[0]
    start_point = (int(0), int(c))
    # print(image.shape)
    end_point = (int(image.shape[1]), int(m * image.shape[1] + c))
    print(f'start_point:{start_point},end_point:{end_point}')
    return cv2.line(image_clone, start_point, end_point, (0, 0, 0), thickness)


# draw line by points
def show_image(image):
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# auto threshold method for processing image
def threshold4length(image):
    sharpen_kernel = np.array([[-1, -1, -1],
                               [-1, 9, -1],
                               [-1, -1, -1]])

    enhanced_image = cv2.filter2D(image, -1, sharpen_kernel)

    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    width = image.shape[1]
    height = image.shape[0]
    print(f'width:{width},height:{height}')

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
        cv2.rectangle(image, (x, 0), (x, height), (0, 0, 0), 1)

    aver_length = 0
    min_length = 0x7f7f7f7f
    max_length = 0
    for data in data_list:
        aver_length += data[2]
        min_length = min(data[2], min_length)
        max_length = max(data[2], max_length)
        # print(f'y_top:{data[0]},y_bottom:{data[1]},length:{data[2]}')

    aver_length /= len(data_list)

    print(f'aver_length is {aver_length}')
    print(f'real length is {round(aver_length * 0.8625, 4)} μm')
    print(f'min  length is {round(min_length * 0.8625, 4)} μm')
    print(f'max  length is {round(max_length * 0.8625, 4)} μm')
    print(round((aver_length + min_length) * 0.8625 / 2, 4))
    print(round((max_length + min_length) * 0.8625 / 2, 4))
    return image


def rotate_image4horizonal(m, img):
    # cv2.imshow("Original Image", img)
    # cv2.waitKey(0)

    angle = np.arctan(m) * (180.0 / np.pi)  # 角度值
    print(f'旋转了{round(angle,4)}度达到水平')

    h, w = img.shape
    center = (w / 2, h / 2)

    M = cv2.getRotationMatrix2D(center, -angle, 1.0)

    rotated_img = cv2.warpAffine(img, M, (w, h))


    # cv2.imshow("Rotated Image", rotated_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return rotated_img

def rotate(image):
    image_original = image.copy()
    sharpen_kernel = np.array([[-1, -1, -1],
                               [-1, 9, -1],
                               [-1, -1, -1]])

    enhanced_image = cv2.filter2D(image, -1, sharpen_kernel)
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    width = image.shape[1]
    height = image.shape[0]
    x_list = []
    for i in range(width // 2):
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

    points = top_points

    image_clone = image.copy()
    points = np.array(points)
    x = points[:, 0]
    y = points[:, 1]
    A = np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(A, y, rcond=None)[0]

    return rotate_image4horizonal(-m, image_original)



def hough(im):
    cv2.imshow('original', im)
    cv2.waitKey(0)

    gray_img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray', gray_img)
    cv2.waitKey(0)

    canny = cv2.Canny(gray_img, 30, 150)
    cv2.imshow('canny', canny)
    cv2.waitKey(0)

    lines = cv2.HoughLines(canny, 1, np.pi / 180, 180)
    lines1 = lines[:, 0, :]
    for rho, theta in lines1[:]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 3000 * (-b))
        y1 = int(y0 + 3000 * (a))
        x2 = int(x0 - 3000 * (-b))
        y2 = int(y0 - 3000 * (a))
        cv2.line(im, (x1, y1), (x2, y2), (0, 0, 255), 1)

    cv2.imshow('original', im)
    cv2.waitKey(0)


from pyzbar.pyzbar import decode
from PIL import Image


def decode_data_matrix(file):
    image = Image.open(file)
    decoded_objects = decode(image)

    for obj in decoded_objects:
        print('Type:', obj.type)
        print('Data:', obj.data.decode('utf-8'))


from pyzxing import BarCodeReader

def decode_data_matrix2(file):
    reader = BarCodeReader()
    result = reader.decode(file)
    print(result)

def decode(file):
    # decode_data_matrix(file)
    decode_data_matrix2(file)