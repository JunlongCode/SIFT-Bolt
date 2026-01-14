# Infrastructure Visual Inspection Framework  
## Bolt Loosening Quantification and Surface Defect Detection

This repository provides an integrated computer vision framework for **infrastructure visual inspection**, including:

- **Quantitative bolt loosening assessment** with full-range rotation measurement  
- **Surface appearance defect detection**, including:
  - Crack
  - Rust
  - Coating spalling / peeling

The framework is designed for **engineering inspection scenarios** and emphasizes **reproducibility, robustness, and practical applicability**.

---

## 1. Framework Overview

The core pipeline is implemented in **`integration.py`**, which integrates multiple vision modules into a unified workflow.

### 1.1 Bolt Loosening Quantification Pipeline

The bolt loosening quantification framework consists of the following stages:

1. YOLO-based bolt object detection  
2. Semantic segmentation of bolt regions  
3. Image super-resolution reconstruction to enhance local texture details  
4. SIFT-Bolt feature point generation, matching, and filtering  
5. Rotation angle calculation based on rigid-body transformation

**Key capability**:
- Full-range bolt rotation measurement within **[0°, 360°)**  
- Overcomes the **0°–60° limitation** of conventional flange-based 2D image methods

---

## 2. Surface Defect Detection

In addition to bolt loosening assessment, this repository provides YOLO-based visual inspection models for common surface defects, including:

- Crack detection / segmentation  
- Rust detection / segmentation  
- Coating spalling detection / segmentation  

These defect detection modules can be executed independently or jointly with the bolt inspection pipeline.

---

## 3. Repository Structure

```text
.
├── README.md
├── requirements.txt
├── integration.py              # main integrated pipeline
├── weights/                    # pretrained model weights (public)
│   ├── bolts/
│   │   ├── detect/
│   │   │   └── bolt detection weight
│   │   └── segment/
│   │       └── bolt segmentation weight
│   └── surface segmentation weight
├── inference/
│   ├── rename.py
│   ├── surface image folder/
│   └── bolt image folder/
│       ├── first/
│       └── second/
├── SRGAN
│   ├── results/
│   │   └── SRGAN weight
│   └── test.py
├── bolt_vision.py             
├── cut.py                    # crop from detection results
├── delete_broken_photo.py
├── detect.py
├── detect_s.py
├── koutu.py                  # crop from segmentation results
├── models.py
├── segment.py
├── setup.py
├── show_result.py
├── sift_bolt.py
├── test_getpath.py
├── test_match.py
├── utils.py
└── wright_json.py
```
---
## 4. Dataset

The datasets are hosted on Microsoft OneDrive and can be freely accessed for research and academic purposes:
- [Bolt object detection](https://hnueducn-my.sharepoint.com/:u:/g/personal/liujunlong_hnu_edu_cn/IQAeuRxWXjiyQbpf73MxkUo8ATzdhU56KmE1Spe9amdzr2U?e=IbD7ax)
- [Bolt segmentation and super-resolution reconstruction](https://hnueducn-my.sharepoint.com/:u:/g/personal/zwliu_hnu_edu_cn/IQCnEMmLmbYVRaMyCZ-simwVAcOf7ofnHurOJQBxupKgG30?e=3LBgJd)
---

---
## 5. Weights

The model weights trained in this study are publicly available via OneDrive:
- Bolt object detection:
  - [YOLOv8n](https://hnueducn-my.sharepoint.com/:f:/g/personal/liujunlong_hnu_edu_cn/IgBjvQihvdIGR46PscubGUZ6ARJo7uRWaACRkPwdL_7urqA?e=cP3BXd)
  - [YOLOv9c](https://hnueducn-my.sharepoint.com/:f:/g/personal/liujunlong_hnu_edu_cn/IgCS8u7RPYw4T67HrxVcIPc0ATGCiqDUd2iVUKvPBZddeDc?e=vnOXgd)
  - [YOLOv10n](https://hnueducn-my.sharepoint.com/:f:/g/personal/liujunlong_hnu_edu_cn/IgDOFvnN5xwRSLvssg2Km5OJATo6JFrL1iINd1gb-TWonJ0?e=oVJl51)
  - [YOLOv11n](https://hnueducn-my.sharepoint.com/:f:/g/personal/liujunlong_hnu_edu_cn/IgCJUR2wavICSJ4RE_nqFF52ASVz5lfgYnUb8Tx2R8K6wkk?e=o0faEX)
  - [YOLOv12n](https://hnueducn-my.sharepoint.com/:f:/g/personal/liujunlong_hnu_edu_cn/IgAFPKiQhfxhRaqnorzvjNTuAT2zqhAHMQjWSqntLy0EeTw?e=TeEvGU)
- Bolt segmentation:
  - [YOLOv8n](https://hnueducn-my.sharepoint.com/:f:/g/personal/liujunlong_hnu_edu_cn/IgAoYi2aIH5jRrwf1dKitglsAcm00daiDOGhbcPTW9Vpzeg?e=WHkQLz)
  - [YOLOv8-P6](https://hnueducn-my.sharepoint.com/:f:/g/personal/liujunlong_hnu_edu_cn/IgB-0MwNS-72SY4hWf3RGfhwAb-T1vvofkwIij_1XaI17Ak?e=vstSBw)
  - [YOLOv9c](https://hnueducn-my.sharepoint.com/:f:/g/personal/liujunlong_hnu_edu_cn/IgB3-FTs4L-EQ5xjV8slwH5BAez1iOkLeBLF3E87mEfpq-g?e=3C26Zy)
  - [YOLOv10n](https://hnueducn-my.sharepoint.com/:f:/g/personal/liujunlong_hnu_edu_cn/IgCu16B9d_pLT4O70QL4I2WUAa9EhKQJ7Cp5BLGkjoBH2_k?e=dsW3MW)
  - [YOLOv11n](https://hnueducn-my.sharepoint.com/:f:/g/personal/liujunlong_hnu_edu_cn/IgBMcGaqa2JVSqzVWaLWm0ENAf8v0MbGsgc7X9RLUFso_8Y?e=ccF1Mo)
  - [YOLOv12n](https://hnueducn-my.sharepoint.com/:f:/g/personal/liujunlong_hnu_edu_cn/IgCZEuO8W1LbT7LBviP_NltKAbeaVzyvn7IOWif00q7k_Vo?e=FZFmSI)
- Bolt super-resolution reconstruction:
  - [SRGAN](https://hnueducn-my.sharepoint.com/:u:/g/personal/liujunlong_hnu_edu_cn/IQCfAjkTQmEcRJbw8U4F7BrdAXSf5skbb2e4mztlsJiXRPU?e=coHYq6)
---

---
## 6. Run


---

## Citation

This project makes use of the **Ultralytics YOLO** implementation for object detection and segmentation tasks.

If you use this repository, please also consider citing the Ultralytics YOLO framework:

```bibtex
@software{Jocher_Ultralytics_YOLO_2023,
  author  = {Jocher, Glenn and Chaurasia, Ayush and Qiu, Jing},
  title   = {Ultralytics YOLO},
  year    = {2023},
  publisher = {GitHub},
  url     = {https://github.com/ultralytics/ultralytics}
}
