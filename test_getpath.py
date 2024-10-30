# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 00:31:58 2023

@author: ljl
"""

import os

def get_subfolders(path):
    # 使用 os.listdir 获取指定路径下的所有文件和文件夹
    print(type(path))
    items = os.listdir(path)

    # 过滤出文件夹
    subfolders = [item for item in items if os.path.isdir(os.path.join(path, item))]

    # 获取下一级文件夹的完整路径
    subfolder_paths = [os.path.join(path, subfolder) for subfolder in subfolders]

    return subfolder_paths

