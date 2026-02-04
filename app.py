import streamlit as st
import google.generativeai as genai
import json
import time
import random

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="QUANTUM ENGINE v3.0", layout="wide", page_icon="⚡")

# API Key
GOOGLE_API_KEY = "AIzaSyALMoUhT8s7GYOHexDYrhnMNVT1xqQ4bgE"
genai.configure(api_key=GOOGLE_API_KEY)

# --- 2. ADVANCED UI SYSTEM (THE CONTROL CENTER) ---
st.markdown("""
<style>
    /* 1. Global Reset & Dark Theme */
    .stApp {
        background-color: #0b0f19; /* Ultra Dark Blue/Black */
        color: #e2e8f0;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* 2. Utility: Borders & Sharp Edges */
    .sharp-card {
        background: rgba(17, 24, 39, 0.7);
        border: 1px solid #334155;
        border-radius: 4px; /* Sharp edges */
        padding: 15px;
        margin-bottom: 10px;
    }
    
    /* 3. AI Status Panel (Top) */
    .ai-status-row {
        display: flex;
        justify-content: space-between;
        background: #0f172a;
        border-bottom: 2px solid #3b82f6;
        padding: 10px 20px;
        margin-bottom: 20px;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        color: #94a3b8;
    }
    .status-active { color: #4ade80; font-weight: bold; text-shadow: 0 0 5px rgba(74, 222, 128, 0.5); }
    .status-value { color: #f8fafc; font-weight: bold; }

    /* 4. AI Coach Message Box */
    .coach-box {
        border-left: 4px solid #f59e0b; /* Amber Alert */
        background: rgba(245, 158, 11, 0.1);
        padding: 15px;
        margin: 15px 0;
        font-size: 15px;
    }
    .coach-title { color: #f59e0b; font-weight: bold; display: flex; align-items: center; gap: 8px; }

    /* 5. Trust Strip (Badges) */
    .trust-strip {
        display: flex;
        gap: 15px;
        flex-wrap: wrap;
        margin-bottom: 20px;
    }
    .trust-badge {
        background: #1e293b;
        border: 1px solid #475569;
        color: #cbd5e1;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        display: flex;
        align-items: center;
        gap: 5px;
    }

    /* 6. ACTION BUTTONS (Sharp, Neon, High Tech) */
    .stButton > button {
        width: 100%;
        background-color: #0f172a !important; /* Dark Background */
        color: #38bdf8 !important; /* Neon Blue Text */
        border: 1px solid #38bdf8 !important; /* Neon Border */
        border-radius: 2px !important; /* Very Sharp */
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        padding: 15px 0 !important;
    }
    .stButton > button:hover {
        background-color: #38bdf8 !important;
        color: #0f172a !important; /* Black Text on Hover */
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.6);
    }
    
    /* 7. Live Demo Card */
    .demo-card {
        border: 1px dashed #ef4444; /* Red Dashed Border */
        background: rgba(239, 68, 68, 0.05);
        padding: 20px;
        position: relative;
    }
    .timer-badge {
        position: absolute;
        top: -10px;
        right: 20px;
        background: #ef4444;
        color: white;
        padding: 2px 10px;
        font-size: 12px;
        font-weight: bold;
        border-radius: 4px;
    }

    /* Text Hierarchy */
    h1 { font-weight: 800; letter-spacing: -1px; margin-bottom: 5px; }
    h3 { font-weight: 600; color: #e2e8f0; margin-top: 0; }
    p { font-weight: 300; color: #94a3b8; }
    
</style>
""", unsafe_allow_html=True)

# --- 3. BACKEND LOGIC (Mock) ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'user_level' not in st.session_state: st.session_state.user_level = 35 # % Progress

# --- 4. HEADER & CREDIBILITY ---
st.markdown("<h1>QUANTUM ENGINE <span style='font-size:18px; color:#38bdf8; vertical-align:middle;'>v3.2 AI-CORE</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='margin-bottom: 20px; border-bottom: 1px solid #334155; padding-bottom: 10px;'>Built for serious aspirants. Not for casual practice.</p>", unsafe_allow_html=True)

# --- 5. AI SYSTEM STATUS STRIP (Top Bar) ---
st.markdown("""
<div class="ai-status-row">
    <span>SYSTEM: <span class="status-active">ONLINE ●</span></span>
    <span>INTELLIGENCE: <span class="status-value">ADAPTIVE MODEL</span></span>
    <span>PREDICTION ACCURACY: <span class="status-value">94.2%</span></span>
    <span>LATENCY: <span class="status-value">12ms</span></span>
</div>
""", unsafe_allow_html=True)

# --- 6. MAIN DASHBOARD LAYOUT ---
if st.session_state.page == "home":
    
    # TRUST STRIP
    st.markdown("""
    <div class="trust-strip">
        <span class="trust-badge">🔒 NCERT Mapped</span>
        <span class="trust-badge">⚡ Real Exam Pattern</span>
        <span class="trust-badge">📉 Negative Marking ON</span>
        <span class="trust-badge">⏱️ Time-Pressure Sim</span>
    </div>
    """, unsafe_allow_html=True)

    # TWO COLUMN LAYOUT
    col_dash, col_action = st.columns([1.5, 1])

    with col_dash:
        # A. AI COACH
        st.markdown("""
        <div class="sharp-card">
            <div class="coach-box">
                <div class="coach-title">🤖 AI COACH INSIGHT</div>
                <p style="color: #cbd5e1; margin: 5px 0 0 0;">
                    "Your Physics <b>Optics</b> accuracy is below JEE Advanced benchmark (42%). 
                    <b>Diagnostic Test</b> is highly recommended to recalibrate your difficulty curve."
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # B. PROGRESS VISUALIZATION
        st.markdown("### 🧬 EVOLUTION TRACKER")
        progress = st.session_state.user_level
        st.progress(progress/100)
        
        # Custom Labels below progress
        c1, c2, c3 = st.columns(3)
        c1.caption("Foundation")
        c2.caption(f"Current: {progress}%")
        c3.caption("Exam Ready")

        # C. LIVE DEMO (High Stakes)
        st.write("")
        st.markdown("### 🔥 LIVE SAMPLE (HARD)")
        st.markdown("""
        <div class="demo-card">
            <div class="timer-badge">00:09</div>
            <p style="color:white; font-size: 14px;"><b>Q.</b> A block of mass m is placed on a wedge of mass M. The wedge is subjected to an acceleration 'a' such that the block remains stationary w.r.t the wedge. Find 'a'.</p>
            <div style="display:flex; gap:10px; margin-top:10px;">
                <span style="border:1px solid #555; padding:5px 10px; font-size:12px; color:#aaa;">A) g tan(θ)</span>
                <span style="border:1px solid #555; padding:5px 10px; font-size:12px; color:#aaa;">B) g cot(θ)</span>
                <span style="border:1px solid #555; padding:5px 10px; font-size:12px; color:#aaa;">C) g sin(θ)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_action:
        st.markdown("### ⚡ ACTION MODULES")
        
        # High Tech Buttons
        if st.button("🚀 LAUNCH AI MOCK TEST"):
            st.session_state.page = "setup"
            st.rerun()
            
        st.write("") # Gap
        
        if st.button("🩺 RUN DIAGNOSTIC TEST"):
            st.toast("Initializing Diagnostic Protocol...", icon="⚙️")
            
        st.write("") # Gap

        if st.button("📊 ANALYZE WEAK AREAS"):
            st.toast("Scanning Performance Data...", icon="🔍")
            
        st.write("") # Gap
        
        if st.button("🔮 PREDICT RANK"):
            st.toast("Calculating Probabilities...", icon="🎲")

        st.markdown("""
        <div style="margin-top: 30px; padding: 15px; border: 1px solid #1e293b; border-radius: 4px; background:#0f172a;">
            <p style="font-size:12px; color:#64748b; margin:0;">USER MODEL ID: <b>#XJ-9021</b></p>
            <p style="font-size:12px; color:#64748b; margin:0;">LAST SYNC: <b>JUST NOW</b></p>
        </div>
        """, unsafe_allow_html=True)

# --- 7. EXAM SETUP PAGE (Minimal Logic for Demo) ---
elif st.session_state.page == "setup":
    st.markdown("### ⚙️ INITIALIZING TEST ENVIRONMENT")
    st.info("Loading Neural Weights for Indian Exam Patterns...")
    
    # Just a dummy return button for now
    if st.button("⬅️ RETURN TO COMMAND CENTER"):
        st.session_state.page = "home"
        st.rerun()
        
