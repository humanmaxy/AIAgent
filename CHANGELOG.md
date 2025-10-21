# 更新日志

## [1.1] - 2025-10-21

### 🐛 Bug修复

#### 1. 修复GUI错误处理的作用域问题
- **问题**: `NameError: cannot access free variable 'e'`
- **原因**: lambda函数捕获变量作用域问题
- **修复**: 使用默认参数传递错误信息
- **文件**: `converter_gui.py` 第401-405行

```python
# 修复前
self.root.after(0, lambda: messagebox.showerror("错误", f"转换失败:\n{str(e)}"))

# 修复后
error_msg = str(e)
self.root.after(0, lambda msg=error_msg: messagebox.showerror("错误", f"转换失败:\n{msg}"))
```

#### 2. 修复Ultralytics模型TracerWarning警告
- **问题**: 
  - `TracerWarning: Converting a tensor to a Python boolean`
  - `TracerWarning: Iterating over a tensor might cause the trace`
- **原因**: Ultralytics YOLOv5模型包含动态判断逻辑
- **修复**: 
  - 自动检测Ultralytics模型
  - 使用warnings过滤器抑制TracerWarning
- **文件**: `converter_gui.py` 和 `convert_yolov5_to_tensorrt.py`

```python
# 添加了警告抑制
import warnings

with warnings.catch_warnings():
    warnings.filterwarnings('ignore', category=torch.jit.TracerWarning)
    warnings.filterwarnings('ignore', message='.*TracerWarning.*')
    torch.onnx.export(...)
```

### ✨ 新增功能

#### 1. Ultralytics模型自动检测
- 自动识别Ultralytics YOLOv5模型
- 显示模型类型信息
- 针对性优化转换流程

```python
# 检测逻辑
model_type = type(model).__name__
if 'DetectionModel' in model_type or hasattr(model, 'yaml'):
    is_ultralytics = True
    print(f"检测到Ultralytics模型: {model_type}")
```

#### 2. 新增故障排查文档
- 创建 `TROUBLESHOOTING.md`
- 包含常见问题和解决方案
- 详细的调试技巧

### 📚 文档更新

#### 新增文档
- `TROUBLESHOOTING.md` - 故障排查指南
- `CHANGELOG.md` - 更新日志（本文件）

#### 更新文档
- `START_HERE.md` - 更新快速开始指南
- `INDEX.md` - 添加新文档索引

### 🔧 改进

1. **错误处理改进**
   - 更好的异常捕获
   - 更详细的错误信息
   - 用户友好的错误提示

2. **警告处理优化**
   - 自动过滤不必要的警告
   - 保留重要的错误信息
   - 更清晰的日志输出

3. **模型兼容性提升**
   - 更好地支持Ultralytics模型
   - 自动检测模型类型
   - 针对性优化

### 🧪 测试

- ✅ GUI错误处理测试
- ✅ Ultralytics模型转换测试
- ✅ TracerWarning抑制测试
- ✅ 跨平台兼容性测试

### 📦 文件变更

```
修改的文件:
  M converter_gui.py              - Bug修复 + Ultralytics支持
  M convert_yolov5_to_tensorrt.py - Ultralytics支持
  
新增的文件:
  A TROUBLESHOOTING.md            - 故障排查指南
  A CHANGELOG.md                  - 更新日志
```

---

## [1.0] - 2025-10-21

### 🎉 首次发布

#### 核心功能
- ✅ PT → ONNX → TensorRT 完整转换流程
- ✅ 图形界面程序
- ✅ 命令行工具
- ✅ Python API

#### 主要特性
- 📁 文件选择对话框
- ⚙️ 完整参数配置
- 🎨 实时彩色日志
- 📊 进度条显示
- 🚀 一键转换
- 🔧 多精度支持（FP32/FP16/INT8）

#### 文档
- README.md - 主文档
- INSTALLATION.md - 安装指南
- QUICKSTART.md - 快速入门
- GUI_USER_GUIDE.md - GUI使用指南
- GUI_FEATURES.md - GUI功能详解
- PROJECT_SUMMARY.md - 项目总结
- INDEX.md - 文件索引
- QUICK_REFERENCE.md - 快速参考
- START_HERE.md - 新手入门

#### 工具文件
- converter_gui.py - GUI程序
- convert_yolov5_to_tensorrt.py - 命令行工具
- example_usage.py - API示例
- test_gui_import.py - 测试脚本
- run_gui.sh - Linux/macOS启动脚本
- run_gui.bat - Windows启动脚本
- requirements.txt - 依赖清单

---

## 版本说明

### 版本号格式
- 主版本号.次版本号
- 例如: 1.0, 1.1, 2.0

### 版本类型
- **主版本** (X.0): 重大功能更新或架构变更
- **次版本** (X.Y): Bug修复、功能改进、文档更新

### 更新频率
- Bug修复: 及时发布
- 功能更新: 根据需求
- 文档更新: 持续更新

---

## 升级指南

### 从 1.0 升级到 1.1

#### 方法1: 下载新版本
1. 备份当前版本（可选）
2. 下载新版本文件
3. 替换以下文件：
   - `converter_gui.py`
   - `convert_yolov5_to_tensorrt.py`
4. 添加新文件：
   - `TROUBLESHOOTING.md`
   - `CHANGELOG.md`

#### 方法2: 手动修改

**修改 converter_gui.py:**
```python
# 找到第401-405行，修改为：
except Exception as e:
    error_msg = str(e)
    self.log_error(f"转换失败: {error_msg}")
    import traceback
    self.log_error(traceback.format_exc())
    self.root.after(0, lambda msg=error_msg: messagebox.showerror("错误", f"转换失败:\n{msg}"))
```

**修改 convert_to_onnx 方法:**
添加warnings过滤和Ultralytics检测（参考新版本代码）

#### 兼容性
- ✅ 向后兼容
- ✅ 无需更改配置
- ✅ 无需重新安装依赖

---

## 已知问题

### 当前版本 (1.1)
- 无已知严重问题

### 计划修复
- [ ] 支持批量转换多个模型
- [ ] 添加转换历史记录
- [ ] 支持配置文件保存/加载

---

## 贡献者

感谢所有为项目做出贡献的人！

### 问题报告
如果发现新的bug或有功能建议，欢迎：
1. 查看 `TROUBLESHOOTING.md` 确认是否为已知问题
2. 提供详细的错误信息和复现步骤
3. 说明您的环境（OS、Python版本等）

---

## 许可证

MIT License

---

**最新版本**: 1.1  
**发布日期**: 2025-10-21  
**维护状态**: 积极维护中
