# 快速入门指南

## 安装步骤

### 1. 安装 Python 依赖
```bash
pip install -r requirements.txt
```

### 2. 安装 TensorRT
```bash
# 方法 1: 使用 pip（如果可用）
pip install tensorrt

# 方法 2: 从 NVIDIA 官网下载并安装
# https://developer.nvidia.com/tensorrt
```

## 使用方法

### 方法 1: 命令行使用（推荐）

#### 最简单的用法
```bash
python convert_yolov5_to_tensorrt.py --weights yolov5s.pt
```

这将生成：
- `yolov5s.onnx` - ONNX 格式模型
- `yolov5s.engine` - TensorRT 引擎

#### 常用命令

**使用 FP16 加速（推荐用于 GPU）**
```bash
python convert_yolov5_to_tensorrt.py --weights yolov5s.pt --fp16
```

**自定义输入尺寸**
```bash
python convert_yolov5_to_tensorrt.py --weights yolov5s.pt --img-size 1280
```

**仅转换为 ONNX**
```bash
python convert_yolov5_to_tensorrt.py --weights yolov5s.pt --onnx-only
```

**查看所有选项**
```bash
python convert_yolov5_to_tensorrt.py --help
```

### 方法 2: Python API 使用

```python
from convert_yolov5_to_tensorrt import YOLOv5Converter

# 创建转换器
converter = YOLOv5Converter(
    pt_model_path='yolov5s.pt',  # 你的模型路径
    img_size=640,                 # 输入图像尺寸
    batch_size=1,                 # 批次大小
    device='cpu'                  # 或 'cuda'
)

# 一键转换 PT -> ONNX -> TensorRT
onnx_path, engine_path = converter.convert_all()

print(f"✓ ONNX: {onnx_path}")
print(f"✓ TensorRT: {engine_path}")
```

### 方法 3: 手动使用 trtexec

如果已有 ONNX 模型，可直接使用 trtexec：

```bash
# 基础转换
trtexec --onnx=model.onnx --saveEngine=model.engine

# FP16 精度（更快）
trtexec --onnx=model.onnx --saveEngine=model.engine --fp16

# 增加工作空间（可能提升性能）
trtexec --onnx=model.onnx --saveEngine=model.engine --workspace=4096
```

## 实际示例

### 示例 1: 转换 YOLOv5s 模型

```bash
# 下载 YOLOv5s 模型（如果还没有）
wget https://github.com/ultralytics/yolov5/releases/download/v6.0/yolov5s.pt

# 转换
python convert_yolov5_to_tensorrt.py --weights yolov5s.pt

# 输出：
# yolov5s.onnx
# yolov5s.engine
```

### 示例 2: 转换大模型并优化

```bash
# 转换 YOLOv5x，使用 FP16 和更大的工作空间
python convert_yolov5_to_tensorrt.py \
    --weights yolov5x.pt \
    --img-size 1280 \
    --fp16 \
    --workspace 8 \
    --device cuda
```

### 示例 3: 仅生成 ONNX 用于部署

```bash
python convert_yolov5_to_tensorrt.py \
    --weights yolov5s.pt \
    --onnx-only \
    --simplify
```

## 转换流程说明

```
┌─────────────┐
│  YOLOv5 PT  │  PyTorch 训练的模型
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    ONNX     │  中间格式（跨平台）
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  TensorRT   │  优化的推理引擎
└─────────────┘
```

## 精度选项对比

| 精度 | 速度 | 精确度 | GPU 内存 | 推荐场景 |
|------|------|--------|----------|----------|
| FP32 | 1x   | 最高   | 最大     | 精度要求高 |
| FP16 | 2-3x | 很高   | 中等     | **推荐** |
| INT8 | 4-5x | 良好   | 最小     | 边缘设备 |

## 故障排查

### 问题 1: 找不到 torch 模块
```bash
pip install torch torchvision
```

### 问题 2: 找不到 trtexec
```bash
# 检查是否安装
which trtexec

# 如果没有，添加到 PATH
export PATH=$PATH:/usr/local/TensorRT/bin
```

### 问题 3: GPU 内存不足
```bash
# 减小工作空间或使用 CPU
python convert_yolov5_to_tensorrt.py --weights model.pt --workspace 2 --device cpu
```

## 下一步

1. 查看 `example_usage.py` 了解更多 Python API 用法
2. 阅读 `README.md` 了解详细文档
3. 根据需要调整参数以获得最佳性能

## 联系与支持

如遇问题，请检查：
- PyTorch 版本是否兼容
- CUDA/cuDNN 是否正确安装
- TensorRT 版本是否与 CUDA 匹配
