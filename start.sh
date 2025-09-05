#!/bin/bash

echo "🤖 启动AI智能助理..."
echo "📁 工作目录: $(pwd)"

# 激活虚拟环境
source ai_assistant_env/bin/activate

# 启动应用
echo "🚀 启动Streamlit应用..."
echo "📝 访问地址: http://localhost:8501"
echo "🔧 Ollama服务器: http://172.27.66.166:11900"
echo "⏹️ 按 Ctrl+C 停止应用"
echo "$(printf '%.0s-' {1..50})"

streamlit run ai_assistant.py --server.port 8501 --server.address 0.0.0.0