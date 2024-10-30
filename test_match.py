# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 20:26:52 2023

@author: ljl
"""

import math
import os
import shutil


# 提取中心点坐标
def read_coordinates(file_path):
    with open(file_path, 'r') as file:
        # 读取一行数据
        line = file.readline().strip().split()

        # 提取第二个和第三个值
        if len(line) >= 3:
            coord1 = float(line[1])
            coord2 = float(line[2])
            return coord1, coord2
        else:
            # 处理数据不足的情况
            return None

# 计算两中心点坐标远近，以判断匹配图片
def calculate_distance(coord1x, coord1y, coord2x, coord2y):
    distance = math.sqrt((coord1x - coord2x)**2 + (coord1y - coord2y)**2)
    distance_with_precision = round(distance, 10)
    return distance_with_precision

# 将图片对应的坐标文档放在一起
def move_txt_and_related_images(txt_file_path, target_folder):
    # 获取txt文件所在的文件夹路径
    source_folder = os.path.dirname(txt_file_path)

    # 移动txt文件
    shutil.move(txt_file_path, os.path.join(target_folder, os.path.basename(txt_file_path)))

    # 获取txt文件的文件名（不包含扩展名）
    txt_filename = os.path.splitext(os.path.basename(txt_file_path))[0]

    # 查找同名的图片文件
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            # 如果文件名与txt文件相同（不考虑扩展名）
            image_name = os.path.splitext(file)[0]
            print(image_name)
            print(txt_filename)
            # 使用下划线作为分隔符，将字符串拆分成多个部分
            parts = image_name.split("_") 
            # 从拆分后的部分中选择需要的部分，并使用下划线重新组合成字符串
            extracted_string = "_".join(parts[:6])  # 提取前5个部分
            
            image_name = extracted_string
            print(image_name)
            if image_name == txt_filename:
                shutil.move(os.path.join(root, file), os.path.join(target_folder, file))


def find_match(input_first_path, input_second_path, outputpath_dir):
    outputpath = os.path.join(outputpath_dir,"split")
    os.makedirs(outputpath, exist_ok=True)
    
    for root1, dirs, files1 in os.walk(input_first_path):
        for file1 in files1:
            
            if file1.endswith('.txt'):
                #创建一个大文件夹
                outputpath_img = os.path.join(outputpath,file1[:10])
                os.makedirs(outputpath_img, exist_ok=True)
                
                coord1x, coord1y = read_coordinates(os.path.join(root1, file1))
                min_distance = float('inf')
                closest_pair = None

                for root2, dirs, files2 in os.walk(input_second_path):
                    for file2 in files2:
                        if file1[:10] == file2[:10] and file2.endswith('.txt'):
                            coord2x, coord2y = read_coordinates(os.path.join(root2, file2))
                            distance = calculate_distance(coord1x, coord1y, coord2x, coord2y)
                                                       
                            if distance < min_distance:
                                min_distance = distance
                                closest_pair = (file1, file2)
                                
                
                if closest_pair:
                    file1_path = os.path.abspath(os.path.join(input_first_path,closest_pair[0]))
                    file2_path = os.path.abspath(os.path.join(input_second_path,closest_pair[1]))
                    save_folder1 = os.path.join(outputpath_img, closest_pair[0].split('.')[0])
                    os.makedirs(save_folder1, exist_ok=True)
                    save_folder_first = os.path.join(save_folder1, "first")
                    os.makedirs(save_folder_first, exist_ok=True)
                    save_folder_second = os.path.join(save_folder1, "second")
                    os.makedirs(save_folder_second, exist_ok=True)
                    
                    move_txt_and_related_images(file1_path, save_folder_first)
                    move_txt_and_related_images(file2_path, save_folder_second)

   
