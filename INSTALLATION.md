# 安装指南

## 系统要求

### 必需组件
- Python 3.7+
- pip (Python包管理器)

### 可选组件（根据使用方式）
- CUDA Toolkit 10.2+ (GPU加速)
- cuDNN 7.6+ (GPU加速)
- TensorRT 7.0+ (TensorRT转换)

## 安装步骤

### 1. 安装Python依赖

```bash
# 基础依赖
pip install torch torchvision onnx onnxruntime

# 可选：ONNX简化工具
pip install onnx-simplifier

# 或者一键安装所有依赖
pip install -r requirements.txt
```

### 2. 安装GUI支持 (仅GUI版本需要)

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install python3-tk
```

#### CentOS/RHEL
```bash
sudo yum install python3-tkinter
```

#### macOS
```bash
# 通常已预装，如需安装：
brew install python-tk@3.11
```

#### Windows
```bash
# Python安装时通常已包含tkinter
# 如果没有，重新安装Python并勾选 "tcl/tk and IDLE"
```

### 3. 安装TensorRT (可选，用于TensorRT转换)

#### 方法1: 使用pip (推荐，如果可用)
```bash
pip install tensorrt
```

#### 方法2: 从NVIDIA官网下载
1. 访问 https://developer.nvidia.com/tensorrt
2. 下载对应CUDA版本的TensorRT
3. 解压并安装：

```bash
# 例如：TensorRT 8.5.3 for Ubuntu 20.04 and CUDA 11.8
tar -xzvf TensorRT-8.5.3.1.Linux.x86_64-gnu.cuda-11.8.cudnn8.6.tar.gz
cd TensorRT-8.5.3.1

# 添加到环境变量
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)/lib
export PATH=$PATH:$(pwd)/bin

# 安装Python包
cd python
pip install tensorrt-8.5.3.1-cp38-none-linux_x86_64.whl
```

#### 方法3: Docker镜像 (推荐生产环境)
```bash
# 使用NVIDIA的TensorRT容器
docker pull nvcr.io/nvidia/tensorrt:22.12-py3
docker run --gpus all -it -v $(pwd):/workspace nvcr.io/nvidia/tensorrt:22.12-py3
```

### 4. 验证安装

#### 验证Python依赖
```bash
python3 -c "import torch; print(f'PyTorch: {torch.__version__}')"
python3 -c "import onnx; print(f'ONNX: {onnx.__version__}')"
```

#### 验证GUI支持
```bash
python3 -c "import tkinter; print('Tkinter OK')"
```

#### 验证TensorRT
```bash
# 检查trtexec
which trtexec
trtexec --help

# 检查Python包
python3 -c "import tensorrt; print(f'TensorRT: {tensorrt.__version__}')"
```

#### 运行测试脚本
```bash
cd /workspace
python3 test_gui_import.py
```

## 常见问题

### Q1: pip install torch 很慢或失败

**方案1**: 使用清华镜像源
```bash
pip install torch torchvision -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**方案2**: 从PyTorch官网选择对应版本
```bash
# 访问 https://pytorch.org/get-started/locally/
# 例如：CPU版本
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### Q2: 找不到tkinter

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**如果上述方法无效，重新安装Python:**
```bash
sudo apt-get install python3-full
```

### Q3: TensorRT安装失败

**检查CUDA版本:**
```bash
nvcc --version
nvidia-smi
```

确保下载的TensorRT版本与CUDA版本匹配。

**版本对应关系:**
- CUDA 11.8 → TensorRT 8.5.x
- CUDA 11.4 → TensorRT 8.2.x
- CUDA 10.2 → TensorRT 7.2.x

### Q4: 权限错误

```bash
# 使用用户安装
pip install --user -r requirements.txt

# 或使用虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Q5: ImportError: libcudart.so 找不到

```bash
# 添加CUDA库路径
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH

# 永久添加到环境变量
echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```

## 推荐安装方式

### 开发环境 (带GUI)
```bash
# 1. 创建虚拟环境
python3 -m venv yolov5_env
source yolov5_env/bin/activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 安装系统包（GUI支持）
sudo apt-get install python3-tk

# 4. 安装TensorRT (根据CUDA版本)
pip install tensorrt
```

### 服务器环境 (命令行)
```bash
# 1. 创建虚拟环境
python3 -m venv yolov5_env
source yolov5_env/bin/activate

# 2. 安装依赖
pip install torch torchvision onnx onnx-simplifier

# 3. 安装TensorRT
# 从NVIDIA官网下载对应版本
```

### Docker环境 (推荐生产环境)
```dockerfile
FROM nvcr.io/nvidia/tensorrt:22.12-py3

WORKDIR /workspace

# 复制文件
COPY requirements.txt .
COPY *.py .

# 安装依赖
RUN pip install -r requirements.txt

# 运行
CMD ["python3", "convert_yolov5_to_tensorrt.py", "--help"]
```

## 最小安装

如果只需要PT到ONNX转换（不需要TensorRT）：

```bash
# 只安装基础依赖
pip install torch onnx onnx-simplifier

# 使用时添加 --onnx-only 参数
python3 convert_yolov5_to_tensorrt.py --weights model.pt --onnx-only
```

## 测试安装是否成功

```bash
# 1. 测试命令行工具
python3 convert_yolov5_to_tensorrt.py --help

# 2. 测试GUI (如果安装了tkinter)
python3 converter_gui.py

# 3. 运行导入测试
python3 test_gui_import.py
```

## 环境变量配置

建议添加到 `~/.bashrc` 或 `~/.zshrc`:

```bash
# CUDA
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH

# TensorRT
export PATH=/path/to/TensorRT/bin:$PATH
export LD_LIBRARY_PATH=/path/to/TensorRT/lib:$LD_LIBRARY_PATH

# Python
export PYTHONPATH=/path/to/TensorRT/python:$PYTHONPATH
```

## 下一步

安装完成后，请参阅：
- GUI使用：`GUI_USER_GUIDE.md`
- 命令行使用：`QUICKSTART.md`
- 完整文档：`README.md`
