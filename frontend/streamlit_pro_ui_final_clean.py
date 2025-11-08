import streamlit as st
import pandas as pd
import requests

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="NEXUS Loan Console", layout="wide")

# -------------------- COLORS --------------------
THEME = {
    "bg": "#F8FAFC",
    "text": "#1E293B",
    "card": "#FFFFFF",
    "accent": "#2563EB",
    "accent2": "#38BDF8"
}

# -------------------- STYLES --------------------
st.markdown(f"""
<style>
body {{
    background-color: {THEME['bg']};
    color: {THEME['text']};
    font-family: 'Inter', sans-serif;
}}
.main-header {{
    background: linear-gradient(90deg, {THEME['accent']}, {THEME['accent2']});
    color: white;
    padding: 1rem 2rem;
    border-radius: 12px;
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    text-align: center;
}}
.metric-card {{
    background-color: {THEME['card']};
    border-radius: 14px;
    padding: 1.2rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    text-align: center;
    border-top: 4px solid {THEME['accent']};
    transition: all 0.2s ease-in-out;
    height: 120px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}
.metric-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 6px 10px rgba(0,0,0,0.08);
}}
.metric-title {{
    font-size: 1rem;
    font-weight: 600;
    color: {THEME['text']};
    opacity: 0.8;
}}
.metric-value {{
    font-size: 1.8rem;
    font-weight: 700;
    color: {THEME['accent']};
    margin-top: 0.3rem;
}}
.upload-box {{
    background-color: {THEME['card']};
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    text-align: center;
    border: 2px dashed {THEME['accent2']};
    margin-bottom: 1.2rem;
}}
.upload-box:hover {{
    border-color: {THEME['accent']};
    background-color: #EFF6FF;
}}
</style>
""", unsafe_allow_html=True)

# -------------------- SIDEBAR --------------------
# Added a small banking emoji logo at the top
st.sidebar.markdown("<h1 style='text-align:center; font-size:48px;'>🏦</h1>", unsafe_allow_html=True)
st.sidebar.markdown("## 💼 NEXUS Bank Officer Portal")
st.sidebar.markdown("---")
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=70)
st.sidebar.markdown("""
**Name:** Monika B  
**Role:** Senior Loan Officer  
**Branch:** Bangalore HQ  
""")
st.sidebar.markdown("---")
st.sidebar.button("🚪 Logout")

# -------------------- HEADER --------------------
st.markdown("<div class='main-header'>🏦 NEXUS Loan Evaluation Dashboard</div>", unsafe_allow_html=True)

# -------------------- INITIAL DATA --------------------
if "loan_data" not in st.session_state:
    st.session_state.loan_data = pd.DataFrame(columns=["file", "salary", "confidence", "decision", "reason"])
if "filter_status" not in st.session_state:
    st.session_state.filter_status = "All"

# -------------------- KPI BOXES --------------------
col1, col2, col3, col4 = st.columns([1, 1, 1, 1], gap="medium")

total_apps = len(st.session_state.loan_data)
approved_apps = len(st.session_state.loan_data[st.session_state.loan_data["decision"] == "Approved"])
rejected_apps = len(st.session_state.loan_data[st.session_state.loan_data["decision"] == "Rejected"])
avg_score = st.session_state.loan_data["confidence"].mean() * 100 if not st.session_state.loan_data.empty else 0

# All perfectly aligned same height and width
with col1:
    if st.button("👥 Total Applications", use_container_width=True):
        st.session_state.filter_status = "All"
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Total Applications</div><div class='metric-value'>{total_apps}</div></div>", unsafe_allow_html=True)

with col2:
    if st.button("✅ Approved", use_container_width=True):
        st.session_state.filter_status = "Approved"
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Approved</div><div class='metric-value'>{approved_apps}</div></div>", unsafe_allow_html=True)

with col3:
    if st.button("❌ Rejected", use_container_width=True):
        st.session_state.filter_status = "Rejected"
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Rejected</div><div class='metric-value'>{rejected_apps}</div></div>", unsafe_allow_html=True)

with col4:
    if st.button("⏳ Average Score", use_container_width=True):
        st.session_state.filter_status = "Average Score"
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Average Score</div><div class='metric-value'>{avg_score:.1f}</div></div>", unsafe_allow_html=True)

# -------------------- FILE UPLOAD --------------------
st.markdown("### 📤 Upload Payslips for Evaluation")
st.markdown("<div class='upload-box'>", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Drag and drop payslips here or browse files",
    type=["pdf", "jpg", "jpeg", "png"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_files:
    st.info("⏳ Evaluating uploaded files...")
    files = [("files", (file.name, file.getvalue(), file.type)) for file in uploaded_files]
    try:
        response = requests.post("http://127.0.0.1:8000/process_payslips", files=files)
        if response.status_code == 200:
            data = response.json()
            results = pd.DataFrame(data["results"])
            st.session_state.loan_data = results
            st.success(f"✅ Processed {len(results)} payslips successfully!")
        else:
            st.error("❌ Failed to process files. Check backend logs.")
    except Exception as e:
        st.error(f"⚠️ Backend not reachable: {e}")

# -------------------- FILTERED TABLE --------------------
df = st.session_state.loan_data

if st.session_state.filter_status == "Approved":
    filtered_df = df[df["decision"] == "Approved"]
    st.success(f"Showing all **Approved** applicants ({len(filtered_df)})")
elif st.session_state.filter_status == "Rejected":
    filtered_df = df[df["decision"] == "Rejected"]
    st.error(f"Showing all **Rejected** applicants ({len(filtered_df)})")
else:
    filtered_df = df
    if not df.empty:
        st.info(f"Showing **All Applications** ({len(filtered_df)})")

if not filtered_df.empty:
    st.markdown("### 📋 Evaluation Results")
    st.dataframe(filtered_df, use_container_width=True, height=480)

# -------------------- FOOTER --------------------
st.markdown("---")
st.markdown(f"<div style='text-align:center; color:{THEME['text']}; opacity:0.7;'>© 2025 Nexus Bank • Loan Evaluation Console</div>", unsafe_allow_html=True)
