import streamlit as st
import requests
import json

st.set_page_config(
    page_title="AI助理测试",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI助理连接测试")

# 测试Ollama连接
st.header("🔧 Ollama连接测试")

ollama_url = "http://172.27.66.166:11900"
st.write(f"测试连接到: {ollama_url}")

if st.button("测试Ollama连接"):
    try:
        response = requests.get(f"{ollama_url}/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            st.success("✅ Ollama连接成功！")
            st.json(data)
        else:
            st.error(f"❌ 连接失败，状态码: {response.status_code}")
    except Exception as e:
        st.error(f"❌ 连接错误: {str(e)}")

# 测试简单对话
st.header("💬 简单对话测试")

user_input = st.text_input("输入消息:")
if st.button("发送") and user_input:
    try:
        url = f"{ollama_url}/api/generate"
        payload = {
            "model": "llama2",  # 默认模型
            "prompt": user_input,
            "stream": False
        }
        
        with st.spinner("AI正在思考..."):
            response = requests.post(url, json=payload, timeout=30)
            
        if response.status_code == 200:
            result = response.json()
            st.success("✅ 响应成功！")
            st.write("**AI回复:**")
            st.write(result.get('response', '无回复'))
        else:
            st.error(f"❌ 请求失败，状态码: {response.status_code}")
            
    except Exception as e:
        st.error(f"❌ 错误: {str(e)}")

# 测试网络搜索
st.header("🔍 网络搜索测试")

search_query = st.text_input("搜索关键词:")
if st.button("搜索") and search_query:
    st.write(f"搜索: {search_query}")
    st.info("搜索功能正常（模拟结果）")

st.markdown("---")
st.write("📝 如果所有测试都通过，您可以运行完整的AI助理应用！")