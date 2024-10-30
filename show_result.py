# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 09:52:13 2023

@author: 86193
"""

# @Function:图片变色

from PIL import Image, ImageDraw, ImageFont
import os
import shutil

def move_files_out_of_folder(folder_path):
    # 获取文件夹内所有文件
    files = os.listdir(folder_path)

    # 移动每个文件到上一层目录
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        destination_path = os.path.join(os.path.dirname(folder_path), file_name)
        shutil.move(file_path, destination_path)
    
    #重构图片名字
    #切换到目标目录
    os.chdir(os.path.dirname(folder_path))

    # 获取目录中的所有文件
    files = os.listdir()
    
    for file_name in files: 
        if "_vision" in file_name:
            # 构建新的文件名，将"_vision"替换为空字符串
            new_filename = file_name.replace("_vision", "")
            new_filename = new_filename.replace("results", "")

            # 重命名文件
            os.rename(file_name, new_filename)



def delete_subfolders(folder_path):
    # 获取文件夹内所有文件和文件夹
    contents = os.listdir(folder_path)

    # 遍历每个文件/文件夹并删除文件夹
    for content in contents:
        content_path = os.path.join(folder_path, content)

        # 检查是否是文件夹
        if os.path.isdir(content_path):
            shutil.rmtree(content_path)
            #print(f"Deleted folder: {content_path}")

def show_result_img(inputfolder,outputdir): 
    single_show(inputfolder,outputdir)
    

def single_show(inputpath,outputpath):
    # 指定文件夹路径
    folder_path = inputpath
    
    #设置边框宽度
    border_width = 3


    # 获取文件夹中的图片文件列表
    image_files = [file for file in os.listdir(folder_path) if file.lower().endswith(('.jpg', '.png', '.jpeg'))]

    for image_file in image_files:
        # 生成txt文件路径
        image_file_txt_name = image_file[:-11]
        txt_file = os.path.join(folder_path, image_file_txt_name.split('.')[0] + '.txt')

        # 生成照片文件路径
        image_file_path = os.path.join(folder_path, image_file)
        # 打开图像
        image_result = Image.open(image_file_path)

        # 获取图像的宽度和高度
        w, h = image_result.size
    
        # 检查txt文件是否存在
        if os.path.exists(inputpath):
            # 打开图片
            image = Image.open(os.path.join(folder_path, image_file))
            draw = ImageDraw.Draw(image)
        
            # 打开txt文件并读取坐标
            with open(txt_file, 'r+') as txt:
                lines = txt.readlines()
            
                n=0 #用于计数第几个文本
            
                for line in lines:
                    # 解析坐标信息（坐标信息以空格分隔）
                    coordinates = line.strip().split(' ')
                    #if len(coordinates) == 6 and coordinates[5] != 'None' and coordinates[5] != '0':
                    if len(coordinates) == 6 and coordinates[5] != 'None' and coordinates[5] != 'missing' and float(coordinates[5]) >= 0 and float(coordinates[5]) < 360:
                        # 创建半透明红色矩形
                
                        x_center = w * float(coordinates[1])  # aa[1]左上点的x坐标
                        y_center = h * float(coordinates[2])  # aa[2]左上点的y坐标
                        width = int(w * float(coordinates[3]))  # aa[3]图片width
                        height = int(h * float(coordinates[4]))  # aa[4]图片height
                        lefttopx = int(x_center - width / 2.0)
                        lefttopy = int(y_center - height / 2.0)
                        rightbottomx = int(x_center + width / 2.0)
                        rightbottomy = int(y_center + height / 2.0)
                    
                        #画红色边框
                        for i in range(border_width):
                            draw.rectangle([(lefttopx-i,lefttopy+i),(rightbottomx+i,rightbottomy+i)],outline=(255, 0, 0))
                    
                        #添加文本
                        Loose_label = "Loose: "+str(coordinates[5])+"°"
                        text = Loose_label #TEXT[n]
                        text_color = (255,0,0)
                        font_size = 48
                        font = ImageFont.truetype("arial.ttf",font_size)
                    
                        # 使用 textbbox 获取文本的边界框（Bounding Box）
                        bbox = draw.textbbox((0, 0), text, font=font)
                        # 获取文本的宽度和高度
                        text_width = bbox[2] - bbox[0]
                        text_height = bbox[3] - bbox[1]
                        
                        text_position = (rightbottomx - (rightbottomx - lefttopx), lefttopy - text_height - text_height/3)
                    
                        draw.text(text_position,text,fill=text_color,font=font)
                    
                        n += 1
                    if len(coordinates) == 7 and coordinates[6] != 'None' and coordinates[5] != '0':
                        #left, top, right, bottom = map(int, coordinates)
                        # 创建半透明红色矩形
                
                        x_center = w * float(coordinates[1])  # aa[1]左上点的x坐标
                        y_center = h * float(coordinates[2])  # aa[2]左上点的y坐标
                        width = int(w * float(coordinates[3]))  # aa[3]图片width
                        height = int(h * float(coordinates[4]))  # aa[4]图片height
                        lefttopx = int(x_center - width / 2.0)
                        lefttopy = int(y_center - height / 2.0)
                        rightbottomx = int(x_center + width / 2.0)
                        rightbottomy = int(y_center + height / 2.0)
                    
                        #画红色边框
                        for i in range(border_width):
                            draw.rectangle([(lefttopx-i,lefttopy+i),(rightbottomx+i,rightbottomy+i)],outline=(255, 0, 0))
                    
                        #添加文本
                        Loose_label = "Loose: "+str(coordinates[5])+"°"+","+str(coordinates[6])+"KN"
                        text = Loose_label #TEXT[n]
                        text_color = (255,0,0)
                        font_size = 48
                        font = ImageFont.truetype("arial.ttf",font_size)
                    
                        # 使用 textbbox 获取文本的边界框（Bounding Box）
                        bbox = draw.textbbox((0, 0), text, font=font)
                        # 获取文本的宽度和高度
                        text_width = bbox[2] - bbox[0]
                        text_height = bbox[3] - bbox[1]
                        
                        text_position = (rightbottomx - (rightbottomx - lefttopx), lefttopy - text_height - text_height/3)
                    
                        draw.text(text_position,text,fill=text_color,font=font)
                    
                        n += 1          
                    
                    if len(coordinates) == 6 and coordinates[5] == 'missing' :
                        #left, top, right, bottom = map(int, coordinates)
                        # 创建半透明红色矩形
                
                        x_center = w * float(coordinates[1])  # aa[1]左上点的x坐标
                        y_center = h * float(coordinates[2])  # aa[2]左上点的y坐标
                        width = int(w * float(coordinates[3]))  # aa[3]图片width
                        height = int(h * float(coordinates[4]))  # aa[4]图片height
                        lefttopx = int(x_center - width / 2.0)
                        lefttopy = int(y_center - height / 2.0)
                        rightbottomx = int(x_center + width / 2.0)
                        rightbottomy = int(y_center + height / 2.0)
                    
                        #画红色边框
                        for i in range(border_width):
                            draw.rectangle([(lefttopx-i,lefttopy+i),(rightbottomx+i,rightbottomy+i)],outline=(255, 0, 0))
                    
                        #添加文本
                        Loose_label = "Loose: "+str(coordinates[5])
                        text = Loose_label #TEXT[n]
                        text_color = (255,0,0)
                        font_size = 48
                        font = ImageFont.truetype("arial.ttf",font_size)
                    
                        # 使用 textbbox 获取文本的边界框（Bounding Box）
                        bbox = draw.textbbox((0, 0), text, font=font)
                        # 获取文本的宽度和高度
                        text_width = bbox[2] - bbox[0]
                        text_height = bbox[3] - bbox[1]
                        
                        text_position = (rightbottomx - (rightbottomx - lefttopx), lefttopy - text_height - text_height/3)
                    
                        draw.text(text_position,text,fill=text_color,font=font)
                    
                        n += 1
                    
            # 保存修改后的图片
            output_path = os.path.join(folder_path, outputpath + image_file)
            image.save(output_path)
            image.close()

    
