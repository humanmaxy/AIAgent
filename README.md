# YOLOv5 模型转换工具

将 YOLOv5 PyTorch 模型（.pt）转换为 ONNX 和 TensorRT 格式的完整工具。

## 功能特性

- ✅ PyTorch (.pt) → ONNX 转换
- ✅ ONNX → TensorRT 引擎转换
- ✅ 支持 FP16/INT8 精度优化
- ✅ 支持动态输入尺寸
- ✅ ONNX 模型简化
- ✅ **图形界面（GUI）** - 简单易用
- ✅ 命令行和 Python API 两种使用方式

## 安装依赖

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装 TensorRT (必须单独安装)
# 方法 1: 使用 pip (如果可用)
pip install tensorrt

# 方法 2: 从 NVIDIA 官网下载
# https://developer.nvidia.com/tensorrt
```

## 快速开始

### 🎨 图形界面（推荐新手使用）

#### 启动 GUI
```bash
# Windows
run_gui.bat

# Linux / macOS
./run_gui.sh
# 或
python3 converter_gui.py
```

#### GUI 特点
- 📁 可视化文件选择
- ⚙️ 直观的参数配置
- 📊 实时转换日志
- 🎯 一键转换功能
- 💡 适合不熟悉命令行的用户

详细使用说明请查看 [GUI_USER_GUIDE.md](GUI_USER_GUIDE.md)

### 1. 命令行使用

#### 基础转换
```bash
python convert_yolov5_to_tensorrt.py --weights yolov5s.pt
```

#### 使用 FP16 精度
```bash
python convert_yolov5_to_tensorrt.py --weights yolov5s.pt --fp16
```

#### 自定义图像尺寸
```bash
python convert_yolov5_to_tensorrt.py --weights yolov5s.pt --img-size 1280
```

#### 只转换为 ONNX（跳过 TensorRT）
```bash
python convert_yolov5_to_tensorrt.py --weights yolov5s.pt --onnx-only
```

#### 动态输入尺寸
```bash
python convert_yolov5_to_tensorrt.py --weights yolov5s.pt --dynamic
```

### 2. Python API 使用

```python
from convert_yolov5_to_tensorrt import YOLOv5Converter

# 创建转换器
converter = YOLOv5Converter(
    pt_model_path='yolov5s.pt',
    img_size=640,
    batch_size=1,
    device='cpu'
)

# 完整转换 PT -> ONNX -> TensorRT
onnx_path, engine_path = converter.convert_all()

# 或者分步转换
# 步骤 1: PT -> ONNX
onnx_path = converter.convert_pt_to_onnx(simplify=True, dynamic=False)

# 步骤 2: ONNX -> TensorRT
engine_path = converter.convert_onnx_to_tensorrt(fp16=True, workspace=4)
```

## 命令行参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--weights` | str | 必需 | YOLOv5 .pt 模型文件路径 |
| `--img-size` | int | 640 | 输入图像尺寸 |
| `--batch-size` | int | 1 | 批次大小 |
| `--device` | str | cpu | 使用的设备 (cpu/cuda) |
| `--opset` | int | 12 | ONNX opset 版本 |
| `--simplify` | flag | True | 简化 ONNX 模型 |
| `--no-simplify` | flag | - | 不简化 ONNX 模型 |
| `--dynamic` | flag | False | 使用动态输入尺寸 |
| `--fp16` | flag | False | TensorRT 使用 FP16 精度 |
| `--int8` | flag | False | TensorRT 使用 INT8 精度 |
| `--workspace` | int | 4 | TensorRT 工作空间大小（GB）|
| `--onnx-only` | flag | False | 仅转换为 ONNX |

## 使用示例

### 示例 1: 基础转换
```bash
python convert_yolov5_to_tensorrt.py --weights yolov5s.pt
```
输出文件：
- `yolov5s.onnx`
- `yolov5s.engine`

### 示例 2: 高精度模型（更大输入尺寸 + FP16）
```bash
python convert_yolov5_to_tensorrt.py \
    --weights yolov5x.pt \
    --img-size 1280 \
    --fp16 \
    --workspace 8
```

### 示例 3: GPU 加速转换
```bash
python convert_yolov5_to_tensorrt.py \
    --weights yolov5m.pt \
    --device cuda \
    --fp16
```

### 示例 4: 仅生成 ONNX（用于其他框架）
```bash
python convert_yolov5_to_tensorrt.py \
    --weights yolov5s.pt \
    --onnx-only \
    --simplify
```

## Python API 示例

详细示例请参考 `example_usage.py` 文件。

### 基础用法
```python
from convert_yolov5_to_tensorrt import YOLOv5Converter

converter = YOLOv5Converter(pt_model_path='yolov5s.pt')
onnx_path, engine_path = converter.convert_all()
```

### 高级用法
```python
converter = YOLOv5Converter(
    pt_model_path='yolov5s.pt',
    img_size=640,
    batch_size=1,
    device='cuda'
)

onnx_path, engine_path = converter.convert_all(
    simplify=True,      # 简化 ONNX
    dynamic=False,      # 固定输入尺寸
    opset=12,          # ONNX opset 版本
    fp16=True,         # 使用 FP16
    workspace=8        # 8GB 工作空间
)
```

## 手动使用 trtexec

如果 Python 脚本无法自动调用 trtexec，可以手动运行：

```bash
# 基础转换
trtexec --onnx=model.onnx --saveEngine=model.engine

# FP16 精度
trtexec --onnx=model.onnx --saveEngine=model.engine --fp16

# 指定工作空间
trtexec --onnx=model.onnx --saveEngine=model.engine --workspace=4096

# 完整示例
trtexec \
    --onnx=yolov5s.onnx \
    --saveEngine=yolov5s.engine \
    --fp16 \
    --workspace=4096 \
    --verbose
```

## 文件结构

```
.
├── converter_gui.py                # 图形界面程序 (推荐)
├── convert_yolov5_to_tensorrt.py  # 命令行转换脚本
├── run_gui.sh                      # GUI启动脚本 (Linux/macOS)
├── run_gui.bat                     # GUI启动脚本 (Windows)
├── requirements.txt                # Python 依赖
├── example_usage.py               # API使用示例
├── GUI_USER_GUIDE.md              # GUI详细使用指南
├── QUICKSTART.md                  # 快速入门
└── README.md                      # 说明文档
```

## 常见问题

### 1. 找不到 trtexec
确保 TensorRT 已安装并且 trtexec 在 PATH 中：
```bash
which trtexec
# 或者添加到 PATH
export PATH=$PATH:/path/to/tensorrt/bin
```

### 2. CUDA 相关错误
确保已安装正确版本的 CUDA 和 cuDNN，并且与 TensorRT 版本兼容。

### 3. 内存不足
降低 `--workspace` 参数或使用更小的模型。

### 4. ONNX 简化失败
使用 `--no-simplify` 跳过简化步骤：
```bash
python convert_yolov5_to_tensorrt.py --weights model.pt --no-simplify
```

## 性能建议

1. **FP16 vs FP32**: FP16 可以显著提升推理速度（约 2-3x），精度损失很小
2. **工作空间**: 增大 workspace 可能提升性能，但会占用更多 GPU 内存
3. **批次大小**: 根据 GPU 内存调整 batch size
4. **输入尺寸**: 较小的输入尺寸（如 416）会更快，但精度较低

## 版本要求

- Python >= 3.7
- PyTorch >= 1.9.0
- ONNX >= 1.9.0
- TensorRT >= 7.0.0
- CUDA >= 10.2 (使用 GPU 时)

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
