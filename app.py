import streamlit as st
import time
import qrcode
from io import BytesIO

st.set_page_config(page_title="财伴AI · 招商银行", page_icon="💎", layout="wide")

# 明亮活泼 + 高对比度
st.markdown("""
<style>
    .stApp { background: linear-gradient(180deg, #F0F9FF 0%, #E0F2FE 100%); color: #0F172A; }
    .section-title { font-size: 1.45rem; font-weight: 900; color: #0F172A; margin-bottom: 1rem; border-bottom: 3px solid #06B6D4; padding-bottom: 8px; }
    .stButton>button { background: linear-gradient(90deg, #06B6D4, #F59E0B); color: white; border: none; border-radius: 9999px; padding: 0.75rem 2.2rem; font-weight: 800; font-size: 1.08rem; }
    .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 15px 20px -5px rgb(245 158 11 / 0.3); }
    .card { background: white; border-radius: 16px; padding: 1.4rem; box-shadow: 0 8px 12px -2px rgb(0 0 0 / 0.1); border: 1px solid #E2E8F0; }
    .metric { font-size: 2rem; font-weight: 900; color: #0EA5E9; }
    .highlight { color: #F59E0B; font-weight: 800; }
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

# 正确顺序：消费记账 → 愿望共创器 → 投研推荐 → 成长树
tab1, tab2, tab3, tab4 = st.tabs(["📝 消费记账", "🌟 愿望共创器", "📈 投研推荐", "🌳 成长树"])

# ==================== Tab 1: 消费记账（入口） ====================
with tab1:
    st.markdown('<div class="section-title">📝 消费记账 · 发现你的闲钱</div>', unsafe_allow_html=True)
    st.caption("先记账 → 发现自己有闲钱 → 再去理财定目标")
    
    col1, col2 = st.columns([1, 1.3])
    
    with col1:
        st.markdown("**快速记账**")
        amount = st.number_input("金额（元）", min_value=1.0, value=38.5, step=0.5)
        category = st.selectbox("分类", ["餐饮", "交通", "娱乐", "学习", "购物", "其他"])
        note = st.text_input("备注", placeholder="食堂 + 奶茶")
        
        if st.button("✅ 记账并同步招商银行一卡通", type="primary", use_container_width=True):
            if "records" not in st.session_state:
                st.session_state.records = []
            st.session_state.records.append({"amount": amount, "category": category, "note": note})
            st.success(f"已记 ¥{amount}，本月闲钱增加 ¥{amount}！")
    
    with col2:
        st.markdown("**本月消费明细**（招商银行同步）")
        if "records" in st.session_state and st.session_state.records:
            total = sum(r["amount"] for r in st.session_state.records)
            st.markdown(f"<div style='font-size:1.1rem; font-weight:700; color:#0EA5E9; margin-bottom:8px;'>本月已花 ¥{total}</div>", unsafe_allow_html=True)
            for r in st.session_state.records[-4:]:
                st.markdown(f"<div style='display:flex; justify-content:space-between; padding:4px 0; border-bottom:1px solid #E2E8F0;'><span>{r['category']} · {r['note']}</span><span style='color:#EF4444; font-weight:700;'>-¥{r['amount']}</span></div>", unsafe_allow_html=True)
        else:
            st.info("还没有记账记录，试试上面快速记账")

# ==================== Tab 2: 愿望共创器 ====================
with tab2:
    st.markdown('<div class="section-title">✨ 愿望共创器 + 实时价格查询</div>', unsafe_allow_html=True)
    st.caption("发现有闲钱后 → 设定旅行/目标基金")
    
    col1, col2 = st.columns([1.1, 1])
    with col1:
        dest = st.selectbox("目的地", ["云南昆明", "云南大理", "云南丽江", "四川成都", "海南三亚"])
        if st.button("🚀 实时查询 + 生成目标", type="primary", use_container_width=True):
            with st.spinner("招商银行合作平台实时查询中..."):
                time.sleep(0.6)
                totals = {"云南昆明": 2200, "云南大理": 2450, "云南丽江": 2680, "四川成都": 1980, "海南三亚": 3120}
                st.session_state.goal = {"name": f"{dest}旅行基金", "target": totals[dest], "monthly": 320}
                st.success("✅ 目标已生成！")
    
    with col2:
        if "goal" in st.session_state:
            g = st.session_state.goal
            st.markdown(f"""
            <div class="card">
                <div style="font-size:1.35rem; font-weight:900; margin-bottom:12px;">{g['name']}</div>
                <div style="display:flex; justify-content:space-between; align-items:end;">
                    <div><div style="font-size:12px; color:#64748B;">目标金额</div><div class="metric">¥{g['target']}</div></div>
                    <div style="text-align:right;"><div style="font-size:12px; color:#64748B;">每月定投</div><div style="font-size:1.7rem; font-weight:900; color:#F59E0B;">¥{g['monthly']}</div></div>
                </div>
                <div style="margin:14px 0; height:9px; background:#E2E8F0; border-radius:9999px; overflow:hidden;">
                    <div style="width:34%; height:100%; background:linear-gradient(90deg,#06B6D4,#F59E0B);"></div>
                </div>
                <div style="font-size:13px; color:#64748B;">已完成 34% · 预计6个月达成</div>
            </div>
            """, unsafe_allow_html=True)

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
    c1.metric("已存金额", f"¥{int(2200*progress/100)}", f"+{int(2200*progress/100*0.08)}")
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
