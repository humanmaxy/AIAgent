#!/bin/bash
# YOLOv5 转换器 GUI 启动脚本

echo "启动 YOLOv5 模型转换工具..."

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 python3"
    exit 1
fi

# 检查依赖
echo "检查依赖..."
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "错误: 未安装 tkinter"
    echo "请安装: sudo apt-get install python3-tk"
    exit 1
fi

# 启动GUI
python3 converter_gui.py
