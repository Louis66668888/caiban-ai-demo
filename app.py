import streamlit as st
import time
import qrcode
from io import BytesIO

st.set_page_config(page_title="财伴AI · 招商银行", page_icon="💎", layout="wide")

st.markdown("""
<style>
    .stApp { background: linear-gradient(180deg, #F0F9FF 0%, #E0F2FE 100%); color: #0F172A; }
    .section-title { font-size: 1.45rem; font-weight: 900; color: #0F172A; margin-bottom: 1rem; border-bottom: 3px solid #06B6D4; padding-bottom: 8px; }
    .stButton>button { background: linear-gradient(90deg, #06B6D4, #F59E0B); color: white; border: none; border-radius: 9999px; padding: 0.75rem 2rem; font-weight: 800; font-size: 1.05rem; }
    .stButton>button:hover { transform: translateY(-3px); }
    .card { background: white; border-radius: 16px; padding: 1.4rem; box-shadow: 0 8px 12px -2px rgb(0 0 0 / 0.1); border: 1px solid #E2E8F0; }
    .llm-box { background: #1E40AF; color: white; padding: 1.2rem 1.5rem; border-radius: 16px; margin: 12px 0; }
    .input-area { background: white; padding: 1.2rem; border-radius: 16px; border: 2px solid #06B6D4; }
</style>
""", unsafe_allow_html=True)

# 顶部
st.markdown("""
<div style="display:flex; align-items:center; justify-content:space-between; padding:1rem 2rem; background:white; border-bottom:2px solid #06B6D4; margin-bottom:1.5rem; border-radius:0 0 16px 16px;">
    <div style="display:flex; align-items:center; gap:14px;">
        <div style="width:52px; height:52px; background:linear-gradient(135deg,#06B6D4,#F59E0B); border-radius:14px; display:flex; align-items:center; justify-content:center; font-size:28px;">💎</div>
        <div>
            <span style="font-size:30px; font-weight:900; color:#0F172A;">财伴AI</span>
            <span style="font-size:15px; color:#F59E0B; margin-left:10px; font-weight:800;">招商银行 × 大学生</span>
        </div>
    </div>
    <div style="background:#DCFCE7; color:#16A34A; padding:8px 18px; border-radius:9999px; font-weight:700; font-size:14px;">✓ 已接入招商银行</div>
</div>
""", unsafe_allow_html=True)

st.markdown("## 大学生理财陪伴智能体 · 招商银行专属版")

tab1, tab2, tab3, tab4 = st.tabs(["📝 消费记账", "🌟 愿望共创器", "📈 投研推荐", "🌳 成长树"])

# ==================== Tab 1: 消费记账（正确布局） ====================
with tab1:
    st.markdown('<div class="section-title">📝 消费记账 · 发现你的闲钱</div>', unsafe_allow_html=True)
    st.caption("先记账 → 发现闲钱 → 再去理财")
    
    # 左上 + 主要区域：LLM分析结果
    st.markdown("""
    <div class="llm-box">
        <div style="font-weight:700; font-size:1.05rem; margin-bottom:8px;">🤖 大语言模型分析结果</div>
        <div style="font-size:1.05rem; line-height:1.6;">
            本月你已记账 <b>3笔</b>，总支出 <b>¥58.5</b><br>
            餐饮占比 <b>66%</b>（偏高），建议本周控制在外卖上<br>
            <b>本月闲钱增加 ¥38.5</b>！可以考虑存入「云南旅行基金」
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 右下角：输入区域
    st.markdown("---")
    st.markdown("**快速记账**（右下角操作区）")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🎤 语音记账", use_container_width=True):
            st.info("（模拟）语音识别中... 已识别：'今天食堂花了38块5'")
            st.success("已记账 ¥38.5（餐饮 · 食堂+奶茶）")
    with col2:
        if st.button("✍️ 文字记账", use_container_width=True):
            st.info("（模拟）打开文字输入框")
            st.success("已记账 ¥38.5（餐饮 · 食堂+奶茶）")

# ==================== Tab 2: 愿望共创器 ====================
with tab2:
    st.markdown('<div class="section-title">🌟 愿望共创器（AI-Native）</div>', unsafe_allow_html=True)
    st.caption("从聊天中提取真实愿望 → 主动提出计划")
    
    st.markdown("""
    <div style="background:#1E40AF; color:white; padding:1.2rem 1.5rem; border-radius:16px; margin:12px 0;">
        <b>你：</b>最近好想去云南玩，但是生活费不够，感觉好遥远...
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 AI分析 + 主动提出计划", type="primary", use_container_width=True):
        with st.spinner("正在理解你的愿望..."):
            time.sleep(0.6)
            st.markdown("""
            <div style="background:#334155; color:#F8FAFC; padding:1.2rem 1.5rem; border-radius:16px; margin:12px 0;">
                <b>财伴AI：</b>我听出来了！你心里一直有个「云南旅行」的愿望，对吧？<br><br>
                我从你最近的聊天中发现你可能想去云南，需要我们一起制定一个「云南旅行基金」计划吗？<br><br>
                <b>推荐方案：</b>每月存 <b>320元</b> × 6个月 = ¥1920<br>
                要现在开始吗？
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("✅ 是的，创建云南旅行基金", use_container_width=True):
                st.session_state.goal = {"name": "云南旅行基金", "target": 1920, "monthly": 320}
                st.success("✅ 目标已创建！")

# ==================== Tab 3 & 4 保持简洁 ====================
with tab3:
    st.markdown('<div class="section-title">📈 招商银行投研团队精选</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class="card" style="border:2px solid #10B981;"><div style="font-weight:800;">招银理财·稳健增利</div><div style="color:#10B981; font-weight:700;">低风险 · 年化 3.8%~4.2%</div><button style="margin-top:8px; width:100%; background:#10B981; color:white; border:none; padding:8px; border-radius:9999px; font-weight:700;">立即认购</button></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="card" style="border:2px solid #F59E0B;"><div style="font-weight:800;">招银基金·固收+</div><div style="color:#F59E0B; font-weight:700;">中低风险 · 年化 5.1%~6.5%</div><button style="margin-top:8px; width:100%; background:#F59E0B; color:white; border:none; padding:8px; border-radius:9999px; font-weight:700;">立即认购</button></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="card" style="border:2px solid #06B6D4;"><div style="font-weight:800;">招银债券·安享</div><div style="color:#06B6D4; font-weight:700;">低风险 · 年化 3.5%~3.9%</div><button style="margin-top:8px; width:100%; background:#06B6D4; color:white; border:none; padding:8px; border-radius:9999px; font-weight:700;">立即认购</button></div>""", unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="section-title">🌳 我的财务健康树</div>', unsafe_allow_html=True)
    progress = st.slider("当前进度", 0, 100, 34, step=2)
    st.progress(progress / 100)
    c1, c2, c3 = st.columns(3)
    c1.metric("已存金额", f"¥{int(1920*progress/100)}")
    c2.metric("连续记账", "19天")
    c3.metric("本月储蓄率", "42%")

# ==================== 底部下载区（国内推荐） ====================
st.divider()

st.markdown("### 📥 下载财伴AI招商银行APP")


st.caption("招商银行 × 财伴AI · 2026 · 仅供演示")
