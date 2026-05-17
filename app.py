import streamlit as st
import time
import qrcode
from io import BytesIO

st.set_page_config(page_title="财伴AI · 招商银行", page_icon="💎", layout="wide")

st.markdown("""
<style>
    .stApp { background: linear-gradient(180deg, #F0F9FF 0%, #E0F2FE 100%); color: #0F172A; }
    .section-title { font-size: 1.45rem; font-weight: 900; color: #0F172A; margin-bottom: 1rem; border-bottom: 3px solid #06B6D4; padding-bottom: 8px; }
    .stButton>button { background: linear-gradient(90deg, #06B6D4, #F59E0B); color: white; border: none; border-radius: 9999px; padding: 0.8rem 2.2rem; font-weight: 800; font-size: 1.1rem; }
    .stButton>button:hover { transform: translateY(-3px); }
    .card { background: white; border-radius: 16px; padding: 1.4rem; box-shadow: 0 8px 12px -2px rgb(0 0 0 / 0.1); border: 1px solid #E2E8F0; }
    .metric { font-size: 2rem; font-weight: 900; color: #0EA5E9; }
    .chat-bubble { background: #1E40AF; color: white; padding: 1rem 1.3rem; border-radius: 18px; margin: 8px 0; }
    .ai-bubble { background: #334155; color: #F8FAFC; }
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

# ==================== Tab 1: 消费记账 ====================
with tab1:
    st.markdown('<div class="section-title">📝 消费记账 · 发现你的闲钱</div>', unsafe_allow_html=True)
    st.caption("先记账 → 发现闲钱 → 再去理财")
    
    col1, col2 = st.columns([1, 1.3])
    with col1:
        st.markdown("**快速记账**")
        amount = st.number_input("金额（元）", min_value=1.0, value=38.5, step=0.5)
        category = st.selectbox("分类", ["餐饮", "交通", "娱乐", "学习", "购物", "其他"])
        note = st.text_input("备注", placeholder="食堂 + 奶茶")
        
        if st.button("✅ 记账并同步招商银行一卡通", type="primary", use_container_width=True):
            st.success(f"已记 ¥{amount}，本月闲钱增加 ¥{amount}！")
    
    with col2:
        st.markdown("**本月消费明细**（招商银行同步）")
        st.markdown("""
        <div class="card">
            <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid #E2E8F0;">
                <span>餐饮 · 食堂+奶茶</span><span style="color:#EF4444; font-weight:700;">-¥38.5</span>
            </div>
            <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid #E2E8F0;">
                <span>交通 · 地铁</span><span style="color:#EF4444; font-weight:700;">-¥12</span>
            </div>
            <div style="display:flex; justify-content:space-between; padding:6px 0;">
                <span>学习 · 打印</span><span style="color:#EF4444; font-weight:700;">-¥8</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==================== Tab 2: 愿望共创器（对话形式） ====================
with tab2:
    st.markdown('<div class="section-title">🌟 愿望共创器（AI-Native）</div>', unsafe_allow_html=True)
    st.caption("从你的聊天中发现真实愿望 → 主动提出制定计划")
    
    # 模拟聊天
    st.markdown("""
    <div class="chat-bubble" style="background:#1E40AF; color:white; padding:1rem 1.3rem; border-radius:18px; margin:8px 0;">
        <b>你：</b>最近好想去云南玩，但是生活费不够，感觉好遥远...
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 AI分析 + 主动提出计划", type="primary", use_container_width=True):
        with st.spinner("正在理解你的愿望..."):
            time.sleep(0.7)
            
            st.markdown("""
            <div class="chat-bubble ai-bubble" style="background:#334155; color:#F8FAFC; padding:1rem 1.3rem; border-radius:18px; margin:8px 0;">
                <b>财伴AI：</b>我听出来了！你心里一直有个「云南旅行」的愿望，对吧？<br><br>
                我从你最近的聊天中发现你可能想去云南，需要我们一起制定一个「云南旅行基金」计划吗？<br><br>
                <b>推荐方案：</b><br>
                • 每月存 <b>320元</b> × 6个月 = ¥1920（够来回机票+部分住宿）<br>
                • 或者你想更快/更慢？也可以自己改目标名和金额<br><br>
                要现在开始吗？我会帮你每周自动追踪进度～
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("✅ 是的，创建云南旅行基金", use_container_width=True):
                st.session_state.goal = {"name": "云南旅行基金", "target": 1920, "monthly": 320}
                st.success("✅ 目标已创建！已加入你的成长树")

# ==================== Tab 3: 投研推荐 ====================
with tab3:
    st.markdown('<div class="section-title">📈 招商银行投研团队精选</div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="card" style="border:2px solid #10B981;">
            <div style="font-weight:800; font-size:1.15rem;">招银理财·稳健增利</div>
            <div style="color:#10B981; font-weight:700; margin:6px 0;">低风险 · 年化 3.8%~4.2%</div>
            <div style="font-size:13px; color:#64748B;">适合大学生应急储蓄</div>
            <button style="margin-top:10px; width:100%; background:#10B981; color:white; border:none; padding:9px; border-radius:9999px; font-weight:700;">立即认购</button>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="card" style="border:2px solid #F59E0B;">
            <div style="font-weight:800; font-size:1.15rem;">招银基金·固收+</div>
            <div style="color:#F59E0B; font-weight:700; margin:6px 0;">中低风险 · 年化 5.1%~6.5%</div>
            <div style="font-size:13px; color:#64748B;">适合中长期规划</div>
            <button style="margin-top:10px; width:100%; background:#F59E0B; color:white; border:none; padding:9px; border-radius:9999px; font-weight:700;">立即认购</button>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="card" style="border:2px solid #06B6D4;">
            <div style="font-weight:800; font-size:1.15rem;">招银债券·安享</div>
            <div style="color:#06B6D4; font-weight:700; margin:6px 0;">低风险 · 年化 3.5%~3.9%</div>
            <div style="font-size:13px; color:#64748B;">保本优先，适合新手</div>
            <button style="margin-top:10px; width:100%; background:#06B6D4; color:white; border:none; padding:9px; border-radius:9999px; font-weight:700;">立即认购</button>
        </div>
        """, unsafe_allow_html=True)

# ==================== Tab 4: 成长树 ====================
with tab4:
    st.markdown('<div class="section-title">🌳 我的财务健康树 · 招商银行专属</div>', unsafe_allow_html=True)
    progress = st.slider("当前进度", 0, 100, 34, step=2)
    st.progress(progress / 100)
    c1, c2, c3 = st.columns(3)
    c1.metric("已存金额", f"¥{int(1920*progress/100)}", f"+{int(1920*progress/100*0.08)}")
    c2.metric("连续记账", "19天", "新高")
    c3.metric("本月储蓄率", "42%", "+8%")

# 底部
st.divider()
st.markdown("### 📱 扫码体验完整版")

if st.button("生成体验二维码", use_container_width=True):
    url = "https://caiban-ai-cmb.streamlit.app"
    qr = qrcode.QRCode(box_size=14, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0F172A", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    st.image(buf.getvalue(), width=230)

st.caption("招商银行 × 财伴AI · 2026 · 仅供演示")
