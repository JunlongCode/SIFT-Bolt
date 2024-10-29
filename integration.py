# -*- coding: utf-8 -*-

from detect_s import detect_surface
from detect import detect_bolt
from cut import cut_bolt
from bolt_vision import change_vision, cut_with_keyword
import argparse
import os
from koutu import crop
from SRGAN import test
from segment import segment_bolt
from sift_bolt import angle_bolt 
from test_match import find_match
from show_result import show_result_img,move_files_out_of_folder,delete_subfolders
from wright_json import create_image_json
import shutil
import cv2
from delete_broken_photo import delete_corrupted_images_surface, delete_corrupted_images_bolt

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="人工智能识别")
    sub_parser = parser.add_subparsers(dest="command")
    surface_cmd = sub_parser.add_parser("surface", help="表面检测")
    bolt_cmd = sub_parser.add_parser("bolt",help="螺栓检测")
    bolt_cmd.add_argument("--source1", help="输入第一次拍摄的文件夹", required=True)
    bolt_cmd.add_argument("--source2", help="输入第二次拍摄的文件夹", required=True)
    surface_cmd.add_argument("--source", help="输入文件夹", required=True)
    surface_cmd.add_argument("--target", help="输出文件夹", required=True)
    bolt_cmd.add_argument("--target", help="输出文件夹", required=True)
    args = parser.parse_args()
    if args.command == "surface":
        delete_corrupted_images_surface(args.source) #删除损坏照片
        detect_surface(args.source,args.target)                
        respond_command = "表观病害检测完成"
        print(respond_command)
        
    
    elif args.command == "bolt":
        delete_corrupted_images_bolt(args.source1, args.source2) #删除损坏照片
       
        
        ####检测螺栓并保存标签                
        detect_bolt(args.source1,args.source2,args.target) 
       
  
        ####矫正拍摄视角
        if not os.path.isabs(args.target):
            abs_target = os.path.abspath(args.target)
        else:
            abs_target = args.target
        
        first_filename = "first"
        second_filename = "second"            
        new_outpath1 = os.path.join(abs_target, first_filename)
        new_outpath2 = os.path.join(abs_target, second_filename)
        change_vision(args.source1,new_outpath1) 
        change_vision(args.source2,new_outpath2)
  
        
        #####创建将矫正后的图片放在一起的文件夹，并且再检测一次
        # 在指定路径下创建名为"vision"的文件夹
        base_path = args.target #os.path.dirname(args.target)   #获取上一级目录
        vision_path = os.path.join(base_path, "vision")
        os.makedirs(vision_path, exist_ok=True)
        # 在"vision"文件夹下创建名为"first"和"second"的子文件夹
        os.makedirs(os.path.join(vision_path, "first"), exist_ok=True)
        os.makedirs(os.path.join(vision_path, "second"), exist_ok=True)
        # 剪切图片带指定文件夹
        vision_first_path = os.path.join(vision_path,"first")
        vision_second_path= os.path.join(vision_path,"second")
        cut_with_keyword(args.source1, vision_first_path, keyword="vision")
        cut_with_keyword(args.source2, vision_second_path, keyword="vision")
        # 检测生成矫正后的照片中螺栓的坐标
        vision_txt_path = os.path.join(vision_path,"txt")
        detect_bolt(vision_first_path,vision_second_path,vision_txt_path)
        # 将坐标剪切到图片中
        txt_first_path = os.path.join(vision_txt_path,"first")
        txt_second_path = os.path.join(vision_txt_path,"second")
        txt_first_label_path = os.path.join(txt_first_path,"labels")
        txt_second_label_path = os.path.join(txt_second_path,"labels")
        cut_with_keyword(txt_first_label_path, vision_first_path, keyword="vision")
        cut_with_keyword(txt_second_label_path, vision_second_path, keyword="vision")        


        ####################cut()将照片裁剪为子图
        # 在指定路径下创建名为"cut_bolt"的文件夹
        base_path = args.target #os.path.dirname(args.target)   #获取上一级目录
        cut_bolt_path = os.path.join(base_path, "cut_bolt")
        os.makedirs(cut_bolt_path, exist_ok=True)
        # 剪切图片带指定文件夹,没有就创立
        cut_bolt_first_path = os.path.join(cut_bolt_path,"first")
        os.makedirs(cut_bolt_first_path, exist_ok=True)
        cut_bolt_first_cut_path = os.path.join(cut_bolt_first_path,"cut")
        os.makedirs(cut_bolt_first_cut_path, exist_ok=True)
        cut_bolt_first_cut_roi_path = os.path.join(cut_bolt_first_cut_path,"roi")
        os.makedirs(cut_bolt_first_cut_roi_path, exist_ok=True)
        cut_bolt_second_path = os.path.join(cut_bolt_path,"second")
        os.makedirs(cut_bolt_first_path, exist_ok=True)
        cut_bolt_second_cut_path = os.path.join(cut_bolt_second_path,"cut")
        os.makedirs(cut_bolt_second_cut_path, exist_ok=True)
        cut_bolt_second_cut_roi_path = os.path.join(cut_bolt_second_cut_path,"roi")
        os.makedirs(cut_bolt_second_cut_roi_path, exist_ok=True)
        # 开始裁剪
        cut_bolt(vision_first_path, cut_bolt_first_cut_roi_path, cut_bolt_first_cut_path)
        cut_bolt(vision_second_path, cut_bolt_second_cut_roi_path, cut_bolt_second_cut_path)

        
        ###################SRGAN清晰子图        
        test.clearify_bolt(cut_bolt_first_cut_roi_path, cut_bolt_first_cut_roi_path)
        test.clearify_bolt(cut_bolt_second_cut_roi_path, cut_bolt_second_cut_roi_path)
              
        
        ###################segment将螺栓分割为螺栓和螺母
        segment_path = os.path.join(abs_target,"segment") #创建分割保存路径
        os.makedirs(segment_path, exist_ok=True)
        segment_path_first = os.path.join(segment_path, "first")
        segment_path_second = os.path.join(segment_path, "second")
        segment_bolt(cut_bolt_first_cut_roi_path, segment_path_first)
        segment_bolt(cut_bolt_second_cut_roi_path, segment_path_second)
    
           
        #########koutu将分割的区域抠出来
        first_label_path = os.path.join(segment_path_first, 'labels')
        second_label_path = os.path.join(segment_path_second, 'labels')
        crop(cut_bolt_first_cut_roi_path, first_label_path, cut_bolt_first_cut_roi_path)
        crop(cut_bolt_second_cut_roi_path, second_label_path, cut_bolt_second_cut_roi_path)
        
        
       
        #########sift_bolt求出转动角度
        sift_path = os.path.join(args.target,"sift")
        os.makedirs(sift_path, exist_ok=True)
        match_path = os.path.join(sift_path,"match")
        os.makedirs(match_path, exist_ok=True)
        #找到相对应的螺栓子图
        find_match(cut_bolt_first_cut_roi_path,cut_bolt_second_cut_roi_path,match_path)
        #求转动角度
        
        angle_bolt(match_path, sift_path, args.target)
        
        
        #########show_result返回结果
        sift_result_path = os.path.join(sift_path, "result")
        result_show_path = os.path.join(args.target, "results")
        os.makedirs(result_show_path, exist_ok=True)
        #此处可能需要绝对路径
        sift_result_path = os.path.abspath(sift_result_path)
        result_show_path = os.path.abspath(result_show_path)
        show_result_img(sift_result_path, result_show_path)

        #########生成json文件
        create_image_json(sift_result_path, result_show_path)
        
        #########把照片移动到和json一个文件夹
        files = os.listdir(args.target)
        for file_name in files:
            source_path = os.path.join(args.target, file_name)
        # 判断是否是文件夹
            if os.path.isdir(source_path):
                continue  # 如果是文件夹，跳过

            # 判断文件类型（例如，这里假设是以 .jpg 结尾的照片文件）
            if file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                # 构建目标文件路径
                target_path = os.path.join(result_show_path, file_name)
                # 移动文件到目标文件夹
                shutil.move(source_path, target_path)

        move_files_out_of_folder(result_show_path)
        #delete_subfolders(abs_target)
        
        respond_command = "螺栓松动检测完工！"
        print(respond_command)
        
        
    else:
        parser.print_help()

