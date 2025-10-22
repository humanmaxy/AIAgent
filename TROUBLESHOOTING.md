# 故障排查指南

## 常见问题及解决方案

### 1. PyTorch 2.6+ Weights Only Load Failed ⭐ 新问题

#### 问题描述
```
_pickle.UnpicklingError: Weights only load failed.
WeightsUnpickler error: Unsupported global: GLOBAL ultralytics.nn.tasks.DetectionModel
```

#### 原因
PyTorch 2.6改变了`torch.load()`的默认行为，默认启用`weights_only=True`，不允许加载包含自定义类的模型。

#### 解决方案
**已在v1.2版本修复！** 更新到最新版本即可。

如果需要手动修复，在两个文件中添加`weights_only=False`参数：

**converter_gui.py (第431行)**:
```python
model = torch.load(str(pt_path), map_location=self.device.get(), weights_only=False)
```

**convert_yolov5_to_tensorrt.py (第73行)**:
```python
model = torch.load(self.pt_model_path, map_location=self.device, weights_only=False)
```

#### 检查PyTorch版本
```bash
python -c "import torch; print(torch.__version__)"
```

详细说明请查看 `PYTORCH_2.6_FIX.md`

---

### 2. TracerWarning 警告

#### 问题描述
```
TracerWarning: Converting a tensor to a Python boolean might cause the trace to be incorrect.
TracerWarning: Iterating over a tensor might cause the trace to be incorrect.
```

#### 原因
这是使用 Ultralytics YOLOv5 模型时的正常警告。模型中包含一些动态判断逻辑，导出 ONNX 时会产生这些警告。

#### 解决方案
**已修复！** 最新版本的转换工具已经自动抑制这些警告。警告不会影响转换结果。

如果仍然看到警告，可以忽略，转换后的 ONNX 和 TensorRT 模型是正常可用的。

#### 验证转换结果
```python
import onnx

# 加载并检查ONNX模型
model = onnx.load("yolov5s.onnx")
onnx.checker.check_model(model)
print("✓ ONNX模型有效")
```

---

### 2. GUI错误：NameError in lambda callback

#### 问题描述
```
Exception in Tkinter callback
NameError: cannot access free variable 'e' where it is not associated with a value
```

#### 原因
旧版本GUI中的错误处理代码有作用域问题。

#### 解决方案
**已修复！** 更新到最新版本的 `converter_gui.py` 即可。

如果使用的是旧版本，请下载最新版本或手动修改第405行：

```python
# 修改前（错误）
self.root.after(0, lambda: messagebox.showerror("错误", f"转换失败:\n{str(e)}"))

# 修改后（正确）
error_msg = str(e)
self.root.after(0, lambda msg=error_msg: messagebox.showerror("错误", f"转换失败:\n{msg}"))
```

---

### 3. 模型加载失败

#### 问题描述
```
RuntimeError: Error loading model
KeyError: 'model'
```

#### 原因
PT模型文件格式不兼容或损坏。

#### 解决方案

1. **检查模型文件**
```bash
# 确保文件存在且完整
ls -lh your_model.pt

# 检查文件大小（不应该太小）
```

2. **验证模型可加载**
```python
import torch

# 尝试加载模型
model = torch.load('your_model.pt', map_location='cpu')
print(type(model))
print(model.keys() if isinstance(model, dict) else "Not a dict")
```

3. **使用正确的YOLOv5模型**
- 确保是官方训练的模型或使用官方代码训练的模型
- 支持的模型格式：
  - Ultralytics YOLOv5 (官方)
  - 标准 PyTorch 模型

---

### 4. CUDA相关错误

#### 问题描述
```
RuntimeError: CUDA out of memory
RuntimeError: No CUDA GPUs are available
```

#### 解决方案

**内存不足：**
```bash
# 使用CPU代替
python3 converter_gui.py
# 在GUI中选择设备为 "cpu"

# 或命令行
python3 convert_yolov5_to_tensorrt.py --weights model.pt --device cpu
```

**找不到CUDA：**
```bash
# 检查CUDA是否安装
nvidia-smi
nvcc --version

# 如果没有CUDA，使用CPU模式
# 在GUI中：设备选择 "cpu"
# 命令行：添加 --device cpu
```

---

### 5. ONNX简化失败

#### 问题描述
```
⚠ ONNX simplification failed, using original model
```

#### 原因
某些复杂模型无法简化，或 onnx-simplifier 版本问题。

#### 解决方案

1. **忽略警告** - 使用未简化的ONNX模型仍然可以正常工作

2. **更新 onnx-simplifier**
```bash
pip install --upgrade onnx-simplifier
```

3. **跳过简化**
- GUI：取消勾选「简化ONNX模型」
- 命令行：使用 `--no-simplify`

---

### 6. TensorRT转换失败

#### 问题描述
```
✗ Error: trtexec not found
✗ TensorRT conversion failed
```

#### 解决方案

**找不到trtexec：**

1. **检查是否安装TensorRT**
```bash
which trtexec
# 如果找不到，需要安装TensorRT
```

2. **设置trtexec路径**
- GUI：点击「trtexec路径」的「浏览...」选择trtexec文件
- 常见位置：`/usr/local/TensorRT/bin/trtexec`

3. **添加到PATH**
```bash
export PATH=$PATH:/usr/local/TensorRT/bin
```

**仅需要ONNX：**
- GUI：勾选「仅转换为ONNX」
- 命令行：使用 `--onnx-only`

---

### 7. 动态输入尺寸问题

#### 问题描述
```
ONNX export failed with dynamic axes
```

#### 解决方案

1. **使用固定尺寸** - 取消勾选「动态输入尺寸」

2. **调整OPSET版本**
```bash
# GUI: 将OPSET版本设置为 11 或更高
# 命令行:
python3 convert_yolov5_to_tensorrt.py --weights model.pt --opset 11 --dynamic
```

3. **检查模型兼容性** - 某些模型不支持动态输入

---

### 8. 输入输出名称错误

#### 问题描述
```
ONNX graph has incorrect input/output names
```

#### 解决方案

**YOLOv5常用名称：**
- 输入名称：`images`
- 输出名称：`output` 或 `output0`

**验证ONNX模型的输入输出：**
```python
import onnx

model = onnx.load("model.onnx")
print("Inputs:", [i.name for i in model.graph.input])
print("Outputs:", [o.name for o in model.graph.output])
```

---

### 9. 权限错误

#### 问题描述
```
PermissionError: [Errno 13] Permission denied
```

#### 解决方案

1. **检查输出目录权限**
```bash
# 创建可写目录
mkdir ~/yolo_output
chmod 755 ~/yolo_output
```

2. **使用管理员权限**
```bash
# Linux/macOS
sudo python3 converter_gui.py

# Windows: 以管理员身份运行
```

---

### 10. 版本兼容性问题

#### 问题描述
```
ImportError: cannot import name '...'
AttributeError: module has no attribute '...'
```

#### 解决方案

**检查版本：**
```bash
python3 --version  # 需要 3.7+
pip list | grep torch
pip list | grep onnx
```

**推荐版本组合：**
```bash
# PyTorch 1.12+ with CUDA 11.6
pip install torch==1.12.0+cu116 torchvision==0.13.0+cu116 --extra-index-url https://download.pytorch.org/whl/cu116

# ONNX
pip install onnx==1.12.0 onnxruntime==1.12.0

# 简化工具
pip install onnx-simplifier==0.4.10
```

---

## 性能优化建议

### 1. 加速转换过程

**使用GPU：**
```bash
# GUI: 设备选择 "cuda"
# 命令行:
python3 convert_yolov5_to_tensorrt.py --weights model.pt --device cuda
```

**跳过简化（如果不需要）：**
- GUI: 取消勾选「简化ONNX模型」
- 命令行: `--no-simplify`

### 2. 优化TensorRT性能

**使用FP16：**
```bash
python3 convert_yolov5_to_tensorrt.py --weights model.pt --fp16
```

**增加workspace：**
```bash
python3 convert_yolov5_to_tensorrt.py --weights model.pt --workspace 8
```

### 3. 减少内存使用

**降低batch size：**
- GUI: Batch Size设置为1
- 命令行: `--batch-size 1`

**使用CPU：**
```bash
--device cpu
```

---

## 调试技巧

### 1. 启用详细日志

**命令行模式：**
```bash
# 添加更多输出
python3 convert_yolov5_to_tensorrt.py --weights model.pt 2>&1 | tee conversion.log
```

**Python脚本调试：**
```python
import logging
logging.basicConfig(level=logging.DEBUG)

from convert_yolov5_to_tensorrt import YOLOv5Converter
converter = YOLOv5Converter(pt_model_path='model.pt')
# ... 进行转换
```

### 2. 分步转换

**先转ONNX：**
```bash
python3 convert_yolov5_to_tensorrt.py --weights model.pt --onnx-only
```

**再转TensorRT：**
```bash
trtexec --onnx=model.onnx --saveEngine=model.engine --fp16
```

### 3. 验证中间结果

**测试ONNX模型：**
```python
import onnxruntime as ort
import numpy as np

# 加载ONNX模型
session = ort.InferenceSession("model.onnx")

# 创建测试输入
input_name = session.get_inputs()[0].name
input_shape = session.get_inputs()[0].shape
dummy_input = np.random.randn(*input_shape).astype(np.float32)

# 推理测试
output = session.run(None, {input_name: dummy_input})
print("ONNX推理成功！输出shape:", [o.shape for o in output])
```

---

## 环境检查清单

在转换前，确保以下条件满足：

- [ ] Python 3.7 或更高版本
- [ ] PyTorch 已安装 (`pip list | grep torch`)
- [ ] ONNX 已安装 (`pip list | grep onnx`)
- [ ] PT模型文件存在且完整
- [ ] 有足够的磁盘空间（至少2倍模型大小）
- [ ] 输出目录有写权限
- [ ] (可选) TensorRT已安装（如需转TRT）
- [ ] (可选) CUDA已安装（如需GPU加速）

**快速检查脚本：**
```bash
python3 test_gui_import.py
```

---

## 获取帮助

### 查看日志

**GUI模式：**
- 日志显示在界面底部
- 可以复制日志内容用于分析

**命令行模式：**
```bash
# 保存日志到文件
python3 convert_yolov5_to_tensorrt.py --weights model.pt 2>&1 | tee log.txt
```

### 报告问题

提供以下信息：
1. 错误日志（完整的traceback）
2. 系统信息（OS、Python版本）
3. 依赖版本（torch、onnx版本）
4. 使用的命令或配置
5. 模型信息（YOLOv5版本、模型大小）

### 相关文档

- [INSTALLATION.md](INSTALLATION.md) - 安装问题
- [GUI_USER_GUIDE.md](GUI_USER_GUIDE.md) - GUI使用问题
- [README.md](README.md) - 功能和参数说明

---

## 已知问题

### Ultralytics TracerWarning
- **状态**: 已修复 ✅
- **影响**: 仅显示警告，不影响功能
- **解决**: 最新版本已自动抑制

### Lambda作用域错误
- **状态**: 已修复 ✅
- **影响**: GUI错误提示失败
- **解决**: 更新到最新版本

---

**更新日期**: 2025-10-21  
**版本**: 1.1
