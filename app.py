import streamlit as st
import google.generativeai as genai
import json
import time
import random

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="QUANTUM ENGINE v4.0", layout="wide", page_icon="⚡")

# API Key
GOOGLE_API_KEY = "AIzaSyALMoUhT8s7GYOHexDYrhnMNVT1xqQ4bgE"
genai.configure(api_key=GOOGLE_API_KEY)

# --- 2. ADVANCED CSS (ANIMATIONS & HIERARCHY) ---
st.markdown("""
<style>
    /* 1. Global Deep Dark Theme */
    .stApp {
        background-color: #050a14; /* Void Black */
        color: #e2e8f0;
        font-family: 'Segoe UI', Roboto, sans-serif;
    }

    /* 2. ANIMATIONS (The "Alive" Feel) */
    @keyframes blink {
        0% { opacity: 1; text-shadow: 0 0 10px #4ade80; }
        50% { opacity: 0.4; text-shadow: none; }
        100% { opacity: 1; text-shadow: 0 0 10px #4ade80; }
    }
    .status-dot {
        color: #4ade80;
        font-weight: bold;
        animation: blink 2s infinite;
    }
    
    @keyframes pulse-border {
        0% { box-shadow: 0 0 0 0 rgba(56, 189, 248, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(56, 189, 248, 0); }
        100% { box-shadow: 0 0 0 0 rgba(56, 189, 248, 0); }
    }
    
    @keyframes timer-deplete {
        from { width: 100%; }
        to { width: 0%; }
    }

    /* 3. AI Status Panel (Top) */
    .ai-dashboard-header {
        display: flex;
        justify-content: space-between;
        background: #0f172a;
        border-bottom: 1px solid #1e293b;
        padding: 8px 20px;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        color: #64748b;
        letter-spacing: 1px;
    }
    .metric-value { color: #f8fafc; font-weight: bold; }

    /* 4. AI Coach Insight (Split View) */
    .coach-panel {
        background: rgba(15, 23, 42, 0.6);
        border-left: 4px solid #f59e0b;
        padding: 20px;
        border-radius: 4px;
        margin-bottom: 20px;
    }
    .coach-diagnosis { color: #f59e0b; font-weight: 700; font-size: 14px; margin-bottom: 5px; }
    .coach-action { color: #38bdf8; font-weight: 600; font-size: 15px; display: flex; align-items: center; gap: 10px; }

    /* 5. PRIMARY CTA BUTTON (The "Launch" Button) */
    /* Targeting the Primary Button specifically */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(45deg, #0ea5e9, #2563eb) !important;
        color: white !important;
        border: none !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        padding: 20px 0 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        animation: pulse-border 2s infinite;
        transition: transform 0.2s;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: scale(1.02);
    }

    /* 6. SECONDARY BUTTONS (Tools) */
    div.stButton > button[kind="secondary"] {
        background: #0f172a !important;
        border: 1px solid #334155 !important;
        color: #94a3b8 !important;
        font-size: 14px !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        border-color: #38bdf8 !important;
        color: #38bdf8 !important;
    }

    /* 7. LIVE DEMO CARD (With CSS Timer) */
    .demo-container {
        border: 1px dashed #334155;
        padding: 20px;
        background: #0b0f19;
        position: relative;
    }
    .timer-bar {
        height: 4px;
        background: #ef4444;
        width: 100%;
        animation: timer-deplete 15s linear forwards; /* CSS Timer Trick */
        margin-bottom: 15px;
    }
    
    /* 8. FOOTER STRIP */
    .footer-strip {
        position: fixed;
        bottom: 0; left: 0; width: 100%;
        background: #0f172a;
        border-top: 1px solid #1e293b;
        padding: 5px 20px;
        display: flex;
        justify-content: space-between;
        font-size: 11px;
        color: #475569;
        z-index: 999;
    }

</style>
""", unsafe_allow_html=True)

# --- 3. SESSION & LOGIC ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'user_xp' not in st.session_state: st.session_state.user_xp = 42

# --- 4. TOP STATUS BAR (Dynamic) ---
st.markdown("""
<div class="ai-dashboard-header">
    <span>SYSTEM STATUS: <span class="status-dot">● ONLINE</span></span>
    <span>ENGINE: <span class="metric-value">QUANTUM v4.0</span></span>
    <span>LATENCY: <span class="metric-value">14ms</span></span>
    <span>USER MODEL: <span class="metric-value">DYNAMIC</span></span>
</div>
""", unsafe_allow_html=True)

# --- 5. MAIN DASHBOARD ---
if st.session_state.page == "home":
    
    # HERO HEADER
    st.markdown("<h1 style='text-align: center; margin-top: 20px; font-size: 48px;'>QUANTUM ENGINE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 16px; margin-bottom: 40px;'>⚠️ WARNING: This system penalizes guesswork. Accuracy > Speed.</p>", unsafe_allow_html=True)

    # TWO COLUMNS: INTELLIGENCE vs ACTION
    col_intel, col_action = st.columns([1.5, 1])

    with col_intel:
        st.markdown("### 📡 INTELLIGENCE FEED")
        
        # 1. AI COACH INSIGHT (Reason + Action)
        st.markdown("""
        <div class="coach-panel">
            <div class="coach-diagnosis">⚠️ ANOMALY DETECTED: ORGANIC CHEMISTRY</div>
            <p style="font-size: 13px; color: #cbd5e1; margin-bottom: 15px;">
                Your reaction mechanism accuracy (34%) is deviating from the Topper Benchmark (85%).
                The system detects confusion in <b>Nucleophilic Substitution</b>.
            </p>
            <div class="coach-action">
                <span>➤ RECOMMENDED PROTOCOL:</span>
                <span style="background: rgba(56, 189, 248, 0.1); padding: 2px 8px; border-radius: 4px;">Run Diagnostic Test #OC-2</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 2. LIVE DEMO QUESTION (Psychological Proof)
        st.markdown("### 🔥 LIVE CALIBRATION (Sample)")
        st.markdown("""
        <div class="demo-container">
            <div class="timer-bar"></div>
            <p style="color: #ef4444; font-size: 10px; font-weight: bold; letter-spacing: 1px;">HIGH STAKES QUESTION • TIME PRESSURE ON</p>
            <p style="color: #e2e8f0; font-size: 15px; font-weight: 500;">
                <b>Q.</b> In a Young's double slit experiment, if the separation between slits is halved and distance to screen is doubled, the fringe width will be:
            </p>
            <div style="display: flex; gap: 10px; margin-top: 10px; opacity: 0.7;">
                <button style="background:none; border:1px solid #555; color:#aaa; padding:5px 15px;">A) Halved</button>
                <button style="background:none; border:1px solid #555; color:#aaa; padding:5px 15px;">B) Unchanged</button>
                <button style="background:none; border:1px solid #555; color:#aaa; padding:5px 15px;">C) Quadrupled</button>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_action:
        st.markdown("### ⚡ CONTROL DECK")
        
        # GAP
        st.write("")
        
        # PRIMARY CTA (Huge & Pulsing)
        if st.button("🚀 LAUNCH AI MOCK TEST", type="primary", use_container_width=True):
            st.session_state.page = "setup"
            st.rerun()
        
        st.markdown("<p style='text-align:center; font-size:11px; color:#475569; margin-top: 5px;'>Auto-configures difficulty based on history</p>", unsafe_allow_html=True)
        
        st.write("---") # Divider
        
        # SECONDARY TOOLS
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🩺 DIAGNOSTIC", type="secondary", use_container_width=True):
                st.toast("Running System Diagnostic...", icon="⚙️")
        with c2:
            if st.button("📊 WEAK AREAS", type="secondary", use_container_width=True):
                st.toast("Fetching Error Logs...", icon="📂")
                
        if st.button("🔮 PREDICT RANK & COLLEGE", type="secondary", use_container_width=True):
            st.toast("Calculating Probabilities...", icon="🎲")

# --- 6. FOOTER (Fixed) ---
st.markdown("""
<div class="footer-strip">
    <span>USER ID: <b>#IND-8821</b></span>
    <span>SESSION: <b>SECURE (TLS 1.3)</b></span>
    <span>DATABASE: <b>UPDATED 2 MINS AGO</b></span>
</div>
""", unsafe_allow_html=True)

# --- 7. SETUP PAGE (Dummy) ---
if st.session_state.page == "setup":
    st.markdown("### ⚙️ INITIALIZING EXAM ENVIRONMENT...")
    progress_text = "Calibrating Difficulty Matrix..."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    
    st.success("SYSTEM READY. RENDERING QUESTIONS.")
    
    if st.button("⬅️ ABORT MISSION"):
        st.session_state.page = "home"
        st.rerun()
        
