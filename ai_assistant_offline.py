import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
import time
from datetime import datetime
from typing import List, Dict, Any
import os

# 配置页面
st.set_page_config(
    page_title="AI智能助理 (内网版)",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 添加自定义CSS来解决滚动问题
st.markdown("""
<style>
    /* 修复主容器滚动问题 */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: none;
    }
    
    /* 确保聊天区域可以滚动 */
    .chat-container {
        height: 400px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #e0e0e0;
        border-radius: 0.5rem;
        background-color: #fafafa;
        margin-bottom: 1rem;
    }
    
    /* 分析结果区域样式 */
    .analysis-container {
        height: 500px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #e0e0e0;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
    }
    
    /* 侧边栏滚动 */
    .css-1d391kg {
        overflow-y: auto;
    }
    
    /* 确保页面可以完全滚动 */
    html, body, [data-testid="stAppViewContainer"] {
        height: 100vh;
        overflow-y: auto;
    }
    
    /* 输入区域样式 */
    .input-container {
        position: sticky;
        bottom: 0;
        background-color: white;
        padding: 1rem 0;
        border-top: 1px solid #e0e0e0;
        z-index: 100;
    }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

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

class LocalKnowledgeBase:
    """本地知识库，用于内网环境下的信息查询"""
    
    def __init__(self):
        self.knowledge_base = {
            "经济危机": {
                "1929年大萧条": {
                    "持续时间": "1929-1939年，约10年",
                    "影响": "全球性经济衰退，失业率高达25%",
                    "原因": "股市崩盘、银行破产、消费不足"
                },
                "2008年金融危机": {
                    "持续时间": "2007-2009年，约2年",
                    "影响": "全球金融体系震荡，房地产泡沫破裂",
                    "原因": "次贷危机、金融衍生品风险"
                },
                "1973年石油危机": {
                    "持续时间": "1973-1974年，约1年",
                    "影响": "石油价格暴涨，通胀严重",
                    "原因": "中东战争导致石油禁运"
                },
                "1997年亚洲金融危机": {
                    "持续时间": "1997-1999年，约2年",
                    "影响": "亚洲多国货币大幅贬值",
                    "原因": "资本外逃、汇率制度问题"
                }
            },
            "人工智能": {
                "发展历程": {
                    "1950年代": "图灵测试提出，AI概念诞生",
                    "1980年代": "专家系统兴起",
                    "2000年代": "机器学习快速发展",
                    "2010年代": "深度学习突破，大数据应用",
                    "2020年代": "大语言模型、ChatGPT等突破"
                },
                "主要技术": {
                    "机器学习": "让机器从数据中学习规律",
                    "深度学习": "模拟人脑神经网络结构",
                    "自然语言处理": "让机器理解和生成人类语言",
                    "计算机视觉": "让机器识别和理解图像"
                }
            },
            "编程技术": {
                "Python": {
                    "特点": "简洁易读、库丰富、应用广泛",
                    "应用领域": "数据科学、Web开发、人工智能",
                    "优势": "开发效率高、社区活跃"
                },
                "JavaScript": {
                    "特点": "动态类型、事件驱动、跨平台",
                    "应用领域": "前端开发、后端开发、移动应用",
                    "优势": "生态系统丰富、学习曲线平缓"
                }
            }
        }
    
    def search_local_knowledge(self, query: str) -> List[Dict[str, Any]]:
        """在本地知识库中搜索"""
        results = []
        query_lower = query.lower()
        
        for category, topics in self.knowledge_base.items():
            if any(keyword in query_lower for keyword in [category.lower(), *[topic.lower() for topic in topics.keys()]]):
                for topic, content in topics.items():
                    if isinstance(content, dict):
                        for key, value in content.items():
                            results.append({
                                'title': f"{category} - {topic} - {key}",
                                'url': f"本地知识库/{category}/{topic}",
                                'snippet': f"{key}: {value}",
                                'category': category,
                                'topic': topic
                            })
                    else:
                        results.append({
                            'title': f"{category} - {topic}",
                            'url': f"本地知识库/{category}",
                            'snippet': str(content),
                            'category': category,
                            'topic': topic
                        })
        
        # 如果没有找到匹配的内容，返回通用建议
        if not results:
            results.append({
                'title': "本地知识库搜索",
                'url': "本地知识库",
                'snippet': f"未找到关于'{query}'的具体信息。建议您直接与AI对话获取相关知识。",
                'category': "通用",
                'topic': "搜索建议"
            })
        
        return results[:5]  # 返回前5个结果

class DataAnalyzer:
    def __init__(self):
        pass
    
    def analyze_local_results(self, results: List[Dict[str, Any]], query: str) -> Dict[str, Any]:
        """分析本地搜索结果"""
        if not results:
            return {"error": "没有搜索结果可供分析"}
        
        analysis = {
            "total_results": len(results),
            "query": query,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sources": [],
            "categories": [],
            "topics": [],
            "summary": ""
        }
        
        # 提取信息
        categories = []
        topics = []
        
        for result in results:
            analysis["sources"].append({
                "title": result['title'],
                "source": result['url'],
                "snippet": result['snippet']
            })
            
            if 'category' in result:
                categories.append(result['category'])
            if 'topic' in result:
                topics.append(result['topic'])
        
        # 统计分类和主题
        if categories:
            category_counts = pd.Series(categories).value_counts().to_dict()
            analysis["category_distribution"] = category_counts
            analysis["categories"] = list(set(categories))
        
        if topics:
            analysis["topics"] = list(set(topics))
        
        return analysis
    
    def create_local_visualizations(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """创建本地数据的可视化图表"""
        charts = {}
        
        # 分类分布饼图
        if "category_distribution" in analysis:
            categories = list(analysis["category_distribution"].keys())
            counts = list(analysis["category_distribution"].values())
            
            fig_pie = px.pie(
                values=counts,
                names=categories,
                title="本地知识库搜索结果分类分布"
            )
            charts["category_pie"] = fig_pie
        
        # 主题条形图
        if "topics" in analysis and len(analysis["topics"]) > 1:
            topics = analysis["topics"][:8]  # 取前8个
            topic_counts = list(range(len(topics), 0, -1))  # 模拟相关度
            
            fig_bar = px.bar(
                x=topic_counts,
                y=topics,
                orientation='h',
                title="相关主题分析",
                labels={'x': '相关度', 'y': '主题'}
            )
            charts["topic_bar"] = fig_bar
        
        return charts

def main():
    st.title("🤖 AI智能助理 (内网版)")
    st.markdown("---")
    
    # 显示内网模式提示
    st.info("🔒 当前运行在内网模式下，使用本地知识库进行信息查询")
    
    # 初始化组件
    if 'ollama_client' not in st.session_state:
        st.session_state.ollama_client = OllamaClient()
    
    if 'knowledge_base' not in st.session_state:
        st.session_state.knowledge_base = LocalKnowledgeBase()
    
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
        
        # 内网模式说明
        st.subheader("🔒 内网模式")
        st.write("✅ 本地AI对话")
        st.write("✅ 本地知识库搜索")
        st.write("❌ 外网搜索 (不可用)")
        
        # 本地知识库信息
        st.subheader("📚 本地知识库")
        st.write("• 经济危机历史")
        st.write("• 人工智能发展")
        st.write("• 编程技术知识")
        st.write("• 更多内容...")
        
        # 清空历史
        if st.button("清空对话历史"):
            st.session_state.chat_history = []
            st.rerun()
    
    # 主界面
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 对话区")
        
        # 显示聊天历史 - 使用可滚动容器
        if st.session_state.chat_history:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            chat_html = ""
            for i, (role, content) in enumerate(st.session_state.chat_history):
                if role == "user":
                    chat_html += f"""
                    <div style="margin-bottom: 1rem; padding: 0.5rem; background-color: #e3f2fd; border-radius: 0.5rem;">
                        <strong>🧑 您:</strong> {content}
                    </div>
                    """
                else:
                    chat_html += f"""
                    <div style="margin-bottom: 1rem; padding: 0.5rem; background-color: #f3e5f5; border-radius: 0.5rem;">
                        <strong>🤖 AI助理:</strong> {content}
                    </div>
                    """
            st.markdown(chat_html, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("💡 开始对话吧！您可以询问任何问题或搜索本地知识库。")
        
        # 输入区域 - 固定在底部
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        user_input = st.text_area("请输入您的问题或需要查询的内容:", height=80, key="user_input")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            search_btn = st.button("🔍 本地搜索分析", type="primary", use_container_width=True)
        
        with col_btn2:
            chat_btn = st.button("💬 直接对话", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 处理按钮点击
        if search_btn and user_input:
            process_local_search(user_input, selected_model)
        elif chat_btn and user_input:
            process_direct_chat(user_input, selected_model)
    
    with col2:
        st.subheader("📊 分析结果")
        
        # 使用可滚动的分析结果容器
        st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
        
        # 显示最近的分析结果
        if hasattr(st.session_state, 'latest_analysis'):
            analysis = st.session_state.latest_analysis
            
            # 基本统计信息
            col_metric1, col_metric2 = st.columns(2)
            with col_metric1:
                st.metric("搜索结果", analysis.get("total_results", 0))
            with col_metric2:
                timestamp = analysis.get("timestamp", "")
                if timestamp:
                    time_only = timestamp.split(" ")[1] if " " in timestamp else timestamp
                    st.metric("分析时间", time_only)
            
            # 相关主题
            if "topics" in analysis and analysis["topics"]:
                st.markdown("### 🏷️ 相关主题")
                topics_html = ""
                for topic in analysis["topics"][:5]:
                    topics_html += f'<span style="display: inline-block; background-color: #e1f5fe; padding: 0.25rem 0.5rem; margin: 0.25rem; border-radius: 1rem; font-size: 0.8rem;">• {topic}</span>'
                st.markdown(topics_html, unsafe_allow_html=True)
            
            # 知识分类
            if "categories" in analysis and analysis["categories"]:
                st.markdown("### 📂 知识分类")
                categories_html = ""
                for category in analysis["categories"]:
                    categories_html += f'<span style="display: inline-block; background-color: #f3e5f5; padding: 0.25rem 0.5rem; margin: 0.25rem; border-radius: 1rem; font-size: 0.8rem;">📁 {category}</span>'
                st.markdown(categories_html, unsafe_allow_html=True)
            
            # 搜索结果详情
            if "sources" in analysis and analysis["sources"]:
                st.markdown("### 📝 搜索结果")
                for i, source in enumerate(analysis["sources"][:3], 1):
                    with st.expander(f"结果 {i}: {source['title'][:50]}..."):
                        st.write(f"**来源:** {source['source']}")
                        st.write(f"**内容:** {source['snippet']}")
        else:
            st.info("🔍 执行搜索后，这里将显示详细的分析结果")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 图表区域 - 在滚动容器外单独显示
        if hasattr(st.session_state, 'latest_charts'):
            charts = st.session_state.latest_charts
            
            if "category_pie" in charts:
                st.plotly_chart(charts["category_pie"], use_container_width=True, height=300)
            
            if "topic_bar" in charts:
                st.plotly_chart(charts["topic_bar"], use_container_width=True, height=300)

def process_local_search(query: str, model: str):
    """处理本地搜索查询"""
    with st.spinner("🔍 正在本地知识库中搜索..."):
        # 添加用户输入到历史
        st.session_state.chat_history.append(("user", query))
        
        # 执行本地搜索
        search_results = st.session_state.knowledge_base.search_local_knowledge(query)
        
        # 分析搜索结果
        analysis = st.session_state.data_analyzer.analyze_local_results(search_results, query)
        st.session_state.latest_analysis = analysis
        
        # 创建可视化
        charts = st.session_state.data_analyzer.create_local_visualizations(analysis)
        st.session_state.latest_charts = charts
        
        # 准备AI分析的内容
        content_for_ai = f"用户查询: {query}\n\n本地知识库搜索结果:\n"
        
        for i, result in enumerate(search_results, 1):
            content_for_ai += f"{i}. 标题: {result['title']}\n"
            content_for_ai += f"   来源: {result['url']}\n"
            content_for_ai += f"   内容: {result['snippet']}\n\n"
        
        if analysis.get('categories'):
            content_for_ai += f"\n相关分类: {', '.join(analysis['categories'])}\n"
        if analysis.get('topics'):
            content_for_ai += f"相关主题: {', '.join(analysis['topics'])}\n"
        
        content_for_ai += f"\n请基于以上本地知识库的搜索结果，对'{query}'进行综合分析和总结。如果信息不够完整，请结合您的知识进行补充说明。"
    
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

# 添加使用提示
def show_usage_tips():
    with st.expander("💡 使用提示"):
        st.markdown("""
        **内网模式下的功能：**
        - 🤖 **AI对话**: 与本地Ollama模型直接对话
        - 🔍 **本地搜索**: 在内置知识库中搜索信息
        - 📊 **数据分析**: 分析本地搜索结果并生成图表
        
        **推荐查询示例：**
        - "分析一下历史上的经济危机持续时间"
        - "人工智能发展历程"
        - "Python编程语言的特点"
        - "机器学习和深度学习的区别"
        
        **注意事项：**
        - 本地知识库内容有限，如需更多信息请直接与AI对话
        - AI会结合本地搜索结果和自身知识进行回答
        """)

if __name__ == "__main__":
    show_usage_tips()
    main()