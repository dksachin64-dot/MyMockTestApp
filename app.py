import streamlit as st
import json
import time
import random

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="QUANTUM ENGINE PRO", layout="wide", page_icon="⚡")

# NOTE: API KEY HATA DI HAI TAAKI APP KABHI CRASH NA HO.
# Ye ab "Simulation Mode" mein chalega.

# --- 2. ADVANCED DATABASE (PRE-LOADED INTELLIGENCE) ---
# Ye database AI ki tarah act karega.
MOCK_DB = {
    "Physics": [
        {"q": "A projectile is fired at 30° to the horizontal. The vertical component of its velocity...", "opt": ["Increases", "Decreases then Increases", "Remains Constant", "Becomes Zero at Max Height"], "ans": "Becomes Zero at Max Height", "exp": "At maximum height, the vertical component of velocity (vy) becomes zero instantly."},
        {"q": "Two parallel wires carrying current in the same direction will:", "opt": ["Attract each other", "Repel each other", "No force", "Rotate"], "ans": "Attract each other", "exp": "Magnetic field lines interaction causes attraction (Ampere's Law)."},
        {"q": "Dimensional formula of Planck's Constant (h) is same as:", "opt": ["Force", "Energy", "Angular Momentum", "Power"], "ans": "Angular Momentum", "exp": "Both have dimensions [ML²T⁻¹]."},
        {"q": "In a p-n junction diode, the depletion layer width increases with:", "opt": ["Forward Bias", "Reverse Bias", "Doping", "Temperature"], "ans": "Reverse Bias", "exp": "Reverse bias pulls majority carriers away from the junction, widening the depletion layer."},
        {"q": "The core of a transformer is laminated to reduce:", "opt": ["Flux leakage", "Hysteresis loss", "Eddy current loss", "Copper loss"], "ans": "Eddy current loss", "exp": "Laminations increase resistance, reducing circulating eddy currents."}
    ],
    "Chemistry": [
        {"q": "Which of the following is paramagnetic?", "opt": ["N2", "O2", "H2", "He"], "ans": "O2", "exp": "According to MOT, O2 has two unpaired electrons in anti-bonding orbitals."},
        {"q": "Shape of XeF4 molecule is:", "opt": ["Tetrahedral", "Square Planar", "Octahedral", "See-saw"], "ans": "Square Planar", "exp": "sp³d² hybridization with 2 lone pairs giving square planar geometry."},
        {"q": "Hybridization of Carbon in Diamond is:", "opt": ["sp", "sp2", "sp3", "dsp2"], "ans": "sp3", "exp": "Each carbon is bonded to 4 other carbons tetrahedrally."},
        {"q": "Which is the strongest acid?", "opt": ["HF", "HCl", "HBr", "HI"], "ans": "HI", "exp": "Bond dissociation energy decreases down the group, making H release easier."},
        {"q": "Glucose on reaction with HI gives:", "opt": ["n-Hexane", "Gluconic Acid", "Saccharic Acid", "Ethanol"], "ans": "n-Hexane", "exp": "Reduction with HI/Red P gives straight chain alkane (n-Hexane)."}
    ],
    "Maths": [
        {"q": "If A is a skew-symmetric matrix of odd order, then |A| is:", "opt": ["0", "1", "-1", "Non-zero"], "ans": "0", "exp": "Determinant of an odd order skew-symmetric matrix is always zero."},
        {"q": "Value of lim(x->0) (sin x / x) is:", "opt": ["0", "1", "Infinity", "Does not exist"], "ans": "1", "exp": "Standard Limit Theorem."},
        {"q": "The slope of normal to the curve y = 2x² + 3 sin x at x = 0 is:", "opt": ["3", "1/3", "-3", "-1/3"], "ans": "-1/3", "exp": "dy/dx at 0 is 3. Slope of normal = -1/m = -1/3."},
        {"q": "Integration of e^x(tan x + sec²x) dx is:", "opt": ["e^x tan x", "e^x sec x", "e^x log x", "None"], "ans": "e^x tan x", "exp": "Using property ∫e^x(f(x)+f'(x))dx = e^x f(x)."},
        {"q": "Probability of getting a sum of 7 with two dice is:", "opt": ["1/6", "1/12", "5/36", "1/36"], "ans": "1/6", "exp": "Favorable cases: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) = 6. Total = 36."}
    ]
}

# --- 3. ADVANCED CSS (ANIMATIONS & VISUALS) ---
st.markdown("""
<style>
    /* Global Dark Theme */
    .stApp { background-color: #050a14; color: #e2e8f0; font-family: 'Segoe UI', Roboto, sans-serif; }

    /* Animations */
    @keyframes blink { 0% { opacity: 1; text-shadow: 0 0 10px #4ade80; } 50% { opacity: 0.4; } 100% { opacity: 1; text-shadow: 0 0 10px #4ade80; } }
    .status-dot { color: #4ade80; font-weight: bold; animation: blink 2s infinite; }
    
    @keyframes pulse-border { 0% { box-shadow: 0 0 0 0 rgba(56, 189, 248, 0.7); } 70% { box-shadow: 0 0 0 10px rgba(56, 189, 248, 0); } 100% { box-shadow: 0 0 0 0 rgba(56, 189, 248, 0); } }
    
    @keyframes timer-run { from { width: 100%; } to { width: 0%; } }

    /* Top Dashboard */
    .ai-header { display: flex; justify-content: space-between; background: #0f172a; border-bottom: 1px solid #1e293b; padding: 10px 20px; font-family: 'Courier New', monospace; font-size: 13px; color: #64748b; }
    
    /* Coach Panel */
    .coach-panel { background: rgba(15, 23, 42, 0.8); border-left: 4px solid #f59e0b; padding: 20px; border-radius: 4px; margin-bottom: 20px; border: 1px solid #1e293b; }
    
    /* Primary Action Button */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(45deg, #0ea5e9, #2563eb) !important; color: white !important; border: none !important;
        font-size: 18px !important; font-weight: 800 !important; padding: 20px 0 !important;
        text-transform: uppercase; letter-spacing: 2px; animation: pulse-border 2s infinite; width: 100%;
    }
    
    /* Live Demo */
    .demo-box { border: 1px dashed #334155; padding: 20px; background: #0b0f19; position: relative; margin-top: 20px; }
    .timer-line { height: 3px; background: #ef4444; width: 100%; animation: timer-run 15s linear forwards; margin-bottom: 10px; }

    /* Footer */
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #0f172a; padding: 5px 20px; font-size: 11px; color: #475569; display: flex; justify-content: space-between; z-index: 99; }
</style>
""", unsafe_allow_html=True)

# --- 4. SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'questions' not in st.session_state: st.session_state.questions = []
if 'responses' not in st.session_state: st.session_state.responses = {}

# --- 5. PAGE: HOME ---
if st.session_state.page == "home":
    # Top Status Bar
    st.markdown("""
    <div class="ai-header">
        <span>SYSTEM: <span class="status-dot">● ONLINE</span></span>
        <span>ENGINE: <b>QUANTUM v5.0 (SIMULATION)</b></span>
        <span>LATENCY: <b>1ms</b></span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; margin-top: 30px; font-size: 50px;'>QUANTUM ENGINE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; margin-bottom: 40px;'>⚠️ WARNING: This system penalizes guesswork. Speed > Knowledge.</p>", unsafe_allow_html=True)

    c1, c2 = st.columns([1.5, 1])

    with c1:
        st.markdown("### 📡 INTELLIGENCE FEED")
        st.markdown("""
        <div class="coach-panel">
            <div style="color:#f59e0b; font-weight:bold; margin-bottom:5px;">⚠️ ANOMALY DETECTED: PHYSICS</div>
            <p style="color:#cbd5e1; font-size:13px;">Your accuracy in 'Electromagnetism' is 34%. Deviation from Topper Benchmark detected.</p>
            <div style="color:#38bdf8; font-weight:bold; font-size:14px; margin-top:10px;">➤ RECOMMENDED ACTION: LAUNCH MOCK TEST</div>
        </div>
        """, unsafe_allow_html=True)

        # Live Demo Visual
        st.markdown("""
        <div class="demo-box">
            <div class="timer-line"></div>
            <p style="color:#ef4444; font-size:10px; font-weight:bold;">LIVE CALIBRATION</p>
            <p style="color:#e2e8f0;"><b>Q.</b> In Young's double slit experiment, if slit width is doubled, the intensity becomes?</p>
            <span style="color:#64748b; font-size:12px;">[ A) 2x ] &nbsp; [ B) 4x ] &nbsp; [ C) Same ]</span>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("### ⚡ CONTROL DECK")
        st.write("")
        if st.button("🚀 LAUNCH AI MOCK TEST", type="primary"):
            with st.status("⚙️ Initializing Simulation...", expanded=True):
                time.sleep(1) # Fake loading effect
                st.write("📂 Loading Offline Neural Weights...")
                time.sleep(1)
                st.write("🧠 Generating Questions...")
                time.sleep(0.5)
                # Load Mock Data
                st.session_state.questions = MOCK_DB["Physics"] + MOCK_DB["Chemistry"]
                random.shuffle(st.session_state.questions) # Shuffle for randomness
                st.session_state.questions = st.session_state.questions[:5] # Pick 5
                st.session_state.responses = {}
                st.session_state.page = "exam"
                st.rerun()
                
        st.write("")
        c_a, c_b = st.columns(2)
        c_a.button("🩺 DIAGNOSTIC")
        c_b.button("📊 ANALYZE")

# --- 6. PAGE: EXAM ---
elif st.session_state.page == "exam":
    st.progress(len(st.session_state.responses)/5)
    st.markdown("### 📝 LIVE SIMULATION TEST")
    
    for i, q in enumerate(st.session_state.questions):
        st.markdown(f"""
        <div style="background:#1e293b; padding:15px; border-radius:10px; border-left:4px solid #38bdf8; margin-bottom:10px;">
            <b>Q{i+1}: {q['q']}</b>
        </div>
        """, unsafe_allow_html=True)
        val = st.radio(f"Select Option {i+1}", q['opt'], key=f"q{i}", index=None)
        if val: st.session_state.responses[i] = val
        
    if st.button("✅ SUBMIT & ANALYZE", type="primary"):
        st.session_state.page = "result"
        st.rerun()

# --- 7. PAGE: RESULT ---
elif st.session_state.page == "result":
    score = sum([1 for i, q in enumerate(st.session_state.questions) if st.session_state.responses.get(i) == q['ans']])
    st.markdown(f"<h1 style='text-align:center; color:#4ade80;'>SCORE: {score}/5</h1>", unsafe_allow_html=True)
    
    for i, q in enumerate(st.session_state.questions):
        user = st.session_state.responses.get(i, "Skipped")
        color = "#10b981" if user == q['ans'] else "#ef4444"
        st.markdown(f"""
        <div style="background:{color}20; padding:15px; border-radius:10px; border:1px solid {color}; margin-bottom:10px;">
            <b>Q{i+1}: {q['q']}</b><br>
            <small>Your Ans: {user} | Correct: {q['ans']}</small><br>
            <i>💡 Logic: {q['exp']}</i>
        </div>
        """, unsafe_allow_html=True)
        
    if st.button("🔄 RESTART ENGINE"):
        st.session_state.page = "home"
        st.rerun()

# --- FOOTER ---
st.markdown("""
<div class="footer">
    <span>USER: #IND-ADMIN</span>
    <span>MODE: OFFLINE SIMULATION</span>
    <span>STATUS: SECURE</span>
</div>
""", unsafe_allow_html=True)
        
