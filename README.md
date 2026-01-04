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
├── bolt_vision.py              # bolt perspective correction
├── cut.py
├── delete_broken_photo.py
├── detect.py
├── detect_s.py
├── koutu.py
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
