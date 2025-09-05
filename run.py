#!/usr/bin/env python3
"""
AI智能助理启动脚本
"""

import subprocess
import sys
import os

def main():
    print("🤖 AI智能助理启动中...")
    
    # 检查虚拟环境
    venv_path = os.path.join(os.getcwd(), "ai_assistant_env")
    if os.path.exists(venv_path):
        python_path = os.path.join(venv_path, "bin", "python3")
        print("✅ 使用虚拟环境")
    else:
        python_path = sys.executable
        print("⚠️ 使用系统Python环境")
    
    # 启动应用
    print("🚀 启动Streamlit应用...")
    print("📝 访问地址: http://localhost:8501")
    print("🔧 Ollama服务器: http://172.27.66.166:11900")
    print("⏹️ 按 Ctrl+C 停止应用")
    print("-" * 50)
    
    try:
        subprocess.run([
            python_path, "-m", "streamlit", "run", "ai_assistant.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ])
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("💡 请确保已安装依赖: source ai_assistant_env/bin/activate && pip install -r requirements.txt")

if __name__ == "__main__":
    main()