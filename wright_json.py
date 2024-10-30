# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 07:22:51 2023

@author: ljl
"""


import os
import json


def create_image_json(folder_path, outpath):
    image_data = {}
    each_img  = []
    total_img = {}
    
    # 遍历文件夹中的txt文件
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.txt')):
            filename_path = os.path.join(folder_path, filename)
            with open(filename_path, 'r') as file:
                for line in file:
                    five_ele = line.split()
                    angle_str = ' '.join(five_ele[5:6]) #提取角度元素
                    if angle_str != "None":
                        angle = float(angle_str)
                        # 在这里对每一行进行处理
                        if line[0] == "2":
                            each_img.append(0)
                        elif angle > 180 or angle == 180:   #设置判定松动的阈值
                            each_img.append(1)
            total_img[filename[:-4]] = each_img
            each_img = []
                    
    
            for key,value in total_img.items():
                if len(value) == 0:

                    # 构造图片信息字典
                    image_info = {
                        filename[:-4] + ".jpg": {
                            "loose": 0,
                            "missing": 0,
                            }
                        }

                else:

                    if 1 in value:
                        loose_num = value.count(1)
                    else:
                        loose_num = 0

                    if 0 in value:
                        missing_num = value.count(0)
                    else:
                        missing_num = 0

                    # 构造图片信息字典
                    # 构建字典结构
                    image_info = {
                        filename[:-4] + ".jpg": {
                            "loose": loose_num,
                            "missing": missing_num,
                            }
                        }

                # 将图片信息添加到字典中
                image_data.update(image_info)

    json_filename = f"bolt_disease.json"    

    # 拼接输出路径
    outpath = os.path.join(outpath, json_filename)

    # 将图片信息字典保存到JSON文件
    with open(outpath, 'w') as json_file:
        json.dump(image_data, json_file, indent=2)

