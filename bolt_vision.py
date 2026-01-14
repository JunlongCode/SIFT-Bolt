# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 01:23:18 2023

@author: Admin
"""

import itertools
import cv2
import numpy as np
from PIL import Image
import os
import shutil

def cut_with_keyword(source_folder, destination_folder, keyword="vision", image_extensions=['.jpg', '.jpeg', '.png','JPG','txt']):
    # 确保目标文件夹存在
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # 遍历源文件夹中的文件
    for filename in os.listdir(source_folder):
        source_path = os.path.join(source_folder, filename)

        # 检查文件是否为图片文件且包含关键字
        if any(filename.lower().endswith(ext) for ext in image_extensions) and keyword.lower() in filename.lower():
            destination_path = os.path.join(destination_folder, filename)

            # 使用shutil.move进行剪切操作
            shutil.move(source_path, destination_path)


def process_image(input_path, perspective_matrix, output_folder):
    # 从输入路径中提取文件名和路径
    path, filename = os.path.split(input_path)
    name, extension = os.path.splitext(filename)

    # 读取原文档内容
    with open(input_path, 'r') as file:
        lines = file.readlines()

    # 创建要写入的文本文件名
    output_filename = os.path.join(output_folder, f"{name}_vision.txt")

    # 打开文件并写入矫正后的坐标和长度值
    with open(output_filename, 'w') as file:
        for line in lines:
            data = line.strip().split()
            if len(data) >= 5:
                x, y, length1, length2 = map(float, data[1:5])

                # 使用透视变换矩阵将坐标进行透视变换
                src_point = np.array([[x, y]], dtype=np.float32)
                dst_point = cv2.perspectiveTransform(src_point.reshape(-1, 1, 2), perspective_matrix)[0][0]

                # 写入矫正后的坐标和长度值
                file.write(f"{dst_point[0]} {dst_point[1]} {length1} {length2}\n")

    

def process_folder(folder_path, perspective_matrix, output_folder):
    # 获取文件夹中的所有文件
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # 处理每个文件
    for file in files:
        file_path = os.path.join(folder_path, file)
        process_image(file_path, perspective_matrix, output_folder)

def get_image_name(image_path):
    # 使用 os.path.basename 获取图片名字
    image_name = os.path.basename(image_path)
    return image_name

def generate_file_path(base_path, file_name, file_extension):
    # 使用 os.path.join 构建完整路径
    file_path = os.path.join(base_path, f"{file_name}.{file_extension}")
    return file_path

def remove_file_extension(file_path):
    # 使用 os.path.splitext 获取文件名和扩展名
    file_name, file_extension = os.path.splitext(file_path)

    # 返回不带扩展名的文件名
    return file_name

def create_txt_file(base_path, file_name):
    # 构建文件名
    file_name_out = f"{file_name}_central.txt"
    
    # 构建完整路径
    full_file_path = os.path.join(base_path, file_name_out)

    # 创建空白的文本文件
    with open(full_file_path, 'w'):
        pass  # 什么都不写入
        
    return full_file_path

def show_and_resize_image(image_path, window_name, width, height):
    # 读取照片
    image = cv2.imread(image_path)

    # 调整照片大小
    resized_image = cv2.resize(image, (width, height))

    # 弹出窗口显示照片
    cv2.imshow(window_name, resized_image)

    # 等待按键输入，参数为0表示一直等待直到按键按下
    cv2.waitKey(0)

    # 关闭窗口
    cv2.destroyAllWindows()

def change_vision(inputdir,outputdir):
    # 遍历文件夹中的所有图片文件
    for filename in os.listdir(inputdir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            # 获取图片的完整路径
            image_path = os.path.join(inputdir, filename)
            
            # 标签路径
            labelpath = os.path.join(outputdir, "labels")
            
            # 处理单张图片的代码
            process_single(image_path, labelpath, outputdir)        

def process_single(inputdir, labelpath, outputdir):
    # 打开图像
    image = Image.open(inputdir)
    
    
    # 获取图片名字
    image_name = get_image_name(inputdir)    
    image_name = remove_file_extension(image_name)

    
    # 获取图像的宽度和高度
    width, height = image.size

    # 将图像数据转换为NumPy数组
    image_np = np.array(image)

    
    # 构建输入路径
    input_file_path = generate_file_path(labelpath, image_name, "txt")

    # 创建一个输出文档
    out_txt_path = create_txt_file(labelpath, image_name)

    # 打开输入文档和输出文档
    with open(input_file_path, 'r') as input_file, open(out_txt_path, 'w') as output_file:
        for line in input_file:
            data = line.strip().split() #*scale_percent/100
        
            if len(data) == 5:
                # 解析左上角和右下角坐标
                mid_x, mid_y, w, h = map(float, data[1:])
            
                # 将中点坐标写入输出文档
                output_file.write(f"{mid_x} {mid_y}\n")


    def calculate_distance(point1, point2):
        """
        计算两点之间的距离的函数
        """
        x1, y1 = point1
        x2, y2 = point2
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def find_quadrilateral_vertices(points):
        '''
            找两组点，这两组点的距离为最大和第二大
        '''
        max_distance = 0
        second_max_distance = 0
        max_combination = None
        second_max_combination = None
        # 使用itertools.combinations生成所有可能的点组合
        for combination in itertools.combinations(points, 2):
            distance = calculate_distance(combination[0], combination[1])
            if distance > max_distance:
                second_max_distance = max_distance
                second_max_combination = max_combination
                max_distance = distance
                max_combination = combination
            elif distance > second_max_distance and combination != max_combination:
                second_max_distance = distance
                second_max_combination = combination
        return max_combination, second_max_combination



    # 创建一个空列表来存储中心坐标
    points = []

    # 打开已知的中心坐标文档
    with open(out_txt_path, 'r') as file:
        for line in file:
            x, y = map(float, line.strip().split())
            points.append((x, y))

    quadrilateral_vertices , a = find_quadrilateral_vertices(points)

    if quadrilateral_vertices:
        unique_points = [quadrilateral_vertices[0],quadrilateral_vertices[1],a[0],a[1]]

        scr=[0,0,0,0]
        temp1=[(0,0)]
        temp2=[(0,0)]
        temp3=[(0,0)]
        temp4=[(1,1)]
    
    #找x最大的点,右下角的点，x+y也会是最大的
        for i in range(4):
            if unique_points[i][0] + unique_points[i][1] > temp2[0][0] + temp2[0][1]:
                temp2 = [unique_points[i]]

    #找左上角的点，x+y会是最小的
        for i in range(4):
            if unique_points[i][0] + unique_points[i][1] < temp4[0][0] + temp4[0][1] and float(unique_points[i][0]) != float(temp2[0][0]) and float(unique_points[i][1]) != float(temp2[0][1]):
                temp4 = [unique_points[i]]
            
            #从剩下两个点中找y最大,左下角
        for i in range(4):
            if unique_points[i][1] > temp1[0][1] and float(unique_points[i][0]) != float(temp2[0][0]) and float(unique_points[i][1]) != float(temp2[0][1]) and float(unique_points[i][0]) != float(temp4[0][0])and float(unique_points[i][1]) != float(temp4[0][1]):
                temp1 = [unique_points[i]]

    #找剩下的点，右上角
        for i in range(4):
            if  float(unique_points[i][0]) != float(temp1[0][0]) and float(unique_points[i][1]) != float(temp1[0][1]) and float(unique_points[i][0]) != float(temp4[0][0])and float(unique_points[i][1]) != float(temp4[0][1]) and float(unique_points[i][0]) != float(temp2[0][0])and float(unique_points[i][1]) != float(temp2[0][1]):
                temp3 = [unique_points[i]]
              
        scr[0]=temp4 #左上
        scr[1]=temp3 #右上
        scr[2]=temp1 #左下
        scr[3]=temp2 #右下

        hang = float(input("请输入螺栓行数：")) # 或直接指定
        lie = float(input("请输入螺栓列数：")) 

        # 假设scr是源点坐标
        scr_points = np.array([[scr[0][0][0],scr[0][0][1]],[scr[1][0][0],scr[1][0][1]],[scr[2][0][0],scr[2][0][1]], [scr[3][0][0],scr[3][0][1]]], dtype=np.float32)
        
        bolt_width  = width*max(abs(scr[0][0][0]-scr[1][0][0]),abs(scr[0][0][0]-scr[2][0][0]),abs(scr[0][0][0]-scr[3][0][0]),abs(scr[1][0][0]-scr[2][0][0]),abs(scr[1][0][0]-scr[3][0][0]),abs(scr[2][0][0]-scr[3][0][0]))
        bolt_height = height*max(abs(scr[0][0][1]-scr[1][0][1]),abs(scr[0][0][1]-scr[2][0][1]),abs(scr[0][0][1]-scr[3][0][1]),abs(scr[1][0][1]-scr[2][0][1]),abs(scr[1][0][1]-scr[2][0][1]),abs(scr[2][0][1]-scr[3][0][1]))
        
        
        a=min(scr[0][0][0],scr[1][0][0],scr[2][0][0],scr[3][0][0])
        b=min(scr[0][0][1],scr[1][0][1],scr[2][0][1],scr[3][0][1])
        
        lie = lie/hang*bolt_height
        hang = bolt_height
        dst_points = np.array([[a*width,b*height],[lie+a*width,b*height],[a*width,hang+b*height],[lie+a*width,hang+b*height]], dtype=np.float32)
        #print("dst_points=",dst_points)  
        scr_points = np.array([[scr[0][0][0]*width,scr[0][0][1]*height],[scr[1][0][0]*width,scr[1][0][1]*height],[scr[2][0][0]*width,scr[2][0][1]*height], [scr[3][0][0]*width,scr[3][0][1]*height]], dtype=np.float32)
        #print("scr_points=",scr_points)
        matrix = cv2.getPerspectiveTransform(scr_points, dst_points)
        #print("matrix=",matrix)

                
        # 透视变换
        imgWarp = cv2.warpPerspective(image_np, matrix, (width, height))
        
        # 更正图片颜色，将图像从 BGR 转换为 RGB 格式
        image_rgb = cv2.cvtColor(imgWarp, cv2.COLOR_BGR2RGB)
        
        
        # 获取输入图像文件名（包含扩展名）      
        _, image_filename = os.path.split(inputdir)
        
        # 获取文件名和扩展名
        image_name2, image_extension = os.path.splitext(image_filename)
        
        # 在文件名后添加"vision"，并保持扩展名的一致性
        output_filename = f"{image_name2}_vision{image_extension.lower()}"
        
        output_path = os.path.join(os.path.dirname(inputdir), output_filename)
        
        cv2.imwrite(output_path, image_rgb) 
         
    else:
        print("无法找到四边形的顶点，点的数量不足。")

    

