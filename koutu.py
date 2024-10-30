# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 18:02:10 2024

@author: ljl
"""

from PIL import Image,ImageDraw
import os

# 针对label_num=0,只有一行的情况的抠图,即内嵌螺栓
def extract_polygon_region_0(image_path, polygon_coordinates):
    # 打开图像
    image = Image.open(image_path)

    # 创建一个图像大小的黑色背景
    mask = Image.new('L', image.size, 0)

    # 将多边形坐标转换为像素坐标
    polygon = [(int(image.width * x), int(image.height * y)) for x, y in zip(polygon_coordinates[0::2], polygon_coordinates[1::2])]

    # 在黑色背景上绘制多边形，多边形内部区域为白色
    ImageDraw.Draw(mask).polygon(polygon, outline=255, fill=255)

    # 将图像和蒙版合并
    result = Image.new('RGB', image.size, (255, 255, 255))
    result.paste(image, mask=mask)

    # 保存合并后的图像覆盖原始图像
    #result.save(image_path)
    new_name = '_nut'
    path_without_extension, file_extension = os.path.splitext(image_path)
    image_path_nut = f"{path_without_extension}{new_name}{file_extension}"
    # 保存合并后的图像覆盖原始图像
    result.save(image_path_nut)
    # 删除原图片
    os.remove(image_path)
    
# 针对label_num=0、1,有两行的情况的抠图,即外套螺栓
def extract_polygon_region_screw(image_path, polygon_coordinates):
    # 打开图像
    image = Image.open(image_path)

    # 创建一个图像大小的黑色背景
    mask = Image.new('L', image.size, 0)

    # 将多边形坐标转换为像素坐标
    polygon = [(int(image.width * x), int(image.height * y)) for x, y in zip(polygon_coordinates[0::2], polygon_coordinates[1::2])]

    # 在黑色背景上绘制多边形，多边形内部区域为白色
    ImageDraw.Draw(mask).polygon(polygon, outline=255, fill=255)

    # 将图像和蒙版合并
    result = Image.new('RGB', image.size, (255, 255, 255))
    result.paste(image, mask=mask)
    
    new_name = '_screw'
    path_without_extension, file_extension = os.path.splitext(image_path)
    image_path_screw = f"{path_without_extension}{new_name}{file_extension}"
    # 保存合并后的图像覆盖原始图像
    result.save(image_path_screw)

def extract_polygon_region_nut(image_path, polygon_coordinates):
    # 打开图像
    image = Image.open(image_path)

    # 创建一个图像大小的黑色背景
    mask = Image.new('L', image.size, 0)

    # 将多边形坐标转换为像素坐标
    polygon = [(int(image.width * x), int(image.height * y)) for x, y in zip(polygon_coordinates[0::2], polygon_coordinates[1::2])]

    # 在黑色背景上绘制多边形，多边形内部区域为白色
    ImageDraw.Draw(mask).polygon(polygon, outline=255, fill=255)

    # 将图像和蒙版合并
    result = Image.new('RGB', image.size, (255, 255, 255))
    result.paste(image, mask=mask)
    
    new_name = '_nut'
    path_without_extension, file_extension = os.path.splitext(image_path)
    image_path_nut = f"{path_without_extension}{new_name}{file_extension}"
    # 保存合并后的图像覆盖原始图像
    result.save(image_path_nut)
    return image_path_nut
    
def cover_polygon_region(image_path, polygon_coordinates_1):
    # 打开图像
    image = Image.open(image_path)

    # 创建一个图像大小的白色背景
    mask = Image.new('L', image.size, 255)

    # 将多边形坐标转换为像素坐标
    polygon_1 = [(int(image.width * x), int(image.height * y)) for x, y in zip(polygon_coordinates_1[0::2], polygon_coordinates_1[1::2])]

    # 在白色背景上绘制多边形，多边形内部区域为黑色
    ImageDraw.Draw(mask).polygon(polygon_1, outline=0, fill=0)

    # 将图像和蒙版合并
    result = Image.new('RGB', image.size, (255, 255, 255))
    result.paste(image, mask=mask)

    # 保存合并后的图像覆盖原始图像
    result.save(image_path)



def crop(images_path, labels_path, output_path):
    #读取标签文件夹中的所有文件
    label_files = [f for f in os.listdir(labels_path) if f.endswith('.txt')]
    image_files = [f for f in os.listdir(images_path) if f.endswith(('.jpg', '.png', '.JPG'))]
    
    #一个个标签文件分析
    for label_file in label_files:
        # 逐个标签文件分析
        label_path = os.path.join(labels_path, label_file)
        # 找到与此标签对应的图片路径
        for image_file in image_files:
            image_path = os.path.join(images_path, image_file)
            if os.path.splitext(image_file)[0] == os.path.splitext(label_file)[0]:
                break
        # 打开标签文档
        with open(label_path, 'r') as label:
            # 查看标签文档有几行，一行即为内嵌，两行即为外套螺栓
            line_count = sum(1 for line in label)
            # 开始对文件内容进行处理
            ############### 当为一行时，即为内嵌螺栓
            coords_nut = None
            coords_screw = None
            if line_count == 1:
                with open(label_path, 'r') as label:
                    for line in label:
                        # 解析多边形坐标信息，格式为 "label x1 y1 x2 y2 x3 y3 ..."
                        parts = line.strip().split()
                        label_num = int(parts[0])
                        coords = list(map(float, parts[1:]))
                        
                        # 裁剪图像并将多边形外的区域变为白色
                        extract_polygon_region_0(image_path, coords)
            
                
            ############### 当为两行时，即为外套螺栓
            elif line_count == 2:
                with open(label_path, 'r') as label:
                    for line in label:
                        # 解析多边形坐标信息，格式为 "label x1 y1 x2 y2 x3 y3 ..."
                        parts = line.strip().split()
                        label_num = int(parts[0])
                        coords = list(map(float, parts[1:]))
                        # 裁剪图像并将多边形外的区域变为白色
                        if label_num == 0:
                            #得到螺母坐标
                            coords_nut = coords                            
                        elif label_num == 1:
                            #得到螺杆坐标
                            coords_screw = coords
                    if coords_screw != None:
                        extract_polygon_region_screw(image_path, coords_screw)
                        image_path_nut = extract_polygon_region_nut(image_path, coords_nut)
                        cover_polygon_region(image_path_nut, coords_screw)
                        
                        #删除原图
                        os.remove(image_path)
                    else:  #说明两个都是0：nut
                        # 裁剪图像并将多边形外的区域变为白色
                        extract_polygon_region_0(image_path, coords)
                        
                    #删除原图片
                    #os.remove(image_path)
                                                
                                          