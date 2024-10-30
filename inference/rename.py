# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 00:08:40 2024

@author: ljl
"""

import os

# 定义文件夹路径
folder_path_first = 'your_path/inference/first'
folder_path_second = 'your_path/inference/second'

# 获取文件夹中的所有文件名
files_first = os.listdir(folder_path_first)
files_second = os.listdir(folder_path_second)

# 对文件进行排序
files_first.sort()
files_second.sort()

# 定义计数器
count = 0
sub_count = 0
sub_sub_count = 1

# 遍历文件并重命名
for file_name in files_first:
    # 拼接新的文件名
    new_name = f"00_0{count}_{sub_count}0_{sub_sub_count}"

    # 构建新的文件名路径
    new_file_path = os.path.join(folder_path_first, new_name + os.path.splitext(file_name)[1])

    # 重命名文件
    os.rename(os.path.join(folder_path_first, file_name), new_file_path)

    # 更新计数器
    sub_sub_count += 1
    if sub_sub_count > 9:  #3:
        sub_sub_count = 1
        sub_count += 1
        if sub_count > 9:
            sub_count = 0
            count += 1
            
            
# 定义计数器
count = 0
sub_count = 0
sub_sub_count = 1

# 遍历文件并重命名
for file_name in files_second:
    # 拼接新的文件名
    new_name = f"00_0{count}_{sub_count}0_{sub_sub_count}"

    # 构建新的文件名路径
    new_file_path = os.path.join(folder_path_second, new_name + os.path.splitext(file_name)[1])

    # 重命名文件
    os.rename(os.path.join(folder_path_second, file_name), new_file_path)

    # 更新计数器
    sub_sub_count += 1
    if sub_sub_count > 9:     
        sub_sub_count = 1
        sub_count += 1
        if sub_count > 9:
            sub_count = 0
            count += 1            


print("重命名完成！")
