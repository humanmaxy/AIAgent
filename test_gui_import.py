#!/usr/bin/env python3
"""
测试GUI程序导入和基本功能
"""

import sys

def test_imports():
    """测试必要的导入"""
    print("Testing imports...")
    
    errors = []
    
    # 测试tkinter
    try:
        import tkinter
        print("✓ tkinter imported successfully")
    except ImportError as e:
        errors.append(f"✗ tkinter import failed: {e}")
    
    # 测试GUI模块
    try:
        import converter_gui
        print("✓ converter_gui imported successfully")
    except ImportError as e:
        errors.append(f"✗ converter_gui import failed: {e}")
    
    # 测试转换器模块（仅检查文件存在）
    try:
        import os
        if os.path.exists('convert_yolov5_to_tensorrt.py'):
            print("✓ convert_yolov5_to_tensorrt.py exists")
        else:
            errors.append("✗ convert_yolov5_to_tensorrt.py not found")
    except Exception as e:
        errors.append(f"✗ Error checking converter module: {e}")
    
    # 可选依赖（不影响GUI启动）
    optional = []
    
    try:
        import torch
        print("✓ torch available")
    except ImportError:
        optional.append("torch")
    
    try:
        import onnx
        print("✓ onnx available")
    except ImportError:
        optional.append("onnx")
    
    try:
        import onnxsim
        print("✓ onnx-simplifier available")
    except ImportError:
        optional.append("onnx-simplifier")
    
    # 输出结果
    print("\n" + "="*50)
    if errors:
        print("ERRORS:")
        for error in errors:
            print(f"  {error}")
        print("\nGUI cannot start due to missing dependencies.")
        return False
    else:
        print("✓ All required imports successful!")
        print("✓ GUI can be started with: python3 converter_gui.py")
    
    if optional:
        print("\nOptional dependencies not found:")
        for dep in optional:
            print(f"  - {dep}")
        print("\nInstall them with: pip install -r requirements.txt")
    else:
        print("\n✓ All optional dependencies available!")
    
    print("="*50)
    return True


def test_gui_creation():
    """测试GUI创建（不显示）"""
    try:
        from tkinter import Tk
        from converter_gui import ConverterGUI
        
        print("\nTesting GUI creation...")
        root = Tk()
        root.withdraw()  # 隐藏窗口
        
        app = ConverterGUI(root)
        print("✓ GUI object created successfully")
        
        root.destroy()
        return True
    except Exception as e:
        print(f"✗ GUI creation failed: {e}")
        return False


if __name__ == '__main__':
    print("YOLOv5 Converter GUI - Import Test")
    print("="*50 + "\n")
    
    # 测试导入
    imports_ok = test_imports()
    
    if imports_ok:
        # 测试GUI创建
        gui_ok = test_gui_creation()
        
        if gui_ok:
            print("\n✓✓✓ All tests passed! ✓✓✓")
            print("\nYou can now run the GUI with:")
            print("  python3 converter_gui.py")
            sys.exit(0)
    
    print("\n✗✗✗ Some tests failed ✗✗✗")
    print("\nPlease install missing dependencies first:")
    print("  pip install -r requirements.txt")
    sys.exit(1)
