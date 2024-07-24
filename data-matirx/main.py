"""
@Project ：Hit 
@File    ：main.py
@IDE     ：PyCharm 
@Author  ：xin700
@Date    ：2024/7/15 11:24
"""

from ultralytics import YOLO
import glob
import cv2
import time

model = YOLO('../models/diamond-line-grain-9-yolov10x.pt')

files = glob.glob('/Users/xin/Desktop/HIT/240719/线1/20240719180030150.bmp')

start_time = time.time()

for file in files:
    image = cv2.imread(file)
    result = model.predict(image)[0]
    boxes = result.boxes
    for box in boxes:
        x1, y1, x2, y2 = box.cpu().xyxy[0]
        cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)
    cv2.imshow('image', image)
    key = cv2.waitKey(0)
    # if key == ord('q'):
    #     break

end_time = time.time()

print(f'time:{end_time - start_time}')