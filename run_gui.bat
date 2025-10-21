@echo off
REM YOLOv5 转换器 GUI 启动脚本 (Windows)

echo 启动 YOLOv5 模型转换工具...

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Python
    pause
    exit /b 1
)

REM 启动GUI
python converter_gui.py

pause
