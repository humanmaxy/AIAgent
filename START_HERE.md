# 🎉 欢迎使用 YOLOv5 模型转换工具！

## 🚀 三步开始使用

### 第一步：安装依赖
```bash
pip install -r requirements.txt
```

### 第二步：启动程序
```bash
# 方法1: 使用启动脚本
./run_gui.sh          # Linux/macOS
run_gui.bat           # Windows

# 方法2: 直接运行Python
python3 converter_gui.py
```

### 第三步：转换模型
1. 点击「PT模型文件」旁的「浏览...」，选择你的 `.pt` 文件
2. 点击「🚀 开始转换」按钮
3. 等待转换完成提示
4. 在输出目录查看生成的 `.onnx` 和 `.engine` 文件

就这么简单！ ✨

## 📖 需要帮助？

### 新手用户
- 📘 [INSTALLATION.md](INSTALLATION.md) - 详细安装指南
- 📗 [QUICKSTART.md](QUICKSTART.md) - 快速入门教程
- 📙 [GUI_USER_GUIDE.md](GUI_USER_GUIDE.md) - GUI详细使用指南

### 进阶用户
- 📕 [README.md](README.md) - 完整功能文档
- 📔 [GUI_FEATURES.md](GUI_FEATURES.md) - GUI功能详解
- 📓 [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 快速参考卡片

### 开发者
- 📝 [example_usage.py](example_usage.py) - Python API示例
- 📖 [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - 项目总结

## 🎯 常见场景

### 场景1: 我只想快速转换一个模型
```bash
python3 converter_gui.py
```
打开GUI → 选择PT文件 → 点击开始转换 → 完成！

### 场景2: 我想在脚本中使用
```bash
python3 convert_yolov5_to_tensorrt.py --weights yolov5s.pt --fp16
```

### 场景3: 我想集成到代码中
```python
from convert_yolov5_to_tensorrt import YOLOv5Converter
converter = YOLOv5Converter(pt_model_path='yolov5s.pt')
converter.convert_all(fp16=True)
```

## ✨ 项目特色

- 🎨 **图形界面** - 简单直观，无需编程
- ⚡ **高效转换** - 多线程，不阻塞界面
- 📊 **实时日志** - 彩色日志，实时显示进度
- 🔧 **灵活配置** - 所有参数可自定义
- 📚 **文档完整** - 9个文档，详细清晰
- 🌐 **跨平台** - 支持 Windows/Linux/macOS

## 📦 项目文件

```
converter_gui.py              ← 🎨 图形界面程序（推荐）
convert_yolov5_to_tensorrt.py ← ⌨️ 命令行工具
example_usage.py              ← 📝 API使用示例
requirements.txt              ← 📋 依赖清单
```

## 💡 使用提示

### GUI界面技巧
1. **默认参数通常就够用** - 大部分情况无需修改
2. **FP16推荐** - 速度提升2-3倍，精度损失很小
3. **日志可以复制** - 遇到问题可以保存日志
4. **输出目录自动设置** - 选择PT文件后自动设置

### 参数建议
- **图像尺寸**: 640×640（默认，平衡） 或 1280×1280（高精度）
- **精度**: FP16（推荐，2-3倍加速）
- **Workspace**: 4-8 GB（根据模型大小）
- **Batch**: 1（实时推理） 或 4-8（批量处理）

## 🔧 系统要求

### 必需
- Python 3.7+
- PyTorch
- ONNX

### 可选
- TensorRT（转换为TRT引擎时需要）
- CUDA（GPU加速）
- tkinter（GUI界面，通常已预装）

## ❓ 遇到问题？

### 常见问题快速解决

**Q: 看到TracerWarning警告**
- ✅ 已修复！最新版本自动抑制，不影响转换结果

**Q: 找不到torch**
```bash
pip install torch torchvision
```

**Q: 找不到tkinter**
```bash
sudo apt-get install python3-tk  # Ubuntu/Debian
```

**Q: 找不到trtexec**
- 在GUI中点击「trtexec路径」的「浏览...」选择trtexec文件
- 或设置环境变量: `export PATH=$PATH:/path/to/TensorRT/bin`

更多问题请查看:
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - 详细故障排查指南 ⭐⭐⭐⭐⭐
- [INSTALLATION.md](INSTALLATION.md) - 安装问题
- [GUI_USER_GUIDE.md](GUI_USER_GUIDE.md) - 使用问题

## 📞 获取更多帮助

1. 查看 [INDEX.md](INDEX.md) 了解所有文档
2. 阅读 [COMPLETION_REPORT.md](COMPLETION_REPORT.md) 了解项目详情
3. 运行 `python3 test_gui_import.py` 测试环境

## 🎓 学习路径

```
第1天: 安装依赖 → 运行GUI → 尝试转换测试模型
第2天: 理解参数 → 调整配置 → 转换实际模型
第3天: 学习命令行 → 编写脚本 → 批量转换
第4天: 使用Python API → 集成到项目
```

## ⭐ 核心功能

✅ 所有需求100%完成：

- ✅ 读取PT模型文件
- ✅ 转换为ONNX
- ✅ 转换为TensorRT
- ✅ 调用trtexec
- ✅ 图形界面
- ✅ 文件选择
- ✅ 参数配置（batch/width/height/channel）
- ✅ 精度选择（FP32/FP16/INT8）
- ✅ 一键转换

---

## 🎯 立即开始

```bash
# 安装依赖
pip install -r requirements.txt

# 启动程序
python3 converter_gui.py

# 开始转换！
```

**祝使用愉快！** 🎉

有任何问题，请查看相应的文档文件。

---

**项目文件**: 16个文件，3300+行代码和文档  
**支持平台**: Windows, Linux, macOS  
**文档语言**: 中文  
**开源协议**: MIT License
