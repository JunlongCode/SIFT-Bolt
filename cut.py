# -*- coding: utf-8 -*-

import os
import cv2
import shutil

def save_coordinates(txt_path, coordinates):
    # 将坐标信息保存到txt文件
    with open(txt_path, 'w') as txt_file:
        txt_file.write(f"{coordinates}")

def cut_bolt(path,path3,path6):
    # 仅支持JPEG,PNG,JPG格式图片
    w = 2700  
    h = 2700
    img_total = []
    txt_total = []
 
    file = os.listdir(path)
    for filename in file:
        first, last = os.path.splitext(filename)
 
        if (last in [".txt"]):  # 图片的后缀名
            txt_total.append(first)
       
        else:
            img_total.append(first)
    if os.path.exists(path3):
        shutil.rmtree(path3)
        os.mkdir(path3)
    else:
        os.mkdir(path3)
 
    for img_ in img_total:
        if img_ in txt_total:
            filename_img = img_ + ".jpg"  # 图片的后缀名
         
            path1 = os.path.join(path, filename_img)
            a = os.path.exists(path1)
            if (a == False):
                filename_img = img_ + ".jpeg"  # 图片的后缀名
                
                path1 = os.path.join(path, filename_img)
                a = os.path.exists(path1)
            if (a == False):
                filename_img = img_ + ".png"  # 图片的后缀名
               
                path1 = os.path.join(path, filename_img)
                a = os.path.exists(path1)

            img = cv2.imread(path1)
            
            img = cv2.resize(img, (w, h))

            filename_txt = img_ + ".txt"
          
            n = 1
            with open(os.path.join(path, filename_txt), "r+", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    aa = line.split(" ")
                    x_center = w * float(aa[1])  # aa[1]左上点的x坐标
                    y_center = h * float(aa[2])  # aa[2]左上点的y坐标
                    width = int(w * float(aa[3]))  # aa[3]图片width
                    height = int(h * float(aa[4]))  # aa[4]图片height
                    lefttopx = int(x_center - width / 2.0)
                    lefttopy = int(y_center - height / 2.0)
                    
                    roi_lefttopx = max(0, lefttopx)  # 确保左上角 x 不小于 0
                    roi_lefttopy = max(0, lefttopy)  # 确保左上角 y 不小于 0
                    roi_rightbottomx = min(img.shape[1], lefttopx + width)  # 确保右下角 x 不大于原始图像宽度
                    roi_rightbottomy = min(img.shape[0], lefttopy + height)  # 确保右下角 y 不大于原始图像高度
                    # 调整裁剪坐标
                    roi = img[roi_lefttopy:roi_rightbottomy, roi_lefttopx:roi_rightbottomx]
                    
                    filename_last = img_ + "_" + str(n) + ".jpg"  # 裁剪出来的小图文件名
                    
                    path2 = os.path.join(path6, "roi")  # 需要在path3路径下创建一个roi文件夹
                    
                    cv2.imwrite(os.path.join(path2, filename_last), roi)
                    # 同时保存坐标信息为同名txt文件
                    coordinates_txt_path = os.path.join(path6, "roi", filename_last.replace(".jpg", ".txt"))
                    save_coordinates(coordinates_txt_path, line)
                    
                    n = n + 1
        else:
            continue

