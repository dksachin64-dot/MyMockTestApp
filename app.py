import streamlit as st
import google.generativeai as genai
import json
import time
import random

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Quantum JEE/NEET AI", layout="wide", page_icon="🧬")

# API Key
GOOGLE_API_KEY = "AIzaSyALMoUhT8s7GYOHexDYrhnMNVT1xqQ4bgE"
genai.configure(api_key=GOOGLE_API_KEY)

# --- 2. HIGH-TECH 'DARK LAB' UI (Best Colour Display) ---
st.markdown("""
<style>
    /* Main Background - Dark Sci-Fi Theme */
    .stApp { background-color: #0f172a; color: #e2e8f0; }
    
    /* Neon Header */
    .hero-container {
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
        padding: 3px; border-radius: 15px; box-shadow: 0 0 20px rgba(0, 114, 255, 0.6);
        margin-bottom: 30px;
    }
    .hero-content {
        background: #1e293b; padding: 25px; border-radius: 12px; text-align: center;
    }
    .hero-content h1 {
        background: -webkit-linear-gradient(#00c6ff, #0072ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 900; letter-spacing: 2px; margin: 0;
    }
    .hero-content p { color: #cbd5e1; font-size: 18px; }
    
    /* Question Card */
    .q-card {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid #334155;
        padding: 20px; border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        border-left: 4px solid #00c6ff;
    }
    
    /* NCERT Tag */
    .ncert-tag {
        background-color: #064e3b; color: #34d399;
        padding: 4px 12px; border-radius: 20px;
        font-size: 11px; font-weight: bold; border: 1px solid #059669;
        display: inline-block; margin-bottom: 8px;
    }
    
    /* BUTTON FIX (Taaki text saaf dikhe) */
    .stButton > button {
        color: #000000 !important;  /* Black Text */
        background-color: #ffffff !important; /* White Button */
        border: 2px solid #00c6ff !important; /* Neon Border */
        font-weight: bold !important;
        border-radius: 8px !important;
    }
    .stButton > button:hover {
        background-color: #00c6ff !important;
        color: white !important;
    }

    /* Result Colors */
    .correct { background: #065f46; border: 1px solid #10b981; padding: 15px; border-radius: 10px; color: #d1fae5; }
    .wrong { background: #7f1d1d; border: 1px solid #ef4444; padding: 15px; border-radius: 10px; color: #fee2e2; }
    
</style>
""", unsafe_allow_html=True)

# --- 3. ROBUST OFFLINE NCERT DATABASE (Backup) ---
OFFLINE_DB = {
    "Physics": [
        {"q": "A particle moves with equation x = t² - 4t + 3. Find velocity at t=2s.", "opt": ["0 m/s", "2 m/s", "4 m/s", "-2 m/s"], "ans": "0 m/s", "ref": "NCERT XI: Kinematics", "exp": "v = dx/dt = 2t - 4. At t=2, v = 2(2)-4 = 0."},
        {"q": "Dimensional formula of Gravitational Constant (G)?", "opt": ["M⁻¹L³T⁻²", "MLT⁻²", "M⁻¹L²T⁻²", "M⁰L⁰T⁰"], "ans": "M⁻¹L³T⁻²", "ref": "NCERT XI: Units & Measurements", "exp": "F = Gm1m2/r² => G = Fr²/m1m2."},
        {"q": "Electric field inside a spherical shell is?", "opt": ["Zero", "Infinite", "Uniform", "Variable"], "ans": "Zero", "ref": "NCERT XII: Electrostatics (Pg 32)", "exp": "According to Gauss Law, E-field inside a conductor is zero."},
        {"q": "Phenomenon responsible for mirage?", "opt": ["Total Internal Reflection", "Refraction", "Diffraction", "Polarization"], "ans": "Total Internal Reflection", "ref": "NCERT XII: Ray Optics", "exp": "Light travels from denser to rarer medium (Hot air)."},
        {"q": "Unit of Magnetic Flux?", "opt": ["Weber", "Tesla", "Gauss", "Ampere"], "ans": "Weber", "ref": "NCERT XII: EMI", "exp": "Tesla is for field, Weber is for Flux."}
    ],
    "Chemistry": [
        {"q": "Shape of NH3 molecule according to VSEPR?", "opt": ["Pyramidal", "Tetrahedral", "Linear", "Bent"], "ans": "Pyramidal", "ref": "NCERT XI: Chemical Bonding", "exp": "Due to one lone pair on Nitrogen."},
        {"q": "Which is a colligative property?", "opt": ["Osmotic Pressure", "Viscosity", "Surface Tension", "Refractive Index"], "ans": "Osmotic Pressure", "ref": "NCERT XII: Solutions", "exp": "Depends only on number of solute particles."},
        {"q": "Hybridization of Carbon in Graphite?", "opt": ["sp2", "sp3", "sp", "dsp2"], "ans": "sp2", "ref": "NCERT XI: p-Block Elements", "exp": "Layered structure, one electron free."},
        {"q": "Transition elements show color due to?", "opt": ["d-d transition", "f-f transition", "Charge transfer", "Polarization"], "ans": "d-d transition", "ref": "NCERT XII: d-Block Elements", "exp": "Unpaired electrons jump between d-orbitals."},
        {"q": "Molarity of pure water is?", "opt": ["55.5 M", "18 M", "1 M", "100 M"], "ans": "55.5 M", "ref": "NCERT XI: Mole Concept", "exp": "1000g / 18g/mol = 55.55 mol/L."}
    ],
    "Biology": [
        {"q": "Powerhouse of the cell?", "opt": ["Mitochondria", "Nucleus", "Ribosome", "Golgi"], "ans": "Mitochondria", "ref": "NCERT XI: Cell Unit of Life", "exp": "Site of Aerobic Respiration (ATP)."},
        {"q": "Functional unit of Kidney?", "opt": ["Nephron", "Neuron", "Alveoli", "Villi"], "ans": "Nephron", "ref": "NCERT XI: Excretory Products", "exp": "Filtration unit."},
        {"q": "Genetic material in HIV?", "opt": ["ss-RNA", "ds-DNA", "ss-DNA", "ds-RNA"], "ans": "ss-RNA", "ref": "NCERT XII: Human Health", "exp": "It is a Retrovirus."},
        {"q": "Example of homologous organs?", "opt": ["Forelimbs of Man & Bat", "Wings of Bat & Insect", "Eye of Octopus & Mammal", "None"], "ans": "Forelimbs of Man & Bat", "ref": "NCERT XII: Evolution", "exp": "Same structure, different function (Divergent Evolution)."},
        {"q": "Double fertilization is unique to?", "opt": ["Angiosperms", "Gymnosperms", "Bryophytes", "Pteridophytes"], "ans": "Angiosperms", "ref": "NCERT XII: Sexual Reproduction", "exp": "Syngamy + Triple Fusion."}
    ],
    "Maths": [
        {"q": "Value of lim(x->0) (sin x / x)?", "opt": ["1", "0", "Infinity", "Does not exist"], "ans": "1", "ref": "NCERT XI: Limits", "exp": "Standard Limit theorem."},
        {"q": "Derivative of log(x)?", "opt": ["1/x", "x", "e^x", "1"], "ans": "1/x", "ref": "NCERT XII: Continuity & Diff", "exp": "d/dx(ln x) = 1/x."},
        {"q": "If A is a square matrix, A + A' is always?", "opt": ["Symmetric", "Skew-symmetric", "Identity", "Null"], "ans": "Symmetric", "ref": "NCERT XII: Matrices", "exp": "Transpose of (A+A') = A'+A = Same."},
        {"q": "Integral of e^x dx?", "opt": ["e^x + C", "x e^x + C", "e^x / x", "log x"], "ans": "e^x + C", "ref": "NCERT XII: Integrals", "exp": "It is its own derivative and integral."},
        {"q": "Slope of normal to y=x² at (1,1)?", "opt": ["-1/2", "2", "1", "-2"], "ans": "-1/2", "ref": "NCERT XII: AOD", "exp": "dy/dx = 2x. At x=1, m=2. Slope of normal = -1/m = -1/2."}
    ]
}

# --- 4. SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'questions' not in st.session_state: st.session_state.questions = []
if 'responses' not in st.session_state: st.session_state.responses = {}
if 'exam_details' not in st.session_state: st.session_state.exam_details = {}

# --- 5. AI GENERATOR (NCERT MODE) ---
def get_ncert_paper(exam, grade, subject):
    # Try AI First
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Act as a Senior Faculty for {exam} (JEE Advanced/NEET).
        Create 5 Hard-Level MCQ Questions for Class {grade} {subject}.
        
        STRICT REQUIREMENT: 
        1. Must be based on NCERT concepts.
        2. Format: JSON.
        3. Include 'ref' pointing to NCERT Chapter/Page.
        
        JSON Structure:
        [{{ "q": "Question", "opt": ["A","B","C","D"], "ans": "Correct Option", "ref": "NCERT Ref", "exp": "Explanation" }}]
        """
        res = model.generate_content(prompt)
        data = json.loads(res.text.replace("```json", "").replace("```", "").strip())
        if data: return data
    except:
        pass
    
    # Fallback to Offline DB (Crash Proof)
    return OFFLINE_DB.get(subject, OFFLINE_DB["Physics"])

# --- 6. PAGE: HOME ---
if st.session_state.page == "home":
    st.markdown("""
    <div class="hero-container">
        <div class="hero-content">
            <h1>🧬 QUANTUM JEE/NEET</h1>
            <p>Advanced NCERT-Based Intelligence Engine</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### ⚙️ Configure Test")
        target_exam = st.selectbox("Target Exam", ["NEET (Medical)", "JEE Mains", "JEE Advanced"])
        grade = st.selectbox("Class Level", ["Class 11", "Class 12"])
        
        st.markdown("---")
        st.info("💡 'JEE Advanced' selects high-level numericals.")

    with col2:
        st.markdown("### 🧪 Select Subject Module")
        
        subjects = ["Physics", "Chemistry", "Biology"] if "NEET" in target_exam else ["Physics", "Chemistry", "Maths"]
        
        # Grid of buttons
        c1, c2, c3 = st.columns(3)
        
        for i, sub in enumerate(subjects):
            col = [c1, c2, c3][i]
            if col.button(f"{sub} 🔬", use_container_width=True):
                st.session_state.exam_details = {"exam": target_exam, "grade": grade, "subject": sub}
                
                with st.status("🔄 Initializing Quantum Engine...", expanded=True):
                    st.write(f"📂 Loading NCERT {grade} {sub} Database...")
                    time.sleep(1)
                    st.write("🧠 Synthesizing High-Order Questions...")
                    
                    st.session_state.questions = get_ncert_paper(target_exam, grade, sub)
                    st.session_state.responses = {}
                    st.session_state.page = "exam"
                    st.rerun()

# --- 7. PAGE: EXAM INTERFACE ---
elif st.session_state.page == "exam":
    details = st.session_state.exam_details
    st.markdown(f"## 📝 {details['exam']} : {details['subject']} ({details['grade']})")
    
    # Check if questions loaded
    if not st.session_state.questions:
        st.error("⚠️ Connection Weak. Loading Offline Backup...")
        st.session_state.questions = OFFLINE_DB.get(details['subject'], OFFLINE_DB["Physics"])
        st.rerun()

    # Progress Bar
    total = len(st.session_state.questions)
    st.progress(len(st.session_state.responses) / total)
    
    for i, q in enumerate(st.session_state.questions):
        st.markdown(f'<span class="ncert-tag">📖 {q.get("ref", "NCERT Concept")}</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="q-card"><b>Q{i+1}.</b> {q["q"]}</div>', unsafe_allow_html=True)
        
        sel = st.radio(f"Select Option {i+1}", q["opt"], key=f"q{i}", index=None)
        if sel: st.session_state.responses[i] = sel
        st.write("")

    col_b1, col_b2 = st.columns([1, 4])
    if col_b1.button("⬅️ Abort"):
        st.session_state.page = "home"
        st.rerun()
    
    if col_b2.button("🚀 Submit & Analyze", type="primary", use_container_width=True):
        st.session_state.page = "result"
        st.rerun()

# --- 8. PAGE: ADVANCED ANALYTICS ---
elif st.session_state.page == "result":
    score = sum([1 for i, q in enumerate(st.session_state.questions) if st.session_state.responses.get(i) == q['ans']])
    total = len(st.session_state.questions)
    percentage = (score/total)*100
    
    # High Tech Scoreboard
    st.markdown(f"""
    <div style="text-align:center; padding: 20px; background: #1e293b; border-radius: 15px; border: 1px solid #334155;">
        <h2 style="color: #94a3b8;">PERFORMANCE METRICS</h2>
        <h1 style="font-size: 60px; color: {'#10b981' if percentage > 70 else '#ef4444'};">{score}/{total}</h1>
        <p>ACCURACY: {percentage}%</p>
    </div>
    <br>
    """, unsafe_allow_html=True)
    
    for i, q in enumerate(st.session_state.questions):
        user = st.session_state.responses.get(i, "Not Attempted")
        css = "correct" if user == q['ans'] else "wrong"
        status = "✅ OPTIMAL" if user == q['ans'] else "❌ DEVIATION"
        
        st.markdown(f"""
        <div class="{css}">
            <div style="display:flex; justify-content:space-between;">
                <span style="font-size:12px; opacity:0.8;">{q.get('ref', 'NCERT')}</span>
                <span style="font-weight:bold;">{status}</span>
            </div>
            <h4 style="margin-top:5px;">Q{i+1}: {q['q']}</h4>
            <p><b>Your Input:</b> {user} | <b>Correct Output:</b> {q['ans']}</p>
            <hr style="border-color: rgba(255,255,255,0.2);">
            <p style="font-style: italic;">💡 <b>Logic:</b> {q['exp']}</p>
        </div><br>
        """, unsafe_allow_html=True)

    if st.button("🔄 Initiate New Protocol"):
        st.session_state.page = "home"
        st.rerun()
        
