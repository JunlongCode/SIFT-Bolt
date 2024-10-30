# -*- coding: utf-8 -*-

import cv2              
import numpy as np      
import math
import os
import shutil


def get_subfolders(path):

    # 使用 os.listdir 获取指定路径下的所有文件和文件夹
    items = os.listdir(path)

    # 过滤出文件夹
    subfolders = [item for item in items if os.path.isdir(os.path.join(path, item))]

    # 获取下一级文件夹的完整路径
    subfolder_paths = [os.path.join(path, subfolder) for subfolder in subfolders]

    return subfolder_paths

#创建文本文档
def create_txt_file_with_string(folder_path, file_name):
    # 拼接文件的完整路径
    file_path = os.path.join(folder_path, file_name)
    # 创建文本文件，并写入内容
    with open(file_path, 'w') as file:
        pass

#提取路径的最后一个名称        
def extract_last_name_from_path(file_path):
    last_name = os.path.basename(file_path)
    return last_name

#文件写入
def append_b_content_and_c_to_a(a_path, b_path, c):
    # 读取b.txt的内容
    with open(b_path, 'r+', encoding='utf-8') as file_b:
        b_content = file_b.read().replace('\n', '')

    # 将b.txt的内容和c的值写入a.txt
    with open(a_path, 'a+', encoding='utf-8') as file_a:
        file_a.write(b_content +' ' + str(c) + '\n')
    

#路径下所有照片路径
def get_image_path(folder_path):
    # 使用 os.listdir 获取指定文件夹下的所有文件
    files = os.listdir(folder_path)

    # 遍历文件列表，找到图片文件的路径
    for file in files:
        # 假设你要找的是以 .jpg 或 .png 结尾的图片文件
        a = file
        if file.lower().endswith(('.jpg', '.png')):
            # 构建图片文件的完整路径
            image_path = os.path.join(folder_path, file)
            return image_path, a  # 返回找到的图片文件路径

    # 如果没有找到图片文件，可以返回 None 或者抛出异常，根据需要处理
    return None


def move_images(source_folder, target_folder):
    # 获取源文件夹中的所有文件
    files = os.listdir(source_folder)

    # 确保目标文件夹存在，如果不存在则创建
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # 遍历文件夹中的文件
    for file_name in files:
        # 判断文件是否为图片（你可以根据实际需要修改判断条件）
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            # 构建源文件路径和目标文件路径
            source_path = os.path.join(source_folder, file_name)
            target_path = os.path.join(target_folder, file_name)

            # 移动文件到目标文件夹
            shutil.move(source_path, target_path)


#主函数

def angle_bolt(match_path,outputpath,args_target):
    
    #对文件中的子图进行sift求解
    #先创建结果保存文件夹
    result_path = os.path.join(outputpath,"result")
    os.makedirs(result_path, exist_ok=True)

    #得到对应的文件路径
    split_path = os.path.join(match_path, "split")

    subfolders1 = get_subfolders(split_path) 
    subfolders2 = []
    i=1
    #创立txt文件
    for subfolder in subfolders1:
        string_variable = extract_last_name_from_path(subfolder) #得到文件夹命名

        create_txt_file_with_string(result_path, f"{string_variable}.txt")
        #获得子图的存放路径
        subfolders2 = get_subfolders(subfolder) 
 
        #求每个子图的角度
        
        for subfolder2 in subfolders2: #subfolder2相当于02_03_07_F_vision_1

            sub_first  = os.path.join(subfolder2,"first") 
            files = os.listdir(sub_first) 
            # 遍历文件列表，找到图片文件的路径
            for file in files: 
                if file.lower().endswith(('.jpg', '.png')):
                    a = os.path.basename(file) #获得文件名
                    # 构建图片文件的完整路径
                    sub_image_first_path = os.path.join(sub_first, file)
        
        
            sub_second = os.path.join(subfolder2,"second")        
            files = os.listdir(sub_second)
            # 遍历文件列表，找到图片文件的路径
            for file in files:
                # 假设你要找的是以 .jpg 或 .png 结尾的图片文件
                if file.lower().endswith(('.jpg', '.png')):
                    b = os.path.basename(file)
                    # 构建图片文件的完整路径
                    sub_image_second_path = os.path.join(sub_second, file)
            
            ########################
            # 判断命名中是否含有screw或nut，不含有的话直接求sift，有的话求两次然后求角度转动的相对值
            if '_nut' in a or 'screw' in a or 'nut' in b or 'screw' in b:
                files_first = os.listdir(sub_first)
                files_second = os.listdir(sub_second)
                the_angle_bolt0 = None
                the_angle_bolt1 = None
                the_angle_bolt = None
                for file_first in files_first:
                    # 假设你要找的是以 .jpg 或 .png 结尾的图片文件
                    if file_first.lower().endswith(('.jpg', '.png')):
                        for file_second in files_second:
                            # 假设你要找的是以 .jpg 或 .png 结尾的图片文件
                            if file_second.lower().endswith(('.jpg', '.png')):
                                if 'nut' in file_first and 'nut' in file_second:
                                    sub_image_first_path =  os.path.join(sub_first, file_first)
                                    sub_image_second_path = os.path.join(sub_second, file_second)
                                    #the_angle_bolt0 = single_bolt(sub_image_first_path, sub_image_second_path)
                                    the_angle_bolt0 = single_bolt(sub_image_second_path, sub_image_first_path, i) #first和second换一下
                                elif 'screw' in file_first and 'screw' in file_second:
                                    sub_image_first_path =  os.path.join(sub_first, file_first)
                                    sub_image_second_path = os.path.join(sub_second, file_second)
                                    #the_angle_bolt1 = single_bolt(sub_image_first_path, sub_image_second_path)
                                    the_angle_bolt1 = single_bolt(sub_image_second_path, sub_image_first_path, i)
                                i += 1
                
                # 根据是否同号来判断螺栓与螺杆相对转动角度
                if the_angle_bolt0 is not None and the_angle_bolt1 is not None:
                    print(the_angle_bolt0,the_angle_bolt1)
                    if the_angle_bolt0*the_angle_bolt1>=0:
                        the_angle_bolt = abs(abs(the_angle_bolt0) - abs(the_angle_bolt1))                
                    elif the_angle_bolt0*the_angle_bolt1<0:
                        the_angle_bolt = abs(the_angle_bolt0) + abs(the_angle_bolt1)
                elif the_angle_bolt0 is not None and the_angle_bolt1 is None:
                    print(the_angle_bolt0)
                    the_angle_bolt = abs(the_angle_bolt0)
                elif the_angle_bolt0 is None and the_angle_bolt1 is not None:
                    print(the_angle_bolt1)
                    the_angle_bolt = abs(the_angle_bolt1)         
            else:
                the_angle_bolt = single_bolt(sub_image_second_path, sub_image_first_path, i) 
                i += 1
            
            
            #将结果写入result_path对应的txt中
            txt_files = [file for file in os.listdir(result_path) if file.endswith(".txt")]
    
            for filename in txt_files:
                ddd = os.path.join(subfolder2,'second')
                       
                temp_img_path, b = get_image_path(ddd)       
        
                dot_index = b.find(".")
                # 使用切片提取点号之前的部分
                b = b[:dot_index] + '.txt'
                
                #去掉字符串中的_nut和_screw
                b = b.replace('_nut','')
                b = b.replace('_screw','')
        
        
                front_ten_str = extract_last_name_from_path(subfolder2)
        
                if filename[:10] == front_ten_str[:10]:
                    a_path = os.path.join(result_path,filename)
                  
                    b_path = os.path.join(sub_second,b) 
                   
                    append_b_content_and_c_to_a(a_path, b_path, the_angle_bolt)
    
    #将图片和处理后的txt放在一起
    vision_path = os.path.join(args_target, "vision")
    source_folder = os.path.join(vision_path, "second")
    move_images(source_folder, result_path)
    

#求单颗螺栓子图
def single_bolt(inputdir_first, inputdir_second, i):    
    ################################################求转角

    original_bolt = cv2.imread(inputdir_first)  # 读取螺栓原图
    
    bolt_rot = cv2.imread(inputdir_second)       # 读取螺栓旋转图
    
    #创建sift
    sift = cv2.SIFT_create()

    (kp1, des1) = sift.detectAndCompute(original_bolt, None)
    (kp2, des2) = sift.detectAndCompute(bolt_rot, None)


    bf = cv2.BFMatcher()
    matches1 = bf.knnMatch(des1, des2, k=2)
   
    ratio1 = 0.4 
    good1 = []
    

    # 判断特征点数目的最小值
    if des1.shape[0]>=des2.shape[0]:
        des_num = des2.shape[0]
    else:
        des_num=des1.shape[0]
        
    
    # 以特征点数目最小值为终点配对
    while len(good1)<des_num:
        ratio1 = ratio1 + 0.01
        good1 = []
        for m1, n1 in matches1:
            # 如果最接近和次接近的比值大于一个既定的值，那么我们保留这个最接近的值，认为它和其匹配的点为good_match
            if m1.distance < ratio1 * n1.distance:
                good1.append([m1])
    
    

    if len(good1) > 4:
        ptsA = np.float32([kp1[m[0].queryIdx].pt for m in good1]).reshape(-1, 1, 2)
        ptsB = np.float32([kp2[m[0].trainIdx].pt for m in good1]).reshape(-1, 1, 2)
 
        ransacReprojThreshold = 4
        cos = sin = float('inf')
        i=1
        # 初始化一个空列表
        number_sequence = []
        
        while (cos>=1.1 or cos<=-1.1) or (sin>=1.1 or sin<=-1.1) or (cos*cos+sin*sin>=1.05 or cos*cos+sin*sin<=0.95): #or (abs(cos1*cos1-cos2*cos2) >=0.1 or abs(sin1*sin1-sin2*sin2) >= 0.1):
            ptsA = np.float32([kp1[m[0].queryIdx].pt for m in good1]).reshape(-1, 1, 2)
            ptsB = np.float32([kp2[m[0].trainIdx].pt for m in good1]).reshape(-1, 1, 2)
 
            # RANSAC算法   
            H, status =cv2.findHomography(ptsA, ptsB, cv2.RANSAC, ransacReprojThreshold, maxIters=2000)

            i=i+1
            
            C=H[:,0]-H[:,2]*H[2,0]
            S=H[:,1]-H[:,2]*H[2,1]
            

            
            cos=(C[0]+S[1])/2
            sin=(-S[0]+C[1])/2
            

            if cos<=1 and cos>=-1:
                number_sequence.append(math.acos(cos)/(2*math.pi)*360)
            
            ransacReprojThreshold = ransacReprojThreshold + 0.1 
            
            if ransacReprojThreshold >= des_num:
                break
        
        if 1 in status:

            cos=round(cos,2) #保留2位小数

            sin=round(sin,2) #保留2位小数
            
            if cos>=1.00:
                cos = 1.00
            if cos<=-1.00:
                cos = -1.00
            if sin>=1.00:
                sin = 1.00
            if sin<=-1.00:
                sin = -1.00          

            print("余弦值Cos为：",cos)
            print("正弦值Sin为：",sin)
            if cos>=-1.0 and cos<=1.0 and sin>=-1.0 and sin<=1.0:  
                # 第一象限
                if cos>=0 and sin>=0:
                    if abs(sin-0.05)<=0.05 or abs(sin+0.05)<=0.05:
                        a = 0.0
                        #print("由此得螺栓转动",a,"度")
                    else:
                        if cos<=-1 or cos>=1:
                            cos = int(cos)
                        a = math.acos(cos)/(2*math.pi)*360    #a为转动角度
 
                # 第二象限
                elif cos<=0 and sin>=0:
                    if cos<=-1 or cos>=1:
                        cos = int(cos)        
                    a = math.acos(cos)/(2*math.pi)*360 
               
                # 第三象限
                elif cos<=0 and sin<=0:
                    if abs(sin-0.05)<0.05 or abs(sin+0.05)<0.05:
                        a = 180.0
                       
                    else:
        
                        a = 360 - math.acos(cos)/(2*math.pi)*360
                    
                # 第四象限
                else:
                    if abs(sin-0.05)>0.05 or abs(sin+0.05)>0.05:
                        a = 360-math.acos(cos)/(2*math.pi)*360
                        if a<0:
                            a = 360 + a
                       
                    else:
                        a = math.acos(cos)/(2*math.pi)*360
                return round(a,1) #只保留一个小数
        else:
            return None
        
