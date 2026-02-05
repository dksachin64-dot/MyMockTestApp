import streamlit as st
import time
import random

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="QUANTUM MOCK TEST", layout="wide", page_icon="🧬")

# --- 2. ADVANCED UI (DARK SCI-FI THEME) ---
st.markdown("""
<style>
    /* Main Background */
    .stApp { background-color: #050a14; color: #e2e8f0; font-family: 'Segoe UI', sans-serif; }

    /* Header Design */
    .hero-box {
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
        padding: 3px; border-radius: 15px;
        box-shadow: 0 0 20px rgba(0, 114, 255, 0.4);
        margin-bottom: 30px;
    }
    .hero-inner {
        background: #0f172a; padding: 30px; border-radius: 12px; text-align: center;
    }
    .hero-title {
        background: -webkit-linear-gradient(#00c6ff, #0072ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 900; font-size: 40px; margin: 0;
    }

    /* Question Card */
    .q-card {
        background: #1e293b; border: 1px solid #334155;
        padding: 20px; border-radius: 10px; margin-bottom: 15px;
        border-left: 5px solid #00c6ff;
    }

    /* Button Fix (Black Text on White) */
    .stButton > button {
        color: #000000 !important;
        background-color: #ffffff !important;
        border: 2px solid #00c6ff !important;
        font-weight: bold !important;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #00c6ff !important; color: white !important;
    }
    
    /* Result Badges */
    .correct { background: #064e3b; color: #34d399; padding: 10px; border-radius: 8px; border: 1px solid #10b981; }
    .wrong { background: #450a0a; color: #fca5a5; padding: 10px; border-radius: 8px; border: 1px solid #ef4444; }

</style>
""", unsafe_allow_html=True)

# --- 3. DATABASE (OFFLINE - NO CRASH) ---
QUESTIONS_DB = {
    "Physics": [
        {"q": "Dimensional formula of Planck's Constant?", "opt": ["ML2T-1", "MLT-1", "ML2T-2", "M0L0T0"], "ans": "ML2T-1", "exp": "E = hv => h = E/v. Dimensions are [ML2T-2] / [T-1] = [ML2T-1]"},
        {"q": "Two parallel wires carrying current in same direction:", "opt": ["Attract", "Repel", "No Force", "Rotate"], "ans": "Attract", "exp": "Magnetic field interaction causes attraction."},
        {"q": "Unit of Magnetic Flux?", "opt": ["Tesla", "Weber", "Gauss", "Ampere"], "ans": "Weber", "exp": "Tesla is for field, Weber is for flux."},
        {"q": "Escape velocity from Earth?", "opt": ["11.2 km/s", "9.8 km/s", "15 km/s", "7.9 km/s"], "ans": "11.2 km/s", "exp": "v = sqrt(2gR)."},
        {"q": "Mirage is caused by?", "opt": ["TIR", "Diffraction", "Refraction", "Polarization"], "ans": "TIR", "exp": "Total Internal Reflection due to atmospheric layers."}
    ],
    "Chemistry": [
        {"q": "Hybridization of Carbon in Diamond?", "opt": ["sp3", "sp2", "sp", "dsp2"], "ans": "sp3", "exp": "Tetrahedral structure."},
        {"q": "Shape of Ammonia (NH3)?", "opt": ["Pyramidal", "Tetrahedral", "Linear", "Bent"], "ans": "Pyramidal", "exp": "Due to one lone pair."},
        {"q": "Which is known as King of Chemicals?", "opt": ["H2SO4", "HCl", "HNO3", "NaOH"], "ans": "H2SO4", "exp": "Sulphuric Acid is used in many industries."},
        {"q": "pH of pure water at 25°C?", "opt": ["7", "0", "14", "1"], "ans": "7", "exp": "Neutral solution."},
        {"q": "Ore of Aluminum?", "opt": ["Bauxite", "Haematite", "Galena", "Cinnabar"], "ans": "Bauxite", "exp": "Al2O3.2H2O"}
    ]
}

# --- 4. SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'subject' not in st.session_state: st.session_state.subject = ""
if 'responses' not in st.session_state: st.session_state.responses = {}

# --- 5. HOME PAGE ---
if st.session_state.page == "home":
    st.markdown("""
    <div class="hero-box">
        <div class="hero-inner">
            <h1 class="hero-title">QUANTUM MOCK TEST</h1>
            <p>Select Subject to Start Exam Engine</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("⚛️ PHYSICS TEST"):
            st.session_state.subject = "Physics"
            st.session_state.responses = {}
            st.session_state.page = "exam"
            st.rerun()
    with c2:
        if st.button("🧪 CHEMISTRY TEST"):
            st.session_state.subject = "Chemistry"
            st.session_state.responses = {}
            st.session_state.page = "exam"
            st.rerun()

# --- 6. EXAM PAGE ---
elif st.session_state.page == "exam":
    sub = st.session_state.subject
    data = QUESTIONS_DB[sub]
    
    st.markdown(f"### 📝 {sub} Mock Test (Live)")
    st.progress(len(st.session_state.responses)/len(data))
    
    for i, q in enumerate(data):
        st.markdown(f'<div class="q-card"><b>Q{i+1}: {q["q"]}</b></div>', unsafe_allow_html=True)
        val = st.radio(f"Select Answer {i+1}", q['opt'], key=f"q{i}", index=None)
        if val: st.session_state.responses[i] = val
        st.write("")
        
    c1, c2 = st.columns([1, 2])
    with c1:
        if st.button("❌ Cancel"):
            st.session_state.page = "home"
            st.rerun()
    with c2:
        if st.button("✅ SUBMIT PAPER", type="primary"):
            st.session_state.page = "result"
            st.rerun()

# --- 7. RESULT PAGE ---
elif st.session_state.page == "result":
    sub = st.session_state.subject
    data = QUESTIONS_DB[sub]
    score = sum([1 for i, q in enumerate(data) if st.session_state.responses.get(i) == q['ans']])
    
    st.markdown(f"""
    <div class="hero-box">
        <h2 style="text-align:center; color:white;">SCORE: {score} / {len(data)}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    for i, q in enumerate(data):
        user_ans = st.session_state.responses.get(i, "Skipped")
        is_correct = user_ans == q['ans']
        css = "correct" if is_correct else "wrong"
        status = "✅ Correct" if is_correct else "❌ Wrong"
        
        st.markdown(f"""
        <div class="{css}" style="margin-bottom:10px;">
            <b>Q{i+1}: {q['q']}</b><br>
            Your Ans: {user_ans} | Correct: <b>{q['ans']}</b><br>
            <i>💡 Explanation: {q['exp']}</i>
        </div>
        """, unsafe_allow_html=True)
        
    if st.button("🔄 New Test"):
        st.session_state.page = "home"
        st.rerun()
