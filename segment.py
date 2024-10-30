from enum import Enum
from ultralytics import YOLO


def segment_bolt(inputdir,outputdir):

    class DiseaseType(Enum):
        """      
        螺母  
        螺杆
        """
        nut   = 0
        screw = 1


    def post_process(detection_result):
        """
        args:
            detection_result: list<torch.tensor>
            returns:
                pred_flag:      list<bool> True: 成功, False: 失败
                pred_num:       list<int> 分类数量
                pred_type:      list<list<DiseaseType>> 每个图片里面的分类
        """

        pred_flag = []
        pred_num  = []
        pred_type = []

        for idx in range(len(detection_result)):
            ith_result = detection_result[idx].boxes.data # 第i个目标检测的预测框信息

            pred_box_num = ith_result.shape[0]
            pred_num.append(pred_box_num)

            pred_flag.append(pred_box_num != 0) # 是否有检测结果

            pred_type.append([DiseaseType(int(cls)).name for cls in ith_result[:, 4]]) # 分类信息

        return pred_flag, pred_num, pred_type


    # 加载预训练权重
    model = YOLO('weights/bolt/segment/weights/best.pt')

    # 警告可以忽略
    results = model.predict(source=inputdir, save=True, name=outputdir, save_txt=True, conf=0.4)
    pred_flag, pred_num, pred_type = post_process(results)
    

