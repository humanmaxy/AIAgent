# 快速参考卡片

## 🚀 一分钟快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动GUI（推荐）
python3 converter_gui.py

# 3. 或使用命令行
python3 convert_yolov5_to_tensorrt.py --weights yolov5s.pt --fp16
```

## 📁 核心文件速查

| 文件 | 用途 |
|------|------|
| `converter_gui.py` | 🎨 **GUI程序** - 点击使用 |
| `convert_yolov5_to_tensorrt.py` | ⌨️ **命令行** - 脚本使用 |
| `example_usage.py` | 📝 **API示例** - 代码集成 |

## 📚 文档速查

| 文档 | 何时查看 |
|------|----------|
| `INSTALLATION.md` | ❓ 首次安装 / 遇到问题 |
| `QUICKSTART.md` | 🎯 快速上手 |
| `GUI_USER_GUIDE.md` | 🖱️ 使用GUI时 |
| `README.md` | 📖 查看完整功能 |

## ⚙️ 常用命令

### GUI使用
```bash
# Linux/macOS
./run_gui.sh

# Windows
run_gui.bat

# 或直接运行
python3 converter_gui.py
```

### 命令行使用

#### 基础转换
```bash
python3 convert_yolov5_to_tensorrt.py --weights model.pt
```

#### FP16加速（推荐）
```bash
python3 convert_yolov5_to_tensorrt.py --weights model.pt --fp16
```

#### 高分辨率
```bash
python3 convert_yolov5_to_tensorrt.py --weights model.pt --img-size 1280 --fp16
```

#### 仅生成ONNX
```bash
python3 convert_yolov5_to_tensorrt.py --weights model.pt --onnx-only
```

#### 查看所有选项
```bash
python3 convert_yolov5_to_tensorrt.py --help
```

### Python API

```python
from convert_yolov5_to_tensorrt import YOLOv5Converter

# 基础使用
converter = YOLOv5Converter(pt_model_path='yolov5s.pt')
onnx_path, engine_path = converter.convert_all()

# 高级使用
converter = YOLOv5Converter(
    pt_model_path='yolov5s.pt',
    img_size=640,
    batch_size=1,
    device='cuda'
)
converter.convert_all(fp16=True, workspace=8)
```

## 🎛️ 重要参数

### 精度选择（影响速度）
- `FP32`: 最高精度，慢 (1x)
- `FP16`: **推荐**，快 (2-3x)
- `INT8`: 最快，需要校准 (4-5x)

### 输入尺寸（影响精度）
- `416`: 快速，精度低
- `640`: **默认**，平衡
- `1280`: 高精度，慢

### Workspace（影响性能）
- 小模型: 2-4 GB
- 中等模型: 4-6 GB
- 大模型: 6-8 GB

## 🔧 常见配置

### 配置1: 标准配置（推荐）
```bash
--weights yolov5s.pt
--img-size 640
--fp16
--workspace 4
```

### 配置2: 高性能
```bash
--weights yolov5s.pt
--img-size 640
--fp16
--workspace 8
--device cuda
```

### 配置3: 高精度
```bash
--weights yolov5x.pt
--img-size 1280
--workspace 8
```

### 配置4: 批量推理
```bash
--weights yolov5s.pt
--batch-size 8
--fp16
--workspace 6
```

## ❓ 常见问题速查

### Q: 找不到torch
```bash
pip install torch torchvision
```

### Q: 找不到tkinter
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk
```

### Q: 找不到trtexec
```bash
# 设置PATH
export PATH=$PATH:/usr/local/TensorRT/bin
```

### Q: CUDA错误
```bash
# 检查版本
nvcc --version
nvidia-smi
```

### Q: 内存不足
```bash
# 降低参数
--workspace 2
--batch-size 1
```

## 📊 输出文件

转换后生成：
- `model.onnx` - ONNX模型
- `model.engine` - TensorRT引擎

## 🎯 使用场景快速选择

| 场景 | 使用方式 | 参考 |
|------|----------|------|
| 转换一个模型 | GUI | `GUI_USER_GUIDE.md` |
| 批量转换 | 命令行 | `QUICKSTART.md` |
| 集成到代码 | Python API | `example_usage.py` |
| 首次使用 | GUI | `INSTALLATION.md` |

## 💡 提示

### GUI技巧
1. 选择PT文件后，输出目录自动设置
2. 默认参数通常就够用
3. 日志可以复制保存
4. 使用FP16可以2-3倍加速

### 命令行技巧
1. 先用`--help`查看所有选项
2. 先用小模型测试参数
3. 批量转换可以写脚本
4. 输出会保存在模型同目录

### Python技巧
1. 查看`example_usage.py`学习用法
2. 可以分步转换（先ONNX再TRT）
3. 使用异常处理捕获错误
4. 可以自定义转换流程

## 🔗 快速跳转

**遇到问题？**
1. `INSTALLATION.md` - 安装问题
2. `GUI_USER_GUIDE.md` - GUI问题
3. `README.md` - 参数问题

**想学更多？**
1. `GUI_FEATURES.md` - 界面详解
2. `PROJECT_SUMMARY.md` - 功能清单
3. `INDEX.md` - 文件索引

## ⚡ 性能参考

YOLOv5s在RTX 3080上：
- 转换时间: 3-5分钟
- FP32推理: ~8ms
- FP16推理: ~3ms
- INT8推理: ~2ms

## 📦 完整功能列表

- ✅ PT → ONNX 转换
- ✅ ONNX → TensorRT 转换
- ✅ FP32/FP16/INT8 精度
- ✅ 动态输入尺寸
- ✅ ONNX简化
- ✅ 图形界面
- ✅ 命令行工具
- ✅ Python API
- ✅ 实时日志
- ✅ 进度显示

## 🎓 学习路径

```
新手: INSTALLATION.md → QUICKSTART.md → GUI使用
进阶: README.md → 命令行使用 → 参数调优
专家: example_usage.py → API集成 → 自定义流程
```

---

**记住**: 
- 📖 遇到问题先查文档
- 🧪 先用小模型测试
- 💾 重要配置记得保存
- 📝 错误日志记得复制

**马上开始**: `python3 converter_gui.py`
