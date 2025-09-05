import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime
import asyncio
import aiohttp
from typing import List, Dict, Any
import urllib.parse

# 配置页面
st.set_page_config(
    page_title="AI智能助理",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

class OllamaClient:
    def __init__(self, base_url: str = "http://172.27.66.166:11900"):
        self.base_url = base_url.rstrip('/')
        
    def chat(self, message: str, model: str = "llama2") -> str:
        """与Ollama模型对话"""
        try:
            url = f"{self.base_url}/api/generate"
            payload = {
                "model": model,
                "prompt": message,
                "stream": False
            }
            
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            return result.get('response', '抱歉，无法获取回复')
            
        except requests.exceptions.RequestException as e:
            return f"连接Ollama服务器失败: {str(e)}"
        except json.JSONDecodeError:
            return "解析响应失败"
        except Exception as e:
            return f"发生错误: {str(e)}"
    
    def get_models(self) -> List[str]:
        """获取可用模型列表"""
        try:
            url = f"{self.base_url}/api/tags"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            models = [model['name'] for model in result.get('models', [])]
            return models if models else ['llama2']
            
        except:
            return ['llama2']  # 默认模型

class WebSearcher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def search_bing(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """使用Bing搜索"""
        try:
            # 首先检查网络连接
            test_response = requests.get("https://www.bing.com", timeout=5)
            
            encoded_query = urllib.parse.quote(query)
            url = f"https://www.bing.com/search?q={encoded_query}"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            results = []
            
            # 查找搜索结果
            search_results = soup.find_all('li', class_='b_algo')[:num_results]
            
            for result in search_results:
                title_elem = result.find('h2')
                link_elem = result.find('a')
                snippet_elem = result.find('p') or result.find('div', class_='b_caption')
                
                if title_elem and link_elem:
                    results.append({
                        'title': title_elem.get_text(strip=True),
                        'url': link_elem.get('href', ''),
                        'snippet': snippet_elem.get_text(strip=True) if snippet_elem else ''
                    })
            
            return results
            
        except requests.exceptions.ConnectionError:
            st.error("🔒 网络连接失败：当前可能处于内网环境，无法访问外部网站")
            st.info("💡 建议使用内网版应用：`streamlit run ai_assistant_offline.py`")
            return []
        except requests.exceptions.Timeout:
            st.error("⏱️ 网络请求超时：网络连接可能不稳定")
            return []
        except Exception as e:
            st.error(f"搜索失败: {str(e)}")
            if "WinError 10013" in str(e) or "访问权限不允许" in str(e):
                st.error("🔒 网络访问权限受限，建议使用内网版应用")
            return []
    
    def get_page_content(self, url: str) -> str:
        """获取网页内容"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 移除脚本和样式标签
            for script in soup(["script", "style"]):
                script.decompose()
            
            # 获取文本内容
            text = soup.get_text()
            
            # 清理文本
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # 限制长度
            return text[:3000] if len(text) > 3000 else text
            
        except Exception as e:
            return f"无法获取网页内容: {str(e)}"

class DataAnalyzer:
    def __init__(self):
        pass
    
    def analyze_search_results(self, results: List[Dict[str, Any]], query: str) -> Dict[str, Any]:
        """分析搜索结果"""
        if not results:
            return {"error": "没有搜索结果可供分析"}
        
        analysis = {
            "total_results": len(results),
            "query": query,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sources": [],
            "key_topics": [],
            "summary": ""
        }
        
        # 提取源信息
        for result in results:
            domain = self.extract_domain(result['url'])
            analysis["sources"].append({
                "title": result['title'],
                "domain": domain,
                "url": result['url'],
                "snippet": result['snippet']
            })
        
        # 分析域名分布
        domains = [self.extract_domain(r['url']) for r in results]
        domain_counts = pd.Series(domains).value_counts().to_dict()
        analysis["domain_distribution"] = domain_counts
        
        # 提取关键词
        all_text = " ".join([r['title'] + " " + r['snippet'] for r in results])
        keywords = self.extract_keywords(all_text)
        analysis["key_topics"] = keywords
        
        return analysis
    
    def extract_domain(self, url: str) -> str:
        """提取域名"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netlify or parsed.hostname or url
        except:
            return url
    
    def extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        """提取关键词"""
        # 简单的关键词提取
        words = re.findall(r'\b[a-zA-Z\u4e00-\u9fa5]{2,}\b', text.lower())
        
        # 过滤停用词
        stop_words = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', 'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        
        filtered_words = [word for word in words if word not in stop_words and len(word) > 1]
        
        # 统计词频
        word_freq = pd.Series(filtered_words).value_counts()
        
        return word_freq.head(top_n).index.tolist()
    
    def create_visualizations(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """创建可视化图表"""
        charts = {}
        
        # 域名分布饼图
        if "domain_distribution" in analysis:
            domains = list(analysis["domain_distribution"].keys())
            counts = list(analysis["domain_distribution"].values())
            
            fig_pie = px.pie(
                values=counts,
                names=domains,
                title="搜索结果来源分布"
            )
            charts["domain_pie"] = fig_pie
        
        # 关键词条形图
        if "key_topics" in analysis:
            keywords = analysis["key_topics"][:8]  # 取前8个
            keyword_counts = list(range(len(keywords), 0, -1))  # 模拟频次
            
            fig_bar = px.bar(
                x=keyword_counts,
                y=keywords,
                orientation='h',
                title="关键主题分析",
                labels={'x': '相关度', 'y': '关键词'}
            )
            charts["keyword_bar"] = fig_bar
        
        return charts

def main():
    st.title("🤖 AI智能助理")
    st.markdown("---")
    
    # 初始化组件
    if 'ollama_client' not in st.session_state:
        st.session_state.ollama_client = OllamaClient()
    
    if 'web_searcher' not in st.session_state:
        st.session_state.web_searcher = WebSearcher()
    
    if 'data_analyzer' not in st.session_state:
        st.session_state.data_analyzer = DataAnalyzer()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # 侧边栏配置
    with st.sidebar:
        st.header("⚙️ 配置")
        
        # 模型选择
        available_models = st.session_state.ollama_client.get_models()
        selected_model = st.selectbox("选择AI模型", available_models)
        
        # 搜索配置
        st.subheader("搜索设置")
        search_results_count = st.slider("搜索结果数量", 3, 10, 5)
        enable_content_fetch = st.checkbox("获取网页详细内容", value=False)
        
        # 清空历史
        if st.button("清空对话历史"):
            st.session_state.chat_history = []
            st.rerun()
    
    # 主界面
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 对话区")
        
        # 显示聊天历史
        chat_container = st.container()
        with chat_container:
            for i, (role, content) in enumerate(st.session_state.chat_history):
                if role == "user":
                    st.markdown(f"**🧑 您:** {content}")
                else:
                    st.markdown(f"**🤖 AI助理:** {content}")
                st.markdown("---")
        
        # 输入框
        user_input = st.text_area("请输入您的问题或需要搜索的内容:", height=100)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔍 搜索并分析", type="primary"):
                if user_input:
                    process_search_query(user_input, selected_model, search_results_count, enable_content_fetch)
        
        with col_btn2:
            if st.button("💬 直接对话"):
                if user_input:
                    process_direct_chat(user_input, selected_model)
    
    with col2:
        st.subheader("📊 分析结果")
        
        # 显示最近的分析结果
        if hasattr(st.session_state, 'latest_analysis'):
            analysis = st.session_state.latest_analysis
            
            st.metric("搜索结果数量", analysis.get("total_results", 0))
            st.metric("分析时间", analysis.get("timestamp", ""))
            
            # 关键主题
            if "key_topics" in analysis:
                st.subheader("🏷️ 关键主题")
                for topic in analysis["key_topics"][:5]:
                    st.tag(topic)
        
        # 显示图表
        if hasattr(st.session_state, 'latest_charts'):
            charts = st.session_state.latest_charts
            
            if "domain_pie" in charts:
                st.plotly_chart(charts["domain_pie"], use_container_width=True)
            
            if "keyword_bar" in charts:
                st.plotly_chart(charts["keyword_bar"], use_container_width=True)

def process_search_query(query: str, model: str, num_results: int, fetch_content: bool):
    """处理搜索查询"""
    with st.spinner("🔍 正在搜索..."):
        # 添加用户输入到历史
        st.session_state.chat_history.append(("user", query))
        
        # 执行搜索
        search_results = st.session_state.web_searcher.search_bing(query, num_results)
        
        if not search_results:
            st.error("搜索失败，请检查网络连接或稍后重试")
            return
        
        # 分析搜索结果
        analysis = st.session_state.data_analyzer.analyze_search_results(search_results, query)
        st.session_state.latest_analysis = analysis
        
        # 创建可视化
        charts = st.session_state.data_analyzer.create_visualizations(analysis)
        st.session_state.latest_charts = charts
        
        # 准备AI分析的内容
        content_for_ai = f"搜索查询: {query}\n\n搜索结果:\n"
        
        for i, result in enumerate(search_results, 1):
            content_for_ai += f"{i}. 标题: {result['title']}\n"
            content_for_ai += f"   链接: {result['url']}\n"
            content_for_ai += f"   摘要: {result['snippet']}\n\n"
            
            # 如果启用了内容获取
            if fetch_content:
                page_content = st.session_state.web_searcher.get_page_content(result['url'])
                content_for_ai += f"   详细内容: {page_content[:500]}...\n\n"
        
        content_for_ai += f"\n关键主题: {', '.join(analysis.get('key_topics', []))}\n"
        content_for_ai += f"请基于以上搜索结果，对'{query}'进行综合分析和总结，并给出有价值的见解。"
    
    with st.spinner("🤖 AI正在分析..."):
        # 获取AI分析
        ai_response = st.session_state.ollama_client.chat(content_for_ai, model)
        st.session_state.chat_history.append(("assistant", ai_response))
        
        st.success("分析完成！")
        st.rerun()

def process_direct_chat(query: str, model: str):
    """处理直接对话"""
    with st.spinner("🤖 AI正在思考..."):
        st.session_state.chat_history.append(("user", query))
        
        ai_response = st.session_state.ollama_client.chat(query, model)
        st.session_state.chat_history.append(("assistant", ai_response))
        
        st.rerun()

if __name__ == "__main__":
    main()