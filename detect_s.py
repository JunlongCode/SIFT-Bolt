# -*- coding: utf-8 -*-

from enum import Enum
from ultralytics import YOLO
from pprint import pprint
import os
from collections import Counter
import json

def create_image_json(folder_path, outpath, pred_num, pred_type):
    image_data = {}
    i = 0  # 用于更新pred_type

    # 遍历文件夹中的图片文件
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            # 获取图片的完整路径
            image_path = os.path.join(folder_path, filename)

            # 获取图片的文件名和扩展名
            image_name, image_extension = os.path.splitext(filename)

            if pred_num[i] == 0:
                i += 1

                # 构造图片信息字典
                image_info = {
                    image_name + ".jpg": {
                        "corrosion" : 0,
                        "crack": 0,
                        "spalling": 0,
                    }
                    }

            else:
                # 示例向量
                my_vector = pred_type[i]

                # 调用函数获取元素出现次数的字典
                element_counts_dict = count_elements(my_vector)

                i += 1

                if "Corrosion" in element_counts_dict:
                    corrosion_num = element_counts_dict["Corrosion"]
                else:
                    corrosion_num = 0

                if "Crack" in element_counts_dict:
                    crack_num = element_counts_dict["Crack"]
                else:
                    crack_num = 0

                if "Spalling" in element_counts_dict:
                    spalling_num = element_counts_dict["Spalling"]
                else:
                    spalling_num = 0


                # 构造图片信息字典
                # 构建字典结构
                image_info = {
                    image_name + ".jpg": {
                        "corrosion": corrosion_num,
                        "crack": crack_num,
                        "spalling": spalling_num,
                    }
                }

            # 将图片信息添加到字典中
            image_data.update(image_info)

    json_filename = f"disease.json"

    # 拼接输出路径
    outpath = os.path.join(outpath, json_filename)

    # 将图片信息字典保存到JSON文件
    with open(outpath, 'w', encoding='utf-8') as json_file:
        json.dump(image_data, json_file, indent=2, ensure_ascii=False)

def count_elements(vector):
    # 使用Counter计算元素出现的次数
    element_counts = Counter(vector)
    
    # 返回元素及其出现的次数的字典
    return dict(element_counts)

def detect_surface(inputdir,outputdir):
    class DiseaseType(Enum):
        
        Corrosion = 0 
        Crack = 1 
        Spalling = 2 

    def post_process(detection_result):
        """
        args:
            detection_result: list<torch.tensor>
        returns:
                pred_flag:      list<bool> True: 成功, False: 失败
                pred_num:       list<int> 病害数量
                pred_type:      list<list<DiseaseType>> 每个图片里面的病害分类
        """

        pred_flag = []
        pred_num = []
        pred_type = []

        for idx in range(len(detection_result)):
            ith_result = detection_result[idx].boxes.data # 第i个目标检测的预测框信息

            pred_box_num = ith_result.shape[0]
            pred_num.append(pred_box_num)
        
            pred_flag.append(pred_box_num != 0) # 是否有检测结果

            pred_type.append([DiseaseType(int(cls)).name for cls in ith_result[:, 5]]) # 分类信息

        return pred_flag, pred_num, pred_type

    # 加载预训练权重
    model = YOLO('weights/surface/best.pt')
    
    Inputdir = inputdir
    Outputdir = outputdir
    
    print('图片输入路径：',Inputdir)
    print('图片保存路径：',Outputdir)
    

    
    if not os.path.isabs(Outputdir):
        Outputdir = os.path.abspath(Outputdir)

    results = model.predict(source=Inputdir, save=True, name=Outputdir, show_conf=False, conf=0.3)

    pred_flag, pred_num, pred_type = post_process(results)

 
    
    create_image_json(Inputdir, Outputdir, pred_num, pred_type)  #将结果保存为json文件
    
    


