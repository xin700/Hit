import os,shutil,glob
import random


dir_name = 'diamond-line-grain'

temp = glob.glob(f'./{dir_name}/images/val/*', recursive=True)
for file in temp:
    shutil.move(file, f'./{dir_name}/images/train/{file.split("/")[-1]}')
temp = glob.glob(f'./{dir_name}/labels/val/*', recursive=True)
for file in temp:
    shutil.move(file, f'./{dir_name}/labels/train/{file.split("/")[-1]}')

files = glob.glob(f'./{dir_name}/images/train/*', recursive=True)

files_number = len(files)

valid_number = files_number // 8

file_names = []

for file in files:
    # print(file)
    file_name = file.split('/')[-1].split('.')[0]
    suffix = file.split('/')[-1].split('.')[1]
    file_names.append((file_name,suffix))
    # print(file_name)

random.shuffle(file_names)

for i in range(valid_number):
    file_name = file_names[i][0]
    suffix = file_names[i][1]
    shutil.move(f'./{dir_name}/images/train/{file_name}.{suffix}', f'./{dir_name}/images/val/{file_name}.{suffix}')
    print(f'./{dir_name}/images/train/{file_name}.{suffix} ./{dir_name}/images/val/{file_name}.{suffix}')
    shutil.move(f'./{dir_name}/labels/train/{file_name}.txt', f'./{dir_name}/labels/val/{file_name}.txt')
    print(f'./{dir_name}/labels/train/{file_name}.txt ./{dir_name}/labels/val/{file_name}.txt')    
