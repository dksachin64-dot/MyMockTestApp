import streamlit as st
import time

# --- 1. PAGE SETUP (Tab Name & Icon) ---
st.set_page_config(page_title="Quantum JEE/NEET", layout="wide", page_icon="🧬")

# --- 2. QUANTUM CSS (The Soul of the Design) ---
st.markdown("""
<style>
    /* 1. Main Dark Background */
    .stApp {
        background-color: #0f172a; /* Deep Space Blue */
        color: #e2e8f0;
    }

    /* 2. Neon Header (Glowing Effect) */
    .hero-box {
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
        padding: 4px; /* Thin Border */
        border-radius: 20px;
        box-shadow: 0 0 25px rgba(0, 114, 255, 0.5); /* Glow */
        margin-bottom: 40px;
    }
    .hero-inner {
        background: #1e293b; /* Inner Dark Box */
        padding: 40px;
        border-radius: 16px;
        text-align: center;
    }
    .hero-title {
        font-size: 60px;
        font-weight: 900;
        background: -webkit-linear-gradient(#00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 20px;
        margin-top: 10px;
    }

    /* 3. Stream Selection Cards (Glass Effect) */
    .stream-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid #334155;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        transition: transform 0.3s;
    }
    .stream-card:hover {
        transform: translateY(-5px);
        border-color: #00c6ff;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    
    /* 4. BUTTON FIX (Text Visibility) */
    /* Hum buttons ko zabardasti White/Black combination de rahe hain */
    .stButton > button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #00c6ff !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        padding: 10px 20px !important;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #00c6ff !important;
        color: #ffffff !important;
        box-shadow: 0 0 15px #00c6ff;
    }

    /* 5. Footer Design */
    .footer {
        text-align: center;
        color: #475569;
        margin-top: 50px;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. UI LAYOUT ---

# A. Header Section
st.markdown("""
<div class="hero-box">
    <div class="hero-inner">
        <h1 class="hero-title">QUANTUM ⚡ ENGINE</h1>
        <p class="hero-subtitle">Advanced AI Exam Simulation for India's Future Engineers & Doctors</p>
    </div>
</div>
""", unsafe_allow_html=True)

# B. Stream Selection (Layout)
st.markdown("### 🎯 Choose Your Target")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="stream-card">
        <h2 style="color:#22c55e;">🩺 NEET (Medical)</h2>
        <p>Biology | Physics | Chemistry</p>
        <p style="font-size:12px; color:#64748b;">NCERT Deep Line Focus</p>
    </div>
    """, unsafe_allow_html=True)
    # Button (Sirf Design ke liye, abhi logic nahi)
    st.button("ENTER MEDICAL LAB 🧬", key="btn_neet")

with col2:
    st.markdown("""
    <div class="stream-card">
        <h2 style="color:#3b82f6;">⚙️ JEE MAINS</h2>
        <p>Maths | Physics | Chemistry</p>
        <p style="font-size:12px; color:#64748b;">Speed & Accuracy Focus</p>
    </div>
    """, unsafe_allow_html=True)
    st.button("ENTER ENGINEERING LAB ⚛️", key="btn_mains")

with col3:
    st.markdown("""
    <div class="stream-card">
        <h2 style="color:#ef4444;">🚀 JEE ADVANCED</h2>
        <p>High Level Concepts</p>
        <p style="font-size:12px; color:#64748b;">Multi-Concept Numerical Focus</p>
    </div>
    """, unsafe_allow_html=True)
    st.button("ENTER RESEARCH LAB ☢️", key="btn_adv")

# C. Features Showcase (Visual Only)
st.markdown("---")
st.markdown("### ⚡ System Capabilities")

f1, f2, f3, f4 = st.columns(4)
f1.info("🧠 **AI Logic**\nGenerates New Questions")
f2.success("📖 **NCERT Core**\nStrict Syllabus Match")
f3.warning("📊 **Deep Analytics**\nReal-time Feedback")
f4.error("🛡️ **Offline Mode**\nAnti-Crash Backup")

# Footer
st.markdown('<div class="footer">POWERED BY QUANTUM ARCHITECTURE • V2.0</div>', unsafe_allow_html=True)
