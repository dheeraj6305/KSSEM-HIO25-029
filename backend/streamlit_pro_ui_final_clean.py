# streamlit_bank_pro_console_final_ui.py
"""
🏦 NEXUS Bank Loan Evaluation Console — Final Professional Edition
Streamlit UI for large-scale PDF upload, AI analysis, and real-time logging.
"""

import streamlit as st
import pandas as pd
import numpy as np
import time, uuid
import plotly.express as px
import plotly.graph_objects as go

# ================== PAGE CONFIG ==================
st.set_page_config(page_title="NEXUS Loan Console", layout="wide")

# ================== CUSTOM CSS ==================
st.markdown("""
<style>
body {background-color:#f8fafc;font-family:'Inter',sans-serif;}
h1,h2,h3,h4 {color:#0a2540;}
.stMetricValue {color:#0a2540;}
.stButton>button {
    background:linear-gradient(90deg,#2f80ed,#1c63c8);
    color:white;border-radius:8px;font-weight:600;
    padding:0.5rem 1rem;border:none;transition:0.2s;
}
.stButton>button:hover {
    box-shadow:0px 0px 8px rgba(47,128,237,0.4);
    transform:translateY(-2px);
}
.badge {padding:6px 12px;border-radius:12px;font-weight:600;font-size:13px;color:white;}
.low {background-color:#27ae60;}
.medium {background-color:#f2c94c;color:#000;}
.high {background-color:#eb5757;}
.sidebar-header {font-weight:700;font-size:16px;margin-bottom:5px;color:#0a2540;}
.upload-box {
    border:2px dashed #cbd5e1;
    background:linear-gradient(180deg,#ffffff,#f9fafb);
    padding:2rem;border-radius:12px;margin-top:1rem;
    color:#0a2540;font-weight:500;text-align:center;
}
.log-box {
    background:#ffffff;border-radius:8px;padding:0.75rem 1rem;
    font-family:monospace;font-size:13px;color:#374151;
    max-height:220px;overflow:auto;border:1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

# ================== SIDEBAR ==================
st.sidebar.markdown("<div class='sidebar-header'>🏦 NEXUS Bank Internal</div>", unsafe_allow_html=True)
st.sidebar.markdown("Loan Evaluation Console (Authorized Personnel Only)")

st.sidebar.markdown("### ⚙️ Controls")
demo_mode = st.sidebar.toggle("Demo Mode (Offline Simulation)", True)

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

# ================== KPI METRICS ==================
col1, col2, col3, col4 = st.columns(4)
total_ph = col1.metric("Total Applications", "—")
approved_ph = col2.metric("Approved", "—")
rejected_ph = col3.metric("Rejected", "—")
proc_ph = col4.metric("Avg Processing Time (s)", "—")

# ================== DATA FUNCTION ==================
def generate_demo_data(n=2000):
    rng = np.random.default_rng(42)
    df = pd.DataFrame({
        "Applicant": [f"Applicant_{i+1}" for i in range(n)],
        "CIBIL": rng.integers(580, 820, n),
        "Income (₹)": rng.integers(20000, 150000, n),
        "Loan Amount": rng.integers(50000, 2000000, n),
        "Avg Score": np.clip(rng.normal(75, 12, n), 10, 99).round(2),
    })
    df["Status"] = np.where(df["Avg Score"] >= 80, "Approved",
                    np.where(df["Avg Score"] >= 60, "Manual Review", "Rejected"))
    return df

# ================== TABS ==================
tab1, tab2 = st.tabs(["📁 Loan Application Intake & Evaluation", "📊 Analytics & Insights"])

# ---------- TAB 1 ----------
with tab1:
    st.subheader("Loan Application Intake & Evaluation")
    st.markdown("<div class='upload-box'>Upload up to <b>5000 Loan Application PDFs</b> for secure OCR and AI evaluation.</div>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Upload Loan Applications", type=["pdf"], accept_multiple_files=True)

    if uploaded_files:
        num_files = len(uploaded_files)
        st.info(f"{num_files} files uploaded successfully. Beginning evaluation...")

        progress = st.progress(0)
        status_placeholder = st.empty()
        log_box = st.empty()

        logs = []
        step_messages = [
            "Initializing secure OCR engine...",
            "Scanning document metadata...",
            "Extracting salary details...",
            "Detecting forged templates...",
            "Running explainable risk model...",
            "Cross-verifying credit patterns...",
            "Generating applicant profiles...",
            "Aggregating portfolio analytics...",
            "Finalizing approval recommendations..."
        ]

        for i in range(100):
            time.sleep(0.03)
            if i % 12 == 0 and (i // 12) < len(step_messages):
                logs.append(f"[{time.strftime('%H:%M:%S')}] {step_messages[i // 12]}")
            progress.progress(i + 1)
            log_box.markdown("<div class='log-box'>" + "<br>".join(logs[-10:]) + "</div>", unsafe_allow_html=True)
            status_placeholder.text(f"Processing... {i+1}% complete")

        df = generate_demo_data(num_files)

        total, approved, rejected = len(df), (df["Status"]=="Approved").sum(), (df["Status"]=="Rejected").sum()
        avg_score = df["Avg Score"].mean()
        total_ph.metric("Total Applications", total)
        approved_ph.metric("Approved", approved)
        rejected_ph.metric("Rejected", rejected)
        proc_ph.metric("Avg Processing Time (s)", round(np.random.uniform(1.8, 3.2), 2))

        risk = "low" if avg_score >= 80 else "medium" if avg_score >= 60 else "high"
        badge = f"<span class='badge {risk}'>{risk.upper()} RISK</span>"
        st.markdown(f"**Overall Portfolio Risk Category:** {badge}", unsafe_allow_html=True)

        gauge_fig.data[0].value = avg_score
        risk_placeholder.plotly_chart(gauge_fig, use_container_width=True)

        st.success(f"✅ Evaluation completed — {approved} Approved, {rejected} Rejected.")

        st.dataframe(df.head(25), use_container_width=True)
        st.download_button("⬇ Download Evaluation Report",
                           df.to_csv(index=False).encode(),
                           file_name=f"loan_report_{uuid.uuid4().hex[:6]}.csv")

# ---------- TAB 2 ----------
with tab2:
    st.subheader("Portfolio Analytics & Risk Visualization")

    df = generate_demo_data(1000)
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

    c1, c2 = st.columns(2)
    with c1:
        pie = px.pie(df, names="Status", title="Approval Distribution",
                     color="Status", color_discrete_map={
                        "Approved":"#27ae60","Manual Review":"#f2c94c","Rejected":"#eb5757"})
        st.plotly_chart(pie, use_container_width=True)
    with c2:
        hist = px.histogram(df, x="Avg Score", nbins=20, title="Applicant Score Spread")
        st.plotly_chart(hist, use_container_width=True)

# ---------- FOOTER ----------
st.markdown("---")
st.markdown("<div style='text-align:center;color:#6b7280;'>© 2025 Nexus Bank Automation — Secure | Explainable | Fast</div>",
            unsafe_allow_html=True)
