# PyTorch 2.6 兼容性修复

## 🚨 问题描述

如果您使用 **PyTorch 2.6 或更高版本**，会遇到以下错误：

```
_pickle.UnpicklingError: Weights only load failed. This file can still be loaded, 
to do so you have two options, do those steps only if you trust the source of 
the checkpoint.

(1) In PyTorch 2.6, we changed the default value of the `weights_only` argument 
in `torch.load` from `False` to `True`.

WeightsUnpickler error: Unsupported global: GLOBAL ultralytics.nn.tasks.DetectionModel 
was not an allowed global by default.
```

## 🔍 原因分析

### PyTorch 2.6的安全性改进

PyTorch 2.6引入了重大安全变更：
- **旧版本**（<2.6）：`torch.load()` 默认 `weights_only=False`
- **新版本**（≥2.6）：`torch.load()` 默认 `weights_only=True`

### 为什么会影响Ultralytics模型？

Ultralytics YOLOv5模型包含自定义Python类（如`DetectionModel`），这些类在`weights_only=True`模式下不被允许加载，因为存在潜在的代码执行风险。

## ✅ 解决方案

### 方案1: 更新到v1.2（推荐）

**步骤1**: 备份您的文件
```bash
copy converter_gui.py converter_gui.py.backup
```

**步骤2**: 更新代码

在您的 `converter_gui.py` 文件中，找到第431行附近：

**修改前：**
```python
model = torch.load(str(pt_path), map_location=self.device.get())
```

**修改后：**
```python
# PyTorch 2.6+ 需要 weights_only=False 来加载 Ultralytics 模型
model = torch.load(str(pt_path), map_location=self.device.get(), weights_only=False)
```

**同样修改** `convert_yolov5_to_tensorrt.py`：

找到：
```python
model = torch.load(self.pt_model_path, map_location=self.device)
```

改为：
```python
# PyTorch 2.6+ requires weights_only=False for Ultralytics models
model = torch.load(self.pt_model_path, map_location=self.device, weights_only=False)
```

### 方案2: 降级PyTorch（不推荐）

```bash
pip install torch==2.5.0 torchvision==0.20.0
```

## 🔐 安全性说明

### weights_only=False 安全吗？

**如果模型来自可信来源，是安全的。**

✅ **安全的情况**：
- 您自己训练的模型
- 从Ultralytics官方下载的模型
- 从可信团队成员获得的模型
- 从官方GitHub仓库下载的模型

❌ **不安全的情况**：
- 来自不明来源的模型
- 未经验证的第三方模型
- 通过不安全渠道获得的模型

### 为什么需要weights_only=False？

YOLOv5模型包含完整的模型架构类定义，不仅仅是权重数据。这些类在加载时需要被反序列化，这就是为什么需要`weights_only=False`。

### 替代方案（仅加载权重）

如果您只需要权重，可以这样做：

```python
# 方法1: 使用safe_globals
import torch.serialization
torch.serialization.add_safe_globals([ultralytics.nn.tasks.DetectionModel])
model = torch.load(path, weights_only=True)

# 方法2: 只加载state_dict
checkpoint = torch.load(path, weights_only=False)
model.load_state_dict(checkpoint['model'].state_dict())
```

但这会增加代码复杂度，且对于我们的转换工具来说不必要。

## 📋 完整修复清单

### 需要修改的文件

1. **converter_gui.py** - 第431行
2. **convert_yolov5_to_tensorrt.py** - 第73行（大约）

### 修改位置

#### File 1: converter_gui.py

```python
# 在 convert_to_onnx 方法中，大约第428-431行
def convert_to_onnx(self):
    # ... 前面的代码 ...
    
    # 加载模型
    self.log_info("加载PyTorch模型...")
    # 添加 weights_only=False
    model = torch.load(str(pt_path), map_location=self.device.get(), weights_only=False)
    
    # ... 后面的代码 ...
```

#### File 2: convert_yolov5_to_tensorrt.py

```python
# 在 convert_pt_to_onnx 方法中，大约第70-73行
def convert_pt_to_onnx(self, simplify=True, dynamic=False, opset=12):
    try:
        import warnings
        
        # Load PyTorch model
        print("\nLoading PyTorch model...")
        # 添加 weights_only=False
        model = torch.load(self.pt_model_path, map_location=self.device, weights_only=False)
        
        # ... 后面的代码 ...
```

## 🧪 验证修复

修复后，运行以下命令测试：

```bash
python converter_gui.py
# 或
python convert_yolov5_to_tensorrt.py --weights your_model.pt
```

应该不会再看到 `Weights only load failed` 错误。

## 📊 版本兼容性

| PyTorch版本 | 是否需要修复 | 说明 |
|-------------|-------------|------|
| < 2.6       | ❌ 不需要   | 默认 weights_only=False |
| ≥ 2.6       | ✅ 需要     | 默认 weights_only=True |

修复后的代码兼容所有版本：
- PyTorch 2.6+：显式设置 `weights_only=False`
- PyTorch < 2.6：参数被忽略（已经是默认值）

## 🔄 更新历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2025-10-21 | 初始版本 |
| v1.1 | 2025-10-21 | 修复TracerWarning和NameError |
| v1.2 | 2025-10-21 | 修复PyTorch 2.6兼容性 ⭐ |

## ❓ 常见问题

### Q: 我必须更新吗？
A: **如果您使用PyTorch 2.6+，必须更新**。否则无法加载模型。

### Q: 这个修复安全吗？
A: **如果您的模型来自可信来源，完全安全**。这是加载Ultralytics模型的标准方式。

### Q: 会影响旧版本PyTorch吗？
A: 不会。`weights_only=False`参数在旧版本中会被忽略或使用默认值，完全兼容。

### Q: 除了torch.load，还需要修改其他地方吗？
A: 不需要。只有这两个文件的这两处需要修改。

## 📖 相关文档

- [PyTorch torch.load 文档](https://pytorch.org/docs/stable/generated/torch.load.html)
- [PyTorch 2.6 Release Notes](https://github.com/pytorch/pytorch/releases/tag/v2.6.0)
- [Ultralytics 文档](https://docs.ultralytics.com/)

## 🆘 需要帮助？

1. 查看 `TROUBLESHOOTING.md` - 其他常见问题
2. 查看 `CHANGELOG.md` - 完整更新历史
3. 确保您的PyTorch版本：`python -c "import torch; print(torch.__version__)"`

---

**更新日期**: 2025-10-21  
**版本**: v1.2  
**修复**: PyTorch 2.6+ 兼容性  
**状态**: ✅ 已修复并测试
