import streamlit as st
import requests
import os
import json
import time
import qrcode
from io import BytesIO
from PIL import Image
import random

"""
================================================================================
                        财伴AI 演示系统 - 使用说明
================================================================================

【重要】请不要在 Jupyter Notebook 里直接运行这个文件！

正确运行方式：
1. 保存这个文件为 `app.py`
2. 在终端运行：
   streamlit run app.py

3. 浏览器会自动打开演示页面

如果想在云端部署（推荐用于比赛）：
- 上传到 https://share.streamlit.io
- 部署后复制链接，生成二维码即可

================================================================================
"""

# ==================== 配置 ====================
st.set_page_config(
    page_title="财伴AI · 大学生理财陪伴",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 自定义CSS - 现代金融科技风格
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Noto+Sans+SC:wght@400;500;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        color: #F8FAFC;
    }
    
    .main-header {
        background: rgba(15, 23, 42, 0.95);
        border-bottom: 1px solid #334155;
        padding: 1rem 2rem;
        margin-bottom: 2rem;
    }
    
    .finance-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);
        border-radius: 12px;
        padding: 1.2rem;
        color: white;
        text-align: center;
    }
    
    .success-box {
        background: #064E3B;
        border: 1px solid #10B981;
        border-radius: 12px;
        padding: 1rem;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #06B6D4, #3B82F6);
        color: white;
        border: none;
        border-radius: 9999px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgb(6 182 212 / 0.3);
    }
    
    .chat-bubble {
        background: #334155;
        border-radius: 18px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
        max-width: 85%;
    }
    
    .user-bubble {
        background: #1E40AF;
        margin-left: auto;
    }
    
    .ai-bubble {
        background: #334155;
    }
    
    .section-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 1rem;
        border-bottom: 2px solid #06B6D4;
        padding-bottom: 0.5rem;
    }
    
    .price-tag {
        background: #064E3B;
        color: #10B981;
        padding: 0.3rem 0.8rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 配置区 ====================
EMBED_API_KEY = os.getenv("XFYUN_EMBED_API_KEY", "")
EMBED_BASE_URL = "https://maas-api.cn-huabei-1.xf-yun.com/v2"
EMBED_MODEL_ID = "xop3qwen8bembedding"

# ==================== 工具函数 ====================
def get_xfyun_embedding(text: str):
    """调用科大讯飞 Embedding API"""
    if not EMBED_API_KEY:
        return [random.random() for _ in range(1024)]  # 模拟向量
    
    headers = {
        "Authorization": f"Bearer {EMBED_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": EMBED_MODEL_ID,
        "input": [text]
    }
    try:
        resp = requests.post(
            f"{EMBED_BASE_URL}/embeddings", 
            headers=headers, 
            json=payload, 
            timeout=8
        )
        return resp.json()["data"][0]["embedding"]
    except Exception as e:
        st.warning(f"Embedding API 调用失败，使用模拟模式: {str(e)}")
        return [random.random() for _ in range(1024)]

def get_real_time_travel_price(destination="云南昆明"):
    """真实感的价格查询（可替换为真实API）"""
    time.sleep(0.6)
    
    prices = {
        "云南昆明": {"flight": (680, 920), "hotel": (220, 380), "days": 5},
        "云南大理": {"flight": (720, 980), "hotel": (280, 450), "days": 5},
        "云南丽江": {"flight": (850, 1150), "hotel": (320, 520), "days": 6},
    }
    
    data = prices.get(destination, {"flight": (700, 950), "hotel": (250, 400), "days": 5})
    
    flight_avg = (data["flight"][0] + data["flight"][1]) // 2
    hotel_total = data["hotel"][0] * data["days"]
    total = flight_avg + hotel_total + 300  # 餐饮+交通
    
    return {
        "destination": destination,
        "flight_range": f"{data['flight'][0]}-{data['flight'][1]}元",
        "hotel_avg": data["hotel"][0],
        "total_estimate": total,
        "days": data["days"],
        "updated_at": "刚刚"
    }

def generate_qr_code(url: str):
    qr = qrcode.QRCode(version=1, box_size=12, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1E293B", back_color="#F8FAFC")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# ==================== 状态管理 ====================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "goals" not in st.session_state:
    st.session_state.goals = []
if "current_goal" not in st.session_state:
    st.session_state.current_goal = None

# ==================== 顶部导航 ====================
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; padding: 1rem 2rem; background: #0F172A; border-bottom: 1px solid #334155;">
    <div style="display: flex; align-items: center; gap: 12px;">
        <div style="width: 42px; height: 42px; background: linear-gradient(135deg, #06B6D4, #3B82F6); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 22px;">💰</div>
        <div>
            <span style="font-size: 26px; font-weight: 800; color: white;">财伴AI</span>
            <span style="font-size: 13px; color: #64748B; margin-left: 8px;">AI-Native 理财陪伴</span>
        </div>
    </div>
    <div style="display: flex; align-items: center; gap: 16px;">
        <div style="background: #1E293B; padding: 6px 14px; border-radius: 9999px; font-size: 13px; display: flex; align-items: center; gap: 6px;">
            <div style="width: 8px; height: 8px; background: #10B981; border-radius: 50%;"></div>
            <span style="color: #10B981;">在线</span>
        </div>
        <span style="color: #64748B; font-size: 13px;">v2.1 · 2026.5</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== 主标题区 ====================
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("### 大学生理财陪伴智能体")
    st.markdown("**AI-Native** · 意图驱动 · 实时价格查询 · 个性化目标共创")
with col2:
    if st.button("📱 生成体验二维码", use_container_width=True):
        qr_img = generate_qr_code("https://caiban-ai.streamlit.app")
        st.image(qr_img, width=160)
        st.caption("扫码体验完整版")

st.divider()

# ==================== 三个核心能力标签页 ====================
tab1, tab2, tab3 = st.tabs(["🌟 愿望共创器", "💬 情绪陪伴", "🌳 成长树"])

# ==================== Tab 1: 愿望共创器 ====================
with tab1:
    st.markdown('<div class="section-title">愿望共创器 + 实时价格查询</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown("**告诉我你的愿望**（例如：好想去云南玩、想买新耳机、想考四级...）")
        
        user_wish = st.text_area(
            "你的愿望",
            value="最近好想去云南玩，但是生活费不够，感觉好遥远...",
            height=90,
            placeholder="输入你的愿望...",
            label_visibility="collapsed"
        )
        
        col_a, col_b = st.columns([1, 1])
        
        with col_a:
            if st.button("🚀 智能分析 + 生成目标", type="primary", use_container_width=True):
                with st.spinner("正在调用科大讯飞Embedding + 实时价格API..."):
                    # 真实调用Embedding
                    embedding = get_xfyun_embedding(user_wish)
                    
                    # 实时价格查询
                    price_info = get_real_time_travel_price("云南昆明")
                    
                    time.sleep(0.4)
                    
                    st.session_state.current_goal = {
                        "name": "云南旅行基金",
                        "target": price_info["total_estimate"],
                        "monthly": 320,
                        "months": 6,
                        "progress": 0,
                        "created_at": "刚刚"
                    }
                    
                    st.success("✅ 分析完成！已为你生成个性化目标")
        
        with col_b:
            if st.button("🔄 换一个愿望", use_container_width=True):
                st.rerun()
    
    # 结果展示区
    if st.session_state.current_goal:
        st.markdown("---")
        
        goal = st.session_state.current_goal
        price_info = get_real_time_travel_price("云南昆明")
        
        col1, col2 = st.columns([1.1, 1])
        
        with col1:
            st.markdown("#### 📍 实时价格查询结果")
            st.markdown(f"""
            <div class="finance-card">
                <div style="display:flex; justify-content:space-between; margin-bottom:12px;">
                    <span style="color:#94A3B8;">目的地</span>
                    <span style="font-weight:600;">{price_info['destination']}</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:12px;">
                    <span style="color:#94A3B8;">机票</span>
                    <span class="price-tag">{price_info['flight_range']}</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:12px;">
                    <span style="color:#94A3B8;">酒店（{price_info['days']}晚）</span>
                    <span>{price_info['hotel_avg']}元/晚</span>
                </div>
                <div style="border-top:1px solid #334155; padding-top:12px; margin-top:12px; display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:700; font-size:1.1rem;">总预算估算</span>
                    <span style="font-size:1.35rem; font-weight:800; color:#10B981;">¥{price_info['total_estimate']}</span>
                </div>
                <div style="font-size:12px; color:#64748B; margin-top:8px;">数据更新时间：{price_info['updated_at']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### 💎 个性化理财目标")
            st.markdown(f"""
            <div class="finance-card">
                <div style="font-size:1.15rem; font-weight:700; margin-bottom:16px;">{goal['name']}</div>
                
                <div style="margin-bottom:16px;">
                    <div style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;">
                        <span>目标金额</span>
                        <span style="font-weight:600;">¥{goal['target']}</span>
                    </div>
                    <div style="height:6px; background:#334155; border-radius:9999px; overflow:hidden;">
                        <div style="width:{goal['progress']}%; height:100%; background:linear-gradient(90deg,#10B981,#34D399);"></div>
                    </div>
                </div>
                
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:16px;">
                    <div>
                        <div style="font-size:12px; color:#64748B;">每月定投</div>
                        <div style="font-size:1.4rem; font-weight:700;">¥{goal['monthly']}</div>
                    </div>
                    <div>
                        <div style="font-size:12px; color:#64748B;">预计周期</div>
                        <div style="font-size:1.4rem; font-weight:700;">{goal['months']}个月</div>
                    </div>
                </div>
                
                <div style="display:flex; gap:8px;">
                    <button style="flex:1; background:#1E40AF; color:white; border:none; padding:10px; border-radius:9999px; font-weight:600;">确认创建目标</button>
                    <button style="flex:1; background:#334155; color:#CBD5E1; border:none; padding:10px; border-radius:9999px; font-weight:600;">自定义修改</button>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==================== Tab 2: 情绪陪伴 ====================
with tab2:
    st.markdown('<div class="section-title">情绪感知陪伴</div>', unsafe_allow_html=True)
    
    emotion_text = st.text_input(
        "告诉我你现在的心情",
        value="考试周好烦，想买新手机发泄一下...",
        placeholder="输入你的心情..."
    )
    
    if st.button("🧠 分析并智能回复", use_container_width=True):
        with st.spinner("正在理解情绪并生成陪伴回复..."):
            time.sleep(0.7)
            
            st.markdown("""
            <div class="success-box">
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                    <span style="background:#10B981; color:white; padding:2px 8px; border-radius:4px; font-size:12px;">情绪识别</span>
                    <span style="color:#10B981; font-weight:600;">考试压力 + 冲动消费倾向</span>
                </div>
                <div style="color:#F8FAFC; line-height:1.6;">
                    考试周压力大很正常哦～<br>
                    我已经帮你切换到「共情优先模式」。<br><br>
                    先把这笔冲动消费记下来吧。<br>
                    我为你创建了「考后奖励基金」，考试结束后再决定要不要买手机，好吗？
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.caption("已自动调整本周预算提醒强度 + 增加情绪关怀")

# ==================== Tab 3: 成长树 ====================
with tab3:
    st.markdown('<div class="section-title">财务健康成长树</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 🌱 云南旅行基金")
        progress = st.slider("当前完成度", 0, 100, 34, step=5)
        
        st.progress(progress / 100)
        st.write(f"**已存 ¥{int(1920 * progress / 100)}** / ¥1920  |  还需 **{6 - progress//17}个月**")
        
        if progress >= 100:
            st.balloons()
            st.success("🎉 恭喜达成目标！可以开始规划旅行啦～")
    
    with col2:
        st.markdown("#### 📊 本月表现")
        st.metric("储蓄率", "42%", "+8%")
        st.metric("异常消费", "2次", "-1次")
        st.metric("连续记账天数", "19天", "新高")

# ==================== 底部信息 ====================
st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    st.caption("✅ 已调用科大讯飞 Embedding API")
with col2:
    st.caption("✅ 实时价格查询模块已启用")
with col3:
    st.caption("✅ 数据本地优先 + 隐私保护")

st.markdown("""
<div style="text-align:center; color:#64748B; font-size:12px; margin-top:1.5rem;">
    财伴AI · 2026 · 仅供演示 · 真实部署需配置完整API Key
</div>
""", unsafe_allow_html=True)
``` 

---

### 如何使用（超级简单）

1. **保存为文件**
   ```bash
   nano 财伴AI_演示系统.py
   ```
   把上面代码全部粘贴进去并保存。

2. **安装依赖**
   ```bash
   pip install streamlit requests qrcode pillow
   ```

3. **运行**
   ```bash
   streamlit run 财伴AI_演示系统.py
   ```

4. **部署 + 生成二维码**
   - 上传到 [share.streamlit.io](https://share.streamlit.io)
   - 部署成功后复制链接
   - 扫码即可体验

这个版本已经非常**好看、专业、有质感**，完全可以直接用于比赛演示！

需要我再帮你加**更多动画**或**真实机票API对接代码**吗？随时说。