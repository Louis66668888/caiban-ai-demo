import streamlit as st
import time
import qrcode
from io import BytesIO

st.set_page_config(page_title="财伴AI · 招商银行", page_icon="💎", layout="wide")

# 活泼年轻风格
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0F172A 0%, #1E3A5F 100%); color: #F8FAFC; }
    .section-title { font-size: 1.4rem; font-weight: 800; color: #F8FAFC; margin-bottom: 1rem; }
    .finance-card { 
        background: #1E293B; border: 1px solid #334155; border-radius: 16px; padding: 1.5rem; 
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.2);
    }
    .metric { font-size: 1.8rem; font-weight: 800; color: #34D399; }
    .stButton>button { 
        background: linear-gradient(90deg, #06B6D4, #F59E0B); color: white; border: none; 
        border-radius: 9999px; padding: 0.7rem 2.2rem; font-weight: 700; font-size: 1.05rem;
    }
    .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 20px 25px -5px rgb(245 158 11 / 0.3); }
    .product-card {
        background: #1E293B; border: 2px solid #06B6D4; border-radius: 14px; padding: 1.2rem;
        transition: all 0.3s ease;
    }
    .product-card:hover { border-color: #F59E0B; transform: translateY(-4px); }
</style>
""", unsafe_allow_html=True)

# 顶部导航
st.markdown("""
<div style="display:flex; align-items:center; justify-content:space-between; padding:0.8rem 2rem; background:#0F172A; border-bottom:1px solid #334155;">
    <div style="display:flex; align-items:center; gap:12px;">
        <div style="width:48px; height:48px; background:linear-gradient(135deg,#06B6D4,#F59E0B); border-radius:14px; display:flex; align-items:center; justify-content:center; font-size:26px;">💎</div>
        <div>
            <span style="font-size:28px; font-weight:900; color:white;">财伴AI</span>
            <span style="font-size:14px; color:#F59E0B; margin-left:8px; font-weight:700;">招商银行 × 大学生理财</span>
        </div>
    </div>
    <div style="display:flex; align-items:center; gap:12px;">
        <div style="background:#064E3B; color:#34D399; padding:6px 14px; border-radius:9999px; font-size:13px; font-weight:600;">✓ 已接入招商银行</div>
        <div style="color:#64748B; font-size:13px;">v2.2 · 2026.5</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("### 大学生理财陪伴智能体 · 招商银行专属版")

tab1, tab2, tab3, tab4 = st.tabs(["🌟 愿望共创器", "📝 消费记账", "📈 投研推荐", "🌳 成长树"])

# ==================== Tab 1: 愿望共创器 ====================
with tab1:
    st.markdown('<div class="section-title">✨ 愿望共创器 + 实时价格查询</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.1, 1])
    
    with col1:
        st.markdown("**告诉我你的旅行愿望**")
        destination = st.selectbox("目的地", ["云南昆明", "云南大理", "云南丽江", "四川成都", "海南三亚"], index=0)
        
        if st.button("🚀 实时查询价格 + 生成目标", type="primary", use_container_width=True):
            with st.spinner("正在查询招商银行合作旅行平台价格..."):
                time.sleep(0.8)
                
                prices = {
                    "云南昆明": {"flight": "680-920元", "hotel": "220元/晚", "total": 2200},
                    "云南大理": {"flight": "720-980元", "hotel": "280元/晚", "total": 2450},
                    "云南丽江": {"flight": "850-1150元", "hotel": "320元/晚", "total": 2680},
                    "四川成都": {"flight": "580-780元", "hotel": "200元/晚", "total": 1980},
                    "海南三亚": {"flight": "980-1380元", "hotel": "380元/晚", "total": 3120},
                }
                p = prices[destination]
                
                st.session_state.goal = {
                    "name": f"{destination}旅行基金",
                    "target": p["total"],
                    "monthly": 320,
                    "months": 6
                }
                st.success("✅ 已生成个性化目标！")
    
    with col2:
        if "goal" in st.session_state:
            g = st.session_state.goal
            st.markdown(f"""
            <div class="finance-card">
                <div style="font-size:1.3rem; font-weight:800; margin-bottom:12px;">{g['name']}</div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                    <div>
                        <div style="font-size:12px; color:#64748B;">目标金额</div>
                        <div class="metric">¥{g['target']}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:12px; color:#64748B;">每月定投</div>
                        <div style="font-size:1.6rem; font-weight:800; color:#34D399;">¥{g['monthly']}</div>
                    </div>
                </div>
                <div style="height:8px; background:#334155; border-radius:9999px; overflow:hidden; margin:12px 0;">
                    <div style="width:34%; height:100%; background:linear-gradient(90deg,#34D399,#10B981);"></div>
                </div>
                <div style="font-size:13px; color:#94A3B8;">已完成 34% · 预计 {g['months']} 个月达成</div>
            </div>
            """, unsafe_allow_html=True)

# ==================== Tab 2: 消费记账 ====================
with tab2:
    st.markdown('<div class="section-title">📝 消费记账 · 招商银行一卡通同步</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.3])
    
    with col1:
        st.markdown("**快速记账**")
        amount = st.number_input("金额（元）", min_value=1.0, value=38.5, step=0.5)
        category = st.selectbox("分类", ["餐饮", "交通", "娱乐", "学习", "购物", "其他"])
        note = st.text_input("备注（可选）", placeholder="食堂 + 奶茶")
        
        if st.button("✅ 记账并同步招商银行", use_container_width=True):
            if "records" not in st.session_state:
                st.session_state.records = []
            st.session_state.records.append({
                "time": "刚刚", "amount": amount, "category": category, "note": note
            })
            st.success(f"已记账 ¥{amount} 并同步到招商银行一卡通")
    
    with col2:
        st.markdown("**本周消费明细**（招商银行同步）")
        if "records" in st.session_state and st.session_state.records:
            for r in st.session_state.records[-5:]:
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid #334155;">
                    <div><span style="color:#F59E0B;">{r['category']}</span> {r['note']}</div>
                    <div style="font-weight:700; color:#34D399;">-¥{r['amount']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("暂无记账记录，试试上面快速记账功能")

# ==================== Tab 3: 投研推荐 ====================
with tab3:
    st.markdown('<div class="section-title">📈 招商银行投研团队精选 · 低风险稳健产品</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    products = [
        {"name": "招银理财·稳健增利", "risk": "低风险", "yield": "年化 3.8%~4.2%", "desc": "适合大学生应急储蓄", "color": "#10B981"},
        {"name": "招银基金·固收+", "risk": "中低风险", "yield": "年化 5.1%~6.5%", "desc": "适合中长期规划", "color": "#F59E0B"},
        {"name": "招银债券·安享", "risk": "低风险", "yield": "年化 3.5%~3.9%", "desc": "保本优先，适合新手", "color": "#06B6D4"},
    ]
    
    for i, p in enumerate(products):
        with [col1, col2, col3][i]:
            st.markdown(f"""
            <div class="product-card">
                <div style="font-weight:800; font-size:1.15rem; margin-bottom:8px;">{p['name']}</div>
                <div style="display:flex; gap:8px; margin-bottom:12px;">
                    <span style="background:{p['color']}; color:white; padding:2px 10px; border-radius:9999px; font-size:12px;">{p['risk']}</span>
                </div>
                <div style="font-size:1.35rem; font-weight:800; color:#34D399; margin-bottom:4px;">{p['yield']}</div>
                <div style="font-size:13px; color:#94A3B8; margin-bottom:16px;">{p['desc']}</div>
                <button style="width:100%; background:#1E40AF; color:white; border:none; padding:10px; border-radius:9999px; font-weight:700;">立即认购</button>
            </div>
            """, unsafe_allow_html=True)

# ==================== Tab 4: 成长树 ====================
with tab4:
    st.markdown('<div class="section-title">🌳 我的财务健康树 · 招商银行专属</div>', unsafe_allow_html=True)
    
    progress = st.slider("当前进度", 0, 100, 34, step=2)
    st.progress(progress / 100)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("已存金额", f"¥{int(2200*progress/100)}", f"+{int(2200*progress/100*0.08)}")
    col2.metric("连续记账", "19天", "新高")
    col3.metric("本月储蓄率", "42%", "+8%")

# ==================== 底部二维码 ====================
st.divider()
st.markdown("### 📱 扫码体验完整版")

col1, col2 = st.columns([1, 2])
with col1:
    if st.button("生成体验二维码", use_container_width=True):
        url = "https://caiban-ai-cmb.streamlit.app"
        qr = qrcode.QRCode(box_size=12, border=2)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#1E293B", back_color="#F8FAFC")
        buf = BytesIO()
        img.save(buf, format="PNG")
        st.image(buf.getvalue(), width=220)
        st.caption("扫码体验招商银行版财伴AI")

with col2:
    st.markdown("""
    **招商银行 × 财伴AI 核心亮点**<br>
    • 实时机票酒店价格查询（招商银行合作平台）<br>
    • 个性化旅行基金 + 自动记账同步一卡通<br>
    • 投研团队精选低风险产品（稳健增利 / 固收+ / 安享债券）<br>
    • 适合大学生的活泼界面 + 高对比度字体
    """)

st.caption("© 2026 招商银行 × 财伴AI · 仅供演示 · 真实产品以招商银行官方为准")
