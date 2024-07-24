"""
@Project ：test
@File    ：get_answer.py
@IDE     ：PyCharm
@Author  ：xin700
@Date    ：2024/7/23 09:19
"""
import sys
import time
from func import *
from tqdm import tqdm

start_time = time.time()
border = 50
map4len = 0.8625

sta, end = 0, 0


def get_length(values):
    global sta, end
    sta, end = 0, 0
    left, right = 0, 0
    for i, value in enumerate(values):
        if values[i + 1] > border >= values[i]:
            left = i + (border - values[i]) / (values[i + 1] - values[i])
            sta = i
            break
    for i in range(len(values) - 1, 0, -1):
        if values[i - 1] > border >= values[i]:
            right = i + (border - values[i]) / (values[i - 1] - values[i])
            end = i
            break
    return (right - left) * map4len


def scan(image, x):
    height = image.shape[0]
    ret = []
    for y in range(height):
        ret.append(image[y, x])
    return ret


img_path = '/Users/xin/Desktop/HIT/240719/线9/20240719191256078.bmp'

if len(sys.argv) > 1:
    img_path = sys.argv[1]

img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

if img is None:
    print('img is None')
    exit()

img_clone = img.copy()
img_clone = cv2.cvtColor(img_clone, cv2.COLOR_GRAY2BGR)

img = rotate(img.copy())
print(f'图像水平矫正完毕')

img_height, img_width = img.shape

scanner_list = [i for i in range(1, img_width - 2)]

scanner_list = sorted(list(set(scanner_list)))

print(f'正在扫描图像...')

lengths = []
for x in tqdm(scanner_list, desc='扫描进度'):
    values = scan(img, x)
    lengths.append(get_length(values))
    # print(sta, end)
    cv2.circle(img_clone, (x, sta), 1, (0, 255, 0), 1)
    cv2.circle(img_clone, (x, end), 1, (0, 255, 0), 1)

lengths = np.array(lengths)

lengths = sorted(lengths)

checker_length = 10
checker_radius_front = 0.001
checker_radius_back = 0.006

length_min = 0
length_max = 0

for i in range(1, len(lengths) - checker_length - 1):
    if lengths[i + checker_length] - lengths[i] < checker_radius_front * checker_length:
        length_min = round(lengths[i], 4)
        print(f'线锯丝径：{length_min}')
        break

for i in range(len(lengths) - 1, 1 + checker_length, -1):
    if lengths[i] - lengths[i - checker_length] < checker_radius_back * checker_length:
        length_max = round(lengths[i], 4)
        print(f'包络外径：{length_max}')
        break

print(f'出刃高度：{round((length_min + length_max) / 2 - length_min, 4)}')

end_time = time.time()
print(f'用时：{round(end_time - start_time, 2)}s')
