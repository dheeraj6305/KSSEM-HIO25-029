# streamlit_pro_ui_final_clean.py
"""
🏦 NEXUS Loan Analyzer — Professional Banker Dashboard (Final Refined Edition)
Clean and realistic UI for bankers without batch upload or agent pipeline clutter.
"""

import streamlit as st
import pandas as pd
import numpy as np
import time, uuid
import plotly.express as px
import plotly.graph_objects as go

# ================== CONFIG ==================
st.set_page_config(page_title="NEXUS Loan Analyzer", layout="wide")

# ================== CUSTOM CSS ==================
st.markdown("""
<style>
body {background-color:#f8fafc;font-family:'Inter',sans-serif;}
h1,h2,h3,h4 {color:#0a2540;}
.stMetricValue {color:#0a2540;}
.stButton>button {
    background-color:#2f80ed;color:white;border-radius:8px;
    font-weight:600;padding:0.5rem 1rem;border:none;
}
.stButton>button:hover {background-color:#1c63c8;}
.badge {padding:6px 12px;border-radius:12px;font-weight:600;font-size:13px;color:white;}
.low {background-color:#27ae60;}
.medium {background-color:#f2c94c;color:#000;}
.high {background-color:#eb5757;}
.sidebar-gauge {background-color:white;padding:10px;border-radius:10px;box-shadow:0px 2px 6px rgba(0,0,0,0.1);}
</style>
""", unsafe_allow_html=True)

# ================== SIDEBAR ==================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2331/2331953.png", width=70)
st.sidebar.markdown("### ⚙️ Controls")
demo_mode = st.sidebar.toggle("Demo Mode (offline)", True)

# Sidebar Risk Gauge (live widget)
st.sidebar.markdown("### 📊 Portfolio Risk Gauge")
risk_placeholder = st.sidebar.empty()
gauge_fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=0,
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': "#2f80ed"},
        'steps': [
            {'range': [0, 60], 'color': '#fdecea'},
            {'range': [60, 80], 'color': '#fff4d6'},
            {'range': [80, 100], 'color': '#e9f7ef'}
        ]
    },
    number={'suffix': " /100"},
))
gauge_fig.update_layout(height=230, margin=dict(t=10, b=10, l=10, r=10))
risk_placeholder.plotly_chart(gauge_fig, use_container_width=True)

# ================== HEADER ==================
st.markdown("""
<div style="background-color:#0a2540;color:white;padding:1rem 2rem;border-radius:12px;
display:flex;justify-content:space-between;align-items:center;">
  <div style="font-size:24px;font-weight:700;">💼 NEXUS Loan Evaluation Dashboard</div>
  <div style="font-size:14px;opacity:0.8;">AI-Powered Risk Intelligence for Bankers</div>
</div>
""", unsafe_allow_html=True)
st.write("")

# ================== KPI CARDS ==================
col1, col2, col3, col4 = st.columns(4)
total_ph = col1.metric("Total Applications", "—")
approved_ph = col2.metric("Approved", "—")
rejected_ph = col3.metric("Rejected", "—")
proc_ph = col4.metric("Avg Processing Time (s)", "—")

# ================== DEMO DATA GEN ==================
def generate_demo_data(n=200):
    rng = np.random.default_rng(42)
    df = pd.DataFrame({
        "Applicant": [f"Employee_{i+1}" for i in range(n)],
        "CIBIL": rng.integers(580, 820, n),
        "Income (₹)": rng.integers(20000, 150000, n),
        "Loan Amount": rng.integers(50000, 2000000, n),
        "Avg Score": np.clip(rng.normal(75, 12, n), 10, 99).round(2),
    })
    df["Status"] = np.where(df["Avg Score"] >= 80, "Approved",
                    np.where(df["Avg Score"] >= 60, "Manual Review", "Rejected"))
    return df

# ================== TABS ==================
tab1, tab2 = st.tabs(["👤 Single Applicant", "📈 Insights"])

# ---------- TAB 1: SINGLE ----------
with tab1:
    st.subheader("Single Applicant Evaluation")
    name = st.text_input("Applicant Name")
    amount = st.number_input("Requested Loan (₹)", value=100000)
    analyze = st.button("🔍 Evaluate", use_container_width=True)

    if analyze:
        with st.spinner("Processing applicant securely..."):
            for _ in range(60):
                time.sleep(0.02)
        score = np.random.randint(45, 99)
        risk = "Low" if score >= 80 else "Medium" if score >= 60 else "High"
        badge = f"<span class='badge {risk.lower()}'>{risk.upper()} RISK</span>"
        st.success(f"✅ {name or 'Applicant'} evaluated successfully!")
        st.markdown(f"**Score:** {score}/100 — {badge}", unsafe_allow_html=True)

# ---------- TAB 2: INSIGHTS ----------
with tab2:
    st.subheader("Portfolio Insights")
    df = generate_demo_data(500)

    total, approved, rejected = len(df), (df["Status"]=="Approved").sum(), (df["Status"]=="Rejected").sum()
    avg_score = df["Avg Score"].mean()
    proc_time = round(np.random.uniform(1.2, 3.6), 2)
    total_ph.metric("Total Applications", total)
    approved_ph.metric("Approved", approved)
    rejected_ph.metric("Rejected", rejected)
    proc_ph.metric("Avg Processing Time (s)", proc_time)

    risk = "low" if avg_score >= 80 else "medium" if avg_score >= 60 else "high"
    badge = f"<span class='badge {risk}'>{risk.upper()} RISK</span>"
    st.markdown(f"**Portfolio Risk Level:** {badge}", unsafe_allow_html=True)

    # Update sidebar gauge dynamically
    gauge_fig.data[0].value = avg_score
    risk_placeholder.plotly_chart(gauge_fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        pie = px.pie(df, names="Status", title="Approval Ratio",
                     color="Status", color_discrete_map={
                        "Approved":"#27ae60","Manual Review":"#f2c94c","Rejected":"#eb5757"})
        st.plotly_chart(pie, use_container_width=True)
    with c2:
        line = px.line(x=np.arange(1,15), y=np.random.randint(100,500,14),
                       markers=True, title="Loan Processing Volume (Last 14 Days)")
        st.plotly_chart(line, use_container_width=True)

    st.markdown("### 🏆 Top Candidates")
    st.dataframe(df.sort_values("Avg Score", ascending=False).reset_index(drop=True), use_container_width=True)
    st.download_button("⬇ Download Shortlisted CSV",
                       df.to_csv(index=False).encode(),
                       file_name=f"shortlisted_{uuid.uuid4().hex[:6]}.csv")

# ---------- FOOTER ----------
st.markdown("---")
st.markdown("<div style='text-align:center;color:#6b7280;'>© 2025 Nexus Bank Automation — Secure | Explainable | Fast</div>",
            unsafe_allow_html=True)
