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
    page_title="AI智能助理 (改进版)",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 添加自定义CSS来完全解决滚动问题
st.markdown("""
<style>
    /* 重置页面样式，确保正常滚动 */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 3rem;
        max-width: none;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    /* 聊天历史区域 */
    .chat-history {
        height: 350px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #ddd;
        border-radius: 8px;
        background-color: #fafafa;
        margin-bottom: 1rem;
        scrollbar-width: thin;
        scrollbar-color: #888 #f1f1f1;
    }
    
    .chat-history::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-history::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 3px;
    }
    
    .chat-history::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 3px;
    }
    
    .chat-history::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    
    /* 用户消息样式 */
    .user-message {
        background-color: #e3f2fd;
        padding: 0.75rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        border-left: 3px solid #2196f3;
    }
    
    /* AI消息样式 */
    .ai-message {
        background-color: #f3e5f5;
        padding: 0.75rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        border-left: 3px solid #9c27b0;
    }
    
    /* 分析结果区域 */
    .analysis-panel {
        height: 400px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #ddd;
        border-radius: 8px;
        background-color: #f8f9fa;
        scrollbar-width: thin;
        scrollbar-color: #888 #f1f1f1;
    }
    
    .analysis-panel::-webkit-scrollbar {
        width: 6px;
    }
    
    .analysis-panel::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 3px;
    }
    
    .analysis-panel::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 3px;
    }
    
    /* 标签样式 */
    .topic-tag {
        display: inline-block;
        background-color: #e1f5fe;
        padding: 0.25rem 0.5rem;
        margin: 0.25rem;
        border-radius: 12px;
        font-size: 0.8rem;
        border: 1px solid #b3e5fc;
    }
    
    .category-tag {
        display: inline-block;
        background-color: #fce4ec;
        padding: 0.25rem 0.5rem;
        margin: 0.25rem;
        border-radius: 12px;
        font-size: 0.8rem;
        border: 1px solid #f8bbd9;
    }
    
    /* 输入区域 */
    .input-section {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #ddd;
        margin-top: 1rem;
    }
    
    /* 按钮样式改进 */
    .stButton > button {
        width: 100%;
        border-radius: 6px;
        font-weight: 500;
    }
    
    /* 侧边栏样式 */
    .css-1d391kg {
        padding-top: 1rem;
    }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }
        
        .chat-history {
            height: 250px;
        }
        
        .analysis-panel {
            height: 300px;
        }
    }
    
    /* 确保页面可以正常滚动 */
    [data-testid="stAppViewContainer"] {
        overflow-y: auto !important;
    }
    
    /* 修复Streamlit默认的高度限制 */
    .element-container {
        overflow: visible !important;
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
                    "影响": "全球性经济衰退，失业率高达25%，工业生产下降50%",
                    "原因": "股市崩盘、银行破产、消费不足、国际贸易萎缩",
                    "恢复措施": "罗斯福新政、公共工程、银行改革"
                },
                "2008年金融危机": {
                    "持续时间": "2007-2009年，约2年",
                    "影响": "全球金融体系震荡，房地产泡沫破裂，多国经济衰退",
                    "原因": "次贷危机、金融衍生品风险、监管不足",
                    "恢复措施": "量化宽松、银行救助、财政刺激"
                },
                "1973年石油危机": {
                    "持续时间": "1973-1974年，约1年",
                    "影响": "石油价格暴涨4倍，通胀严重，经济滞涨",
                    "原因": "中东战争导致石油禁运、地缘政治紧张",
                    "恢复措施": "能源多样化、节能政策、替代能源开发"
                },
                "1997年亚洲金融危机": {
                    "持续时间": "1997-1999年，约2年",
                    "影响": "亚洲多国货币大幅贬值，经济增长停滞",
                    "原因": "资本外逃、汇率制度问题、金融体系脆弱",
                    "恢复措施": "IMF救助、汇率改革、金融体系重建"
                }
            },
            "人工智能": {
                "发展历程": {
                    "1950年代": "图灵测试提出，AI概念诞生，早期符号主义研究",
                    "1960年代": "专家系统概念提出，机器学习理论基础建立",
                    "1980年代": "专家系统商业化应用，神经网络复兴",
                    "1990年代": "机器学习算法改进，互联网推动数据积累",
                    "2000年代": "大数据兴起，机器学习快速发展",
                    "2010年代": "深度学习突破，图像识别、语音识别重大进展",
                    "2020年代": "大语言模型、ChatGPT等突破，AGI研究加速"
                },
                "主要技术": {
                    "机器学习": "让机器从数据中学习规律，包括监督学习、无监督学习、强化学习",
                    "深度学习": "模拟人脑神经网络结构，多层神经网络处理复杂数据",
                    "自然语言处理": "让机器理解和生成人类语言，包括文本分析、机器翻译",
                    "计算机视觉": "让机器识别和理解图像，包括目标检测、图像分类",
                    "强化学习": "通过试错学习最优策略，在游戏、机器人控制等领域应用"
                },
                "应用领域": {
                    "医疗健康": "疾病诊断、药物发现、个性化治疗、医学影像分析",
                    "金融服务": "风险评估、算法交易、反欺诈、智能投顾",
                    "自动驾驶": "环境感知、路径规划、决策控制、车联网",
                    "智能制造": "质量检测、预测维护、生产优化、机器人自动化"
                }
            },
            "编程技术": {
                "Python": {
                    "特点": "简洁易读、库丰富、跨平台、动态类型",
                    "应用领域": "数据科学、Web开发、人工智能、自动化脚本",
                    "优势": "开发效率高、社区活跃、学习曲线平缓",
                    "主要库": "NumPy、Pandas、TensorFlow、Django、Flask"
                },
                "JavaScript": {
                    "特点": "动态类型、事件驱动、异步编程、跨平台",
                    "应用领域": "前端开发、后端开发、移动应用、桌面应用",
                    "优势": "生态系统丰富、实时交互、全栈开发",
                    "主要框架": "React、Vue、Node.js、Express、Angular"
                },
                "机器学习": {
                    "监督学习": "使用标记数据训练模型，如分类、回归问题",
                    "无监督学习": "从无标记数据中发现模式，如聚类、降维",
                    "深度学习": "多层神经网络，处理复杂的非线性关系",
                    "最佳实践": "数据预处理、特征工程、模型验证、超参数调优"
                }
            }
        }
    
    def search_local_knowledge(self, query: str) -> List[Dict[str, Any]]:
        """在本地知识库中搜索"""
        results = []
        query_lower = query.lower()
        
        # 搜索关键词
        search_keywords = [
            '经济危机', '金融危机', '大萧条', '石油危机', '亚洲金融危机',
            '人工智能', 'ai', '机器学习', '深度学习', '神经网络',
            'python', 'javascript', '编程', '开发', '算法'
        ]
        
        matched_keywords = [kw for kw in search_keywords if kw in query_lower]
        
        for category, topics in self.knowledge_base.items():
            category_match = any(kw in category.lower() for kw in matched_keywords) or category.lower() in query_lower
            
            for topic, content in topics.items():
                topic_match = any(kw in topic.lower() for kw in matched_keywords) or topic.lower() in query_lower
                
                if category_match or topic_match:
                    if isinstance(content, dict):
                        for key, value in content.items():
                            results.append({
                                'title': f"{category} - {topic} - {key}",
                                'url': f"本地知识库/{category}/{topic}",
                                'snippet': f"{key}: {value}",
                                'category': category,
                                'topic': topic,
                                'subtopic': key
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
                'title': "本地知识库搜索建议",
                'url': "本地知识库",
                'snippet': f"未找到关于'{query}'的具体信息。建议尝试搜索：经济危机、人工智能、编程技术等主题，或直接与AI对话获取更多信息。",
                'category': "搜索建议",
                'topic': "使用提示"
            })
        
        return results[:6]  # 返回前6个结果

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
            "subtopics": [],
            "summary": ""
        }
        
        # 提取信息
        categories = []
        topics = []
        subtopics = []
        
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
            if 'subtopic' in result:
                subtopics.append(result['subtopic'])
        
        # 统计分类和主题
        if categories:
            category_counts = pd.Series(categories).value_counts().to_dict()
            analysis["category_distribution"] = category_counts
            analysis["categories"] = list(set(categories))
        
        if topics:
            analysis["topics"] = list(set(topics))
            
        if subtopics:
            analysis["subtopics"] = list(set(subtopics))
        
        return analysis
    
    def create_local_visualizations(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """创建本地数据的可视化图表"""
        charts = {}
        
        # 分类分布饼图
        if "category_distribution" in analysis and len(analysis["category_distribution"]) > 1:
            categories = list(analysis["category_distribution"].keys())
            counts = list(analysis["category_distribution"].values())
            
            fig_pie = px.pie(
                values=counts,
                names=categories,
                title="知识库搜索结果分类分布",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            charts["category_pie"] = fig_pie
        
        # 主题条形图
        if "topics" in analysis and len(analysis["topics"]) > 1:
            topics = analysis["topics"][:6]  # 取前6个
            topic_counts = list(range(len(topics), 0, -1))  # 模拟相关度
            
            fig_bar = px.bar(
                x=topic_counts,
                y=topics,
                orientation='h',
                title="相关主题分析",
                labels={'x': '相关度', 'y': '主题'},
                color=topic_counts,
                color_continuous_scale='Blues'
            )
            fig_bar.update_layout(showlegend=False)
            charts["topic_bar"] = fig_bar
        
        return charts

def main():
    st.title("🤖 AI智能助理 (改进版)")
    st.markdown("---")
    
    # 显示内网模式提示
    st.info("🔒 内网模式运行中 | 📚 本地知识库 | 🤖 AI对话 | 📊 智能分析")
    
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
        st.header("⚙️ 设置")
        
        # 模型选择
        available_models = st.session_state.ollama_client.get_models()
        selected_model = st.selectbox("🤖 AI模型", available_models)
        
        st.markdown("---")
        
        # 内网模式说明
        st.subheader("🔒 内网模式")
        st.success("✅ 本地AI对话")
        st.success("✅ 本地知识库搜索")
        st.success("✅ 数据分析可视化")
        st.error("❌ 外网搜索 (不可用)")
        
        st.markdown("---")
        
        # 本地知识库信息
        st.subheader("📚 知识库内容")
        with st.expander("经济危机", expanded=False):
            st.write("• 1929年大萧条")
            st.write("• 2008年金融危机")
            st.write("• 1973年石油危机")
            st.write("• 1997年亚洲金融危机")
        
        with st.expander("人工智能", expanded=False):
            st.write("• 发展历程")
            st.write("• 主要技术")
            st.write("• 应用领域")
        
        with st.expander("编程技术", expanded=False):
            st.write("• Python语言")
            st.write("• JavaScript开发")
            st.write("• 机器学习")
        
        st.markdown("---")
        
        # 使用统计
        if st.session_state.chat_history:
            st.subheader("📊 使用统计")
            st.metric("对话轮次", len(st.session_state.chat_history) // 2)
            
        # 清空历史
        if st.button("🗑️ 清空历史", use_container_width=True):
            st.session_state.chat_history = []
            if hasattr(st.session_state, 'latest_analysis'):
                delattr(st.session_state, 'latest_analysis')
            if hasattr(st.session_state, 'latest_charts'):
                delattr(st.session_state, 'latest_charts')
            st.rerun()
    
    # 主界面布局
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("💬 对话区域")
        
        # 显示聊天历史
        if st.session_state.chat_history:
            chat_html = '<div class="chat-history">'
            for i, (role, content) in enumerate(st.session_state.chat_history):
                if role == "user":
                    chat_html += f'''
                    <div class="user-message">
                        <strong>🧑 您:</strong><br>
                        {content.replace("\n", "<br>")}
                    </div>
                    '''
                else:
                    chat_html += f'''
                    <div class="ai-message">
                        <strong>🤖 AI助理:</strong><br>
                        {content.replace("\n", "<br>")}
                    </div>
                    '''
            chat_html += '</div>'
            st.markdown(chat_html, unsafe_allow_html=True)
        else:
            st.info("💡 开始对话吧！您可以询问任何问题或搜索本地知识库。")
        
        # 输入区域
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        user_input = st.text_area(
            "💭 请输入您的问题或需要查询的内容:", 
            height=80, 
            key="user_input",
            placeholder="例如：分析一下历史上的经济危机持续时间..."
        )
        
        col_btn1, col_btn2, col_btn3 = st.columns([2, 2, 1])
        with col_btn1:
            search_btn = st.button("🔍 本地搜索分析", type="primary", use_container_width=True)
        with col_btn2:
            chat_btn = st.button("💬 直接对话", use_container_width=True)
        with col_btn3:
            clear_btn = st.button("🧹 清空输入", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 处理按钮点击
        if clear_btn:
            st.session_state.user_input = ""
            st.rerun()
        elif search_btn and user_input.strip():
            process_local_search(user_input.strip(), selected_model)
        elif chat_btn and user_input.strip():
            process_direct_chat(user_input.strip(), selected_model)
        elif (search_btn or chat_btn) and not user_input.strip():
            st.warning("⚠️ 请先输入问题或查询内容")
    
    with col2:
        st.subheader("📊 分析面板")
        
        # 分析结果显示区域
        analysis_html = '<div class="analysis-panel">'
        
        if hasattr(st.session_state, 'latest_analysis'):
            analysis = st.session_state.latest_analysis
            
            # 基本统计
            analysis_html += f'''
            <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                <div style="text-align: center; flex: 1;">
                    <div style="font-size: 1.5rem; font-weight: bold; color: #1976d2;">{analysis.get("total_results", 0)}</div>
                    <div style="font-size: 0.8rem; color: #666;">搜索结果</div>
                </div>
                <div style="text-align: center; flex: 1;">
                    <div style="font-size: 1rem; font-weight: bold; color: #388e3c;">{analysis.get("timestamp", "").split(" ")[1] if analysis.get("timestamp") else ""}</div>
                    <div style="font-size: 0.8rem; color: #666;">分析时间</div>
                </div>
            </div>
            '''
            
            # 相关主题
            if analysis.get("topics"):
                analysis_html += '<h4>🏷️ 相关主题</h4><div style="margin-bottom: 1rem;">'
                for topic in analysis["topics"][:5]:
                    analysis_html += f'<span class="topic-tag">🔖 {topic}</span>'
                analysis_html += '</div>'
            
            # 知识分类
            if analysis.get("categories"):
                analysis_html += '<h4>📂 知识分类</h4><div style="margin-bottom: 1rem;">'
                for category in analysis["categories"]:
                    analysis_html += f'<span class="category-tag">📁 {category}</span>'
                analysis_html += '</div>'
            
            # 搜索结果详情
            if analysis.get("sources"):
                analysis_html += '<h4>📝 搜索结果详情</h4>'
                for i, source in enumerate(analysis["sources"][:4], 1):
                    analysis_html += f'''
                    <div style="background-color: white; padding: 0.75rem; margin-bottom: 0.5rem; border-radius: 6px; border-left: 3px solid #4caf50;">
                        <div style="font-weight: bold; font-size: 0.9rem; margin-bottom: 0.25rem;">
                            {i}. {source["title"][:60]}{"..." if len(source["title"]) > 60 else ""}
                        </div>
                        <div style="font-size: 0.8rem; color: #666; margin-bottom: 0.25rem;">
                            📍 {source["source"]}
                        </div>
                        <div style="font-size: 0.85rem; line-height: 1.4;">
                            {source["snippet"][:150]}{"..." if len(source["snippet"]) > 150 else ""}
                        </div>
                    </div>
                    '''
        else:
            analysis_html += '''
            <div style="text-align: center; padding: 2rem; color: #666;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
                <div style="font-size: 1.1rem; margin-bottom: 0.5rem;">等待分析结果</div>
                <div style="font-size: 0.9rem;">执行搜索后，这里将显示详细的分析结果</div>
            </div>
            '''
        
        analysis_html += '</div>'
        st.markdown(analysis_html, unsafe_allow_html=True)
        
        # 图表区域
        if hasattr(st.session_state, 'latest_charts'):
            charts = st.session_state.latest_charts
            
            if "category_pie" in charts:
                st.plotly_chart(charts["category_pie"], use_container_width=True, height=250)
            
            if "topic_bar" in charts:
                st.plotly_chart(charts["topic_bar"], use_container_width=True, height=250)

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
        
        content_for_ai += f"\n请基于以上本地知识库的搜索结果，对'{query}'进行综合分析和总结。请提供详细、准确的信息，如果信息不够完整，请结合您的知识进行补充说明。"
    
    with st.spinner("🤖 AI正在分析..."):
        # 获取AI分析
        ai_response = st.session_state.ollama_client.chat(content_for_ai, model)
        st.session_state.chat_history.append(("assistant", ai_response))
        
        st.success("✅ 分析完成！")
        time.sleep(0.5)  # 短暂延迟让用户看到成功消息
        st.rerun()

def process_direct_chat(query: str, model: str):
    """处理直接对话"""
    with st.spinner("🤖 AI正在思考..."):
        st.session_state.chat_history.append(("user", query))
        
        ai_response = st.session_state.ollama_client.chat(query, model)
        st.session_state.chat_history.append(("assistant", ai_response))
        
        st.success("✅ 回复完成！")
        time.sleep(0.5)
        st.rerun()

# 添加使用提示
def show_usage_tips():
    with st.expander("💡 使用指南", expanded=False):
        st.markdown("""
        ### 🎯 功能介绍
        
        **🔍 本地搜索分析**
        - 在内置知识库中搜索相关信息
        - 自动生成分析报告和可视化图表
        - 结合AI进行深度解读
        
        **💬 直接对话**
        - 与本地AI模型直接交流
        - 获得基于AI知识的回答
        - 支持各种类型的问答
        
        ### 📚 推荐查询
        
        **经济话题**
        - "分析历史上的经济危机持续时间"
        - "2008年金融危机的成因和影响"
        - "经济危机的共同特征"
        
        **技术话题**
        - "人工智能的发展历程"
        - "Python和JavaScript的区别"
        - "机器学习的主要技术"
        
        **开放问题**
        - "如何学习编程？"
        - "AI对未来工作的影响"
        - "数据科学入门建议"
        
        ### ⚡ 操作技巧
        - 界面支持完整滚动，可查看所有内容
        - 聊天历史和分析面板都可独立滚动
        - 使用"清空输入"快速重新开始
        - 侧边栏显示详细的知识库内容
        """)

if __name__ == "__main__":
    show_usage_tips()
    main()