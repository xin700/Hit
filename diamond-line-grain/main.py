"""
@Project ：Hit 
@File    ：main.py
@IDE     ：PyCharm 
@Author  ：xin700
@Date    ：2024/7/15 11:24
"""
import torch
from ultralytics import YOLO
import glob
import cv2
import time

model = YOLO('../models/diamond-line-newly-yolov8x-300.pt')


def get_device():
    if torch.cuda.is_available():
        device = 'cuda'
        print("CUDA is available. Using GPU.")
    elif torch.backends.mps.is_available() and torch.backends.mps.is_built():
        device = 'mps'
        print("MPS is available. Using MPS.")
    else:
        device = 'cpu'
        print("CUDA and MPS are not available. Using CPU.")

    return device


device = get_device()

files = glob.glob('/Users/xin/Desktop/HIT/240719/线6/20240719185447651.bmp')

start_time = time.time()

for file in files:
    image = cv2.imread(file)
    result = model.predict(image, conf=0.0067, iou=0.3, device=device)[0]
    boxes = result.boxes
    for box in boxes:
        x1, y1, x2, y2 = box.cpu().xyxy[0]
        cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)
    cv2.imshow('image', image)
    key = cv2.waitKey(0)
    if key == ord('q'):
        break

end_time = time.time()

print(f'time:{end_time - start_time}')