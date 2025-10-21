# 项目文件索引

## 📖 快速导航

### 🚀 快速开始
1. **首次使用**: 阅读 [INSTALLATION.md](INSTALLATION.md) 安装依赖
2. **快速上手**: 阅读 [QUICKSTART.md](QUICKSTART.md) 
3. **启动GUI**: 运行 `run_gui.sh` (Linux/macOS) 或 `run_gui.bat` (Windows)

### 📱 程序文件

| 文件 | 类型 | 说明 | 推荐度 |
|------|------|------|--------|
| **converter_gui.py** | GUI程序 | 图形界面版本，简单易用 | ⭐⭐⭐⭐⭐ |
| **convert_yolov5_to_tensorrt.py** | 命令行工具 | 命令行版本，适合脚本 | ⭐⭐⭐⭐ |
| **example_usage.py** | 示例代码 | Python API使用示例 | ⭐⭐⭐ |
| test_gui_import.py | 测试脚本 | 测试依赖是否安装 | ⭐⭐ |

### 📋 启动脚本

| 文件 | 平台 | 说明 |
|------|------|------|
| **run_gui.sh** | Linux/macOS | GUI启动脚本（执行 chmod +x 后使用） |
| **run_gui.bat** | Windows | GUI启动脚本（双击运行） |

### 📚 文档文件

#### 入门文档（必读）
| 文件 | 内容 | 适合人群 |
|------|------|----------|
| **README.md** | 项目主文档，功能介绍 | 所有用户 ⭐⭐⭐⭐⭐ |
| **INSTALLATION.md** | 详细安装指南 | 首次安装 ⭐⭐⭐⭐⭐ |
| **QUICKSTART.md** | 快速入门教程 | 新手用户 ⭐⭐⭐⭐⭐ |

#### GUI文档（GUI用户必读）
| 文件 | 内容 | 适合人群 |
|------|------|----------|
| **GUI_USER_GUIDE.md** | GUI详细使用指南 | GUI用户 ⭐⭐⭐⭐⭐ |
| **GUI_FEATURES.md** | GUI界面功能详解 | GUI高级用户 ⭐⭐⭐⭐ |

#### 参考文档
| 文件 | 内容 | 适合人群 |
|------|------|----------|
| **TROUBLESHOOTING.md** | 故障排查指南 | 遇到问题时 ⭐⭐⭐⭐⭐ |
| **PROJECT_SUMMARY.md** | 项目总结，功能清单 | 开发者/管理者 ⭐⭐⭐ |
| **CHANGELOG.md** | 更新日志 | 了解版本变化 ⭐⭐⭐ |
| **INDEX.md** | 本文件，文件索引 | 所有用户 ⭐⭐⭐ |

### 📦 配置文件

| 文件 | 说明 |
|------|------|
| **requirements.txt** | Python依赖包列表 |

## 📖 推荐阅读顺序

### 新手用户（使用GUI）
```
1. INSTALLATION.md     (安装依赖)
   ↓
2. QUICKSTART.md       (快速了解)
   ↓
3. GUI_USER_GUIDE.md   (详细使用)
   ↓
4. 开始使用 converter_gui.py
```

### 命令行用户
```
1. INSTALLATION.md     (安装依赖)
   ↓
2. QUICKSTART.md       (快速了解)
   ↓
3. README.md           (详细参数)
   ↓
4. 使用 convert_yolov5_to_tensorrt.py
```

### Python开发者
```
1. INSTALLATION.md     (安装依赖)
   ↓
2. README.md           (API说明)
   ↓
3. example_usage.py    (代码示例)
   ↓
4. 集成到自己的代码
```

## 🎯 根据场景选择文件

### 场景1: 我想转换一个YOLOv5模型
```bash
# 最简单：使用GUI
./run_gui.sh
# 或
python3 converter_gui.py
```
📖 参考文档: `GUI_USER_GUIDE.md`

### 场景2: 我想在脚本中批量转换
```bash
# 使用命令行工具
python3 convert_yolov5_to_tensorrt.py --weights model.pt --fp16
```
📖 参考文档: `README.md`, `QUICKSTART.md`

### 场景3: 我想集成到Python项目
```python
from convert_yolov5_to_tensorrt import YOLOv5Converter
converter = YOLOv5Converter(pt_model_path='model.pt')
converter.convert_all()
```
📖 参考文档: `example_usage.py`, `README.md`

### 场景4: 我遇到了问题
1. 查看 `TROUBLESHOOTING.md` - 故障排查指南 ⭐⭐⭐⭐⭐
2. 查看 `INSTALLATION.md` - 安装相关问题
3. 查看 `GUI_USER_GUIDE.md` - GUI使用问题
4. 查看 `README.md` - 详细说明

### 场景5: 我想了解所有功能
1. 查看 `PROJECT_SUMMARY.md` - 功能清单
2. 查看 `GUI_FEATURES.md` - GUI详细功能
3. 查看 `README.md` - 完整文档

## 📂 文件大小参考

```
converter_gui.py              ~23 KB  (GUI主程序)
convert_yolov5_to_tensorrt.py ~13 KB  (命令行工具)
example_usage.py              ~3 KB   (示例代码)
test_gui_import.py            ~3 KB   (测试脚本)

GUI_FEATURES.md               ~12 KB  (GUI功能详解)
GUI_USER_GUIDE.md             ~7 KB   (GUI使用指南)
README.md                     ~6 KB   (主文档)
INSTALLATION.md               ~5 KB   (安装指南)
QUICKSTART.md                 ~4 KB   (快速入门)
PROJECT_SUMMARY.md            ~8 KB   (项目总结)
INDEX.md                      ~4 KB   (本文件)

requirements.txt              ~445 B  (依赖列表)
run_gui.sh                    ~446 B  (启动脚本)
run_gui.bat                   ~269 B  (启动脚本)
```

## 🔧 核心功能对照表

| 功能 | GUI | 命令行 | Python API |
|------|-----|--------|------------|
| PT → ONNX | ✅ | ✅ | ✅ |
| ONNX → TensorRT | ✅ | ✅ | ✅ |
| 参数配置 | ✅ 可视化 | ✅ 命令行参数 | ✅ 函数参数 |
| 实时日志 | ✅ 彩色界面 | ✅ 终端输出 | ✅ Python输出 |
| 进度显示 | ✅ 进度条 | ✅ 文本输出 | ✅ 回调函数 |
| 易用性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| 灵活性 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 适合场景 | 新手/一次性 | 脚本/批量 | 集成/自动化 |

## 📝 文件关系图

```
用户
  │
  ├─→ 图形界面用户
  │    ├─→ run_gui.sh / run_gui.bat
  │    │    └─→ converter_gui.py
  │    └─→ 阅读: GUI_USER_GUIDE.md, GUI_FEATURES.md
  │
  ├─→ 命令行用户
  │    ├─→ convert_yolov5_to_tensorrt.py
  │    └─→ 阅读: README.md, QUICKSTART.md
  │
  └─→ Python开发者
       ├─→ import convert_yolov5_to_tensorrt
       ├─→ 参考: example_usage.py
       └─→ 阅读: README.md

所有用户先阅读: INSTALLATION.md (安装)
遇到问题查看: INSTALLATION.md, GUI_USER_GUIDE.md (故障排查)
```

## 🎓 学习路径

### 初级（只想转换模型）
- [ ] 阅读 INSTALLATION.md 前半部分
- [ ] 运行 pip install -r requirements.txt
- [ ] 启动 converter_gui.py
- [ ] 浏览 GUI_USER_GUIDE.md 的"使用步骤"部分
- [ ] 完成第一次转换

### 中级（理解参数意义）
- [ ] 完整阅读 GUI_USER_GUIDE.md
- [ ] 了解 GUI_FEATURES.md 中的参数说明
- [ ] 尝试不同参数配置
- [ ] 了解 FP16/INT8 的区别
- [ ] 学习动态输入的用法

### 高级（命令行和脚本）
- [ ] 阅读 README.md 完整文档
- [ ] 学习 QUICKSTART.md 中的命令行用法
- [ ] 尝试 convert_yolov5_to_tensorrt.py
- [ ] 编写批处理脚本
- [ ] 集成到 CI/CD

### 专家（Python API集成）
- [ ] 研究 example_usage.py
- [ ] 阅读 convert_yolov5_to_tensorrt.py 源码
- [ ] 理解 YOLOv5Converter 类
- [ ] 自定义转换流程
- [ ] 贡献代码改进

## 💡 快速查找

### 我想知道...

#### 如何安装？
→ `INSTALLATION.md`

#### 如何快速开始？
→ `QUICKSTART.md`

#### GUI怎么用？
→ `GUI_USER_GUIDE.md`

#### 各个参数什么意思？
→ `GUI_FEATURES.md`

#### 命令行参数有哪些？
→ `README.md` 或运行 `--help`

#### Python API怎么调用？
→ `example_usage.py`

#### 有哪些功能？
→ `PROJECT_SUMMARY.md`

#### 遇到错误怎么办？
→ `GUI_USER_GUIDE.md` (常见问题) 或 `INSTALLATION.md` (故障排查)

#### 性能如何优化？
→ `README.md` (性能建议) 或 `QUICKSTART.md` (精度对比)

#### 支持哪些模型？
→ `README.md` 或 `PROJECT_SUMMARY.md`

## 🔗 快速链接

### 立即开始
```bash
# 1. 安装
pip install -r requirements.txt

# 2. 启动GUI
python3 converter_gui.py

# 或使用命令行
python3 convert_yolov5_to_tensorrt.py --help
```

### 文档速查
- 新手入门: `INSTALLATION.md` → `QUICKSTART.md` → `GUI_USER_GUIDE.md`
- 命令行: `QUICKSTART.md` → `README.md`
- API集成: `example_usage.py` → `README.md`
- 故障排查: `INSTALLATION.md` → `GUI_USER_GUIDE.md`

## 📞 获取帮助

1. **查看文档**: 按照上述索引查找相关文档
2. **运行测试**: `python3 test_gui_import.py`
3. **查看帮助**: `python3 convert_yolov5_to_tensorrt.py --help`
4. **查看示例**: `example_usage.py`
5. **查看日志**: GUI中的转换日志

---

**提示**: 建议先阅读 `INSTALLATION.md` 完成安装，然后根据使用方式选择相应文档。

**最后更新**: 2025-10-21
