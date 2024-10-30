# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 20:01:09 2024

@author: Admin
"""

from PIL import Image
import os

def is_image_corrupted(file_path):
    try:
        # 尝试打开图像文件
        with Image.open(file_path) as img:
            img.verify()
        return False  # 图像文件未损坏
    except (IOError, SyntaxError):
        return True  # 图像文件损坏

def delete_corrupted_images_surface(folder_path):
    if not os.path.isabs(folder_path):
        folder_path = os.path.abspath(folder_path)
    else:
        folder_path = folder_path
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if is_image_corrupted(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted corrupted image: {filename}")
            except Exception as e:
                print(f"Error deleting {filename}: {str(e)}")

def delete_corrupted_images_bolt(folder_path1,folder_path2):
    if not os.path.isabs(folder_path1):
        folder_path1 = os.path.abspath(folder_path1)
    else:
        folder_path1 = folder_path1
        
    if not os.path.isabs(folder_path2):
        folder_path2 = os.path.abspath(folder_path2)
    else:
        folder_path2 = folder_path2
        
    for filename in os.listdir(folder_path1):
        file_path1 = os.path.join(folder_path1, filename)
        if is_image_corrupted(file_path1):
            try:
                os.remove(file_path1)
                print(f"Deleted corrupted image: {filename}")
            except Exception as e:
                print(f"Error deleting {filename}: {str(e)}")
    
    for filename in os.listdir(folder_path2):
        file_path2 = os.path.join(folder_path2, filename)
        if is_image_corrupted(file_path2):
            try:
                os.remove(file_path2)
                print(f"Deleted corrupted image: {filename}")
            except Exception as e:
                print(f"Error deleting {filename}: {str(e)}")

