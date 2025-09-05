#!/bin/bash

echo "🤖 启动AI智能助理 (内网版)..."
echo "📁 工作目录: $(pwd)"

# 激活虚拟环境
source ai_assistant_env/bin/activate

# 启动内网版应用
echo "🚀 启动Streamlit应用 (内网模式)..."
echo "📝 访问地址: http://localhost:8501"
echo "🔧 Ollama服务器: http://172.27.66.166:11900"
echo "🔒 运行模式: 内网环境 (无需外网连接)"
echo "⏹️ 按 Ctrl+C 停止应用"
echo "$(printf '%.0s-' {1..50})"

streamlit run ai_assistant_offline.py --server.port 8501 --server.address 0.0.0.0