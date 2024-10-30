# -*- encoding: utf-8 -*-


from utils import *
from torch import nn
from models import SRResNet,Generator
import time
from PIL import Image

# 模型参数
large_kernel_size = 9   # 第一层卷积和最后一层卷积的核大小
small_kernel_size = 3   # 中间层卷积的核大小
n_channels = 64         # 中间层通道数
n_blocks = 16           # 残差模块数量
scaling_factor = 4      # 放大比例


# 图像文件夹
def clearify_bolt(input_folder,outputpath):
    #imgPath = './results/test.jpg'
    # 创建输出文件夹
    os.makedirs(outputpath, exist_ok=True)
    
    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        
        # 检查文件是否为图片文件
        if os.path.isfile(input_path) and any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
            SRGAN_Single_Bolt(input_path, outputpath)


def SRGAN_Single_Bolt(imgPath, outputpath):

    # 预训练模型
    srgan_checkpoint = "./results/checkpoint_srgan.pth"
    #srresnet_checkpoint = "./results/checkpoint_srresnet.pth"
    
    #检测GPU是否可用
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # 加载模型SRResNet 或 SRGAN
    checkpoint = torch.load(srgan_checkpoint)
    generator = Generator(large_kernel_size=large_kernel_size,
                        small_kernel_size=small_kernel_size,
                        n_channels=n_channels,
                        n_blocks=n_blocks,
                        scaling_factor=scaling_factor)
    generator = generator.to(device)
    generator.load_state_dict(checkpoint['generator'])
   
    generator.eval()
    model = generator

    # 加载图像
    img = Image.open(imgPath, mode='r')
    img = img.convert('RGB')

    # 图像预处理
    lr_img = convert_image(img, source='pil', target='imagenet-norm')
    lr_img.unsqueeze_(0)

    # 记录时间
    start = time.time()

    # 转移数据至设备
    lr_img = lr_img.to(device)  # (1, 3, w, h ), imagenet-normed

    # 模型推理
    with torch.no_grad():
        sr_img = model(lr_img).squeeze(0).cpu().detach()  # (1, 3, w*scale, h*scale), in [-1, 1]   
        sr_img = convert_image(sr_img, source='[-1, 1]', target='pil')
        #sr_img.save('./results/test_srgan.jpg')
        sr_img.save(imgPath)

    print('用时  {:.3f} 秒'.format(time.time()-start))
