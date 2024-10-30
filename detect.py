from enum import Enum
from ultralytics import YOLO
from pprint import pprint
import os

def detect_bolt(inputdir1,inputdir2,outputdir):
    class DiseaseType(Enum):
        """
        外套螺栓  
        内嵌螺栓  
        螺栓缺失
        """

        bolt_out = 0
        bolt_in = 1
        missing = 2


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

            pred_type.append([DiseaseType(int(cls)).name for cls in ith_result[:, 4]]) # 分类信息

        return pred_flag, pred_num, pred_type


    # 加载预训练权重
    model = YOLO('weights/bolt/detect/weights/best.pt')

    Inputdir1 = inputdir1
    Inputdir2 = inputdir2
    Outputdir = outputdir

    if not os.path.isabs(Outputdir):
        Outputdir = os.path.abspath(Outputdir)
    
    first_filename = "first"
    second_filename = "second"
    
    new_outpath1 = os.path.join(Outputdir, first_filename)
    new_outpath2 = os.path.join(Outputdir, second_filename)

 
    results1 = model.predict(source=Inputdir1, save=True, save_txt=True, name=new_outpath1, conf=0.8)
    results2 = model.predict(source=Inputdir2, save=True, save_txt=True, name=new_outpath2, conf=0.8)
    pred_flag1, pred_num1, pred_type1 = post_process(results1)
    pred_flag2, pred_num2, pred_type2 = post_process(results2)


    
    #删除不含螺栓的照片
    def filter_images_without_detection(image_folder, output_folder, yolo_output_folder):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for filename in os.listdir(image_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                image_path = os.path.join(image_folder, filename)
                output_path = os.path.join(output_folder, filename)
                txt_file_path = os.path.join(yolo_output_folder, os.path.splitext(filename)[0] + ".txt")

                # 如果没有对应的txt文件，说明没有目标检测结果
                if not os.path.exists(txt_file_path):
                    os.remove(image_path)
                    os.remove(output_path)
                    
    filter_images_without_detection(Inputdir1, new_outpath1, os.path.join(new_outpath1, 'labels'))
    filter_images_without_detection(Inputdir2, new_outpath2, os.path.join(new_outpath2, 'labels'))
    
    
    
