import streamlit as st
import google.generativeai as genai
import json
import time
import random

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="King of Mock Tests 👑", layout="wide", page_icon="🇮🇳")

# API Key
GOOGLE_API_KEY = "AIzaSyALMoUhT8s7GYOHexDYrhnMNVT1xqQ4bgE"
genai.configure(api_key=GOOGLE_API_KEY)

# --- 2. CSS STYLING (Royal Look) ---
st.markdown("""
<style>
    .stApp { background-color: #fdfbf7; color: #333; }
    
    /* Royal Header */
    .hero-card {
        background: linear-gradient(to right, #DAA520, #FFD700); /* Gold Colors */
        padding: 25px; border-radius: 15px; text-align: center;
        margin-bottom: 25px; box-shadow: 0 4px 15px rgba(218, 165, 32, 0.4);
        border: 2px solid #B8860B;
    }
    .hero-card h1 { color: #4b3621; font-weight: 800; margin: 0; }
    .hero-card p { color: #4b3621; font-weight: 600; }
    
    /* Question Card */
    .q-card {
        background: white; padding: 20px; border-radius: 10px;
        border-left: 6px solid #DAA520; margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Source Tag */
    .ref-tag {
        background-color: #fff8e1; color: #8d6e63;
        padding: 4px 10px; border-radius: 4px;
        font-size: 12px; font-weight: bold; border: 1px solid #ffe0b2;
    }
    
    /* Result Colors */
    .correct { background-color: #e8f5e9; border: 1px solid #c8e6c9; color: #1b5e20; padding: 10px; border-radius: 8px;}
    .wrong { background-color: #ffebee; border: 1px solid #ffcdd2; color: #b71c1c; padding: 10px; border-radius: 8px;}
</style>
""", unsafe_allow_html=True)

# --- 3. INDIAN EXAM LIBRARY (The Master List) ---
# Ye hai aapki "Library". Har exam yahan list hai.
INDIAN_EXAM_HUB = {
    "🏛️ UPSC & State PSC": ["UPSC CSE (Prelims)", "UPPSC", "BPSC", "MPPSC", "RAS", "JPSC"],
    "🚂 SSC & Railways": ["SSC CGL", "SSC CHSL", "SSC MTS", "SSC GD", "RRB NTPC", "RRB Group D", "RRB ALP"],
    "⚙️ Engineering (JEE)": ["JEE Mains", "JEE Advanced", "BITSAT", "WBJEE", "MHT CET", "GATE (CS)", "GATE (Mech)"],
    "🩺 Medical (NEET)": ["NEET UG", "AIIMS Nursing", "NEET PG", "B.Sc Nursing"],
    "⚔️ Defence (NDA/CDS)": ["NDA (Maths)", "NDA (GAT)", "CDS (OTA)", "AFCAT", "Indian Army Agniveer"],
    "🏦 Banking": ["SBI PO", "IBPS PO", "RBI Grade B", "LIC AAO", "RRB Office Assistant"],
    "🎓 Teaching & Others": ["CTET", "UGC NET (Paper 1)", "KVS", "DSSSB", "CLAT (Law)", "CAT (MBA)"]
}

# --- 4. EXAM PATTERN LOGIC (AI Brain) ---
def get_indian_paper(exam_name):
    # Specific instruction for "King Level" Quality
    prompt_style = "Standard Competitive Exam"
    
    if "UPSC" in exam_name:
        prompt_style = "Use 'Statement Based' questions (1 only, 2 only). Focus on Polity (Laxmikanth), History (Spectrum), Environment."
    elif "JEE" in exam_name:
        prompt_style = "Strictly Numerical & Conceptual. Physics (HC Verma level), Chemistry (NCERT Deep lines), Math (Cengage level)."
    elif "NEET" in exam_name:
        prompt_style = "Strictly NCERT Biology based lines. Assertion-Reasoning type questions included."
    elif "SSC" in exam_name or "Railways" in exam_name:
        prompt_style = "Focus on Quant Shortcuts, Reasoning Puzzles, and Static GK (Lucent style)."
    elif "NDA" in exam_name:
        prompt_style = "Maths should be 11th/12th level. GAT should cover English and General Science."

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Act as the 'King of Mock Tests' for India.
        Create a Premium Quality Mock Test for: "{exam_name}".
        
        INSTRUCTIONS:
        1. Pattern: {prompt_style}
        2. Difficulty: Exam Level (Not too easy).
        3. Language: English (Standard).
        4. Quantity: 10 Questions.
        
        OUTPUT FORMAT (JSON ONLY):
        [{{
            "q": "Question Text",
            "opt": ["A", "B", "C", "D"],
            "ans": "Correct Option Full Text",
            "ref": "Reference Book/Topic (e.g., NCERT Class 11, Laxmikanth Ch-5)",
            "exp": "Detailed Solution/Trick"
        }}]
        """
        res = model.generate_content(prompt)
        return json.loads(res.text.replace("```json", "").replace("```", "").strip())
    except:
        return []

# --- 5. SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'questions' not in st.session_state: st.session_state.questions = []
if 'responses' not in st.session_state: st.session_state.responses = {}
if 'current_exam' not in st.session_state: st.session_state.current_exam = ""

# --- 6. PAGE: HOME (LIBRARY VIEW) ---
if st.session_state.page == "home":
    st.markdown("""
    <div class="hero-card">
        <h1>👑 KING OF MOCK TESTS 👑</h1>
        <p>India's Largest Free Exam Library | No Paywall | Pure Selection</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for Category
    with st.sidebar:
        st.header("📂 Select Category")
        category = st.radio("Choose Stream:", list(INDIAN_EXAM_HUB.keys()))
        st.info("Designed for 100% Success Rate")

    # Main Area: Show Exams in that Category
    st.subheader(f"📚 {category}")
    exams = INDIAN_EXAM_HUB[category]
    
    # Grid Layout for Buttons
    cols = st.columns(3)
    for i, exam in enumerate(exams):
        with cols[i % 3]:
            if st.button(f"🚀 Start {exam}", use_container_width=True):
                st.session_state.current_exam = exam
                with st.status("⚙️ Setting up Exam Paper...", expanded=True):
                    st.write("🔍 Analyzing Syllabus...")
                    time.sleep(1)
                    st.write("📖 Picking High-Probablity Questions...")
                    st.session_state.questions = get_indian_paper(exam)
                    st.session_state.responses = {}
                    st.session_state.page = "exam"
                    st.rerun()

# --- 7. PAGE: EXAM MODE ---
elif st.session_state.page == "exam":
    st.markdown(f"### ✍️ {st.session_state.current_exam} - Live Test")
    st.progress(len(st.session_state.responses)/len(st.session_state.questions))
    
    for i, q in enumerate(st.session_state.questions):
        st.markdown(f'<div class="ref-tag">📖 Ref: {q.get("ref", "Syllabus")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="q-card"><b>Q{i+1}.</b> {q["q"]}</div>', unsafe_allow_html=True)
        
        sel = st.radio(f"Select Answer {i+1}", q["opt"], key=f"q{i}", index=None)
        if sel: st.session_state.responses[i] = sel
        st.write("") # Spacer

    st.write("---")
    if st.button("✅ Submit Paper", type="primary"):
        st.session_state.page = "result"
        st.rerun()

# --- 8. PAGE: RESULT & ANALYSIS ---
elif st.session_state.page == "result":
    score = sum([1 for i, q in enumerate(st.session_state.questions) if st.session_state.responses.get(i) == q['ans']])
    total = len(st.session_state.questions)
    
    st.markdown(f"""
    <div class="hero-card">
        <h1>Result: {score} / {total}</h1>
        <p>{'👑 King Level Performance!' if score > 8 else 'Needs Improvement 📚'}</p>
    </div>
    """, unsafe_allow_html=True)
    
    for i, q in enumerate(st.session_state.questions):
        user = st.session_state.responses.get(i, "Not Attempted")
        css = "correct" if user == q['ans'] else "wrong"
        status = "✅ Correct" if user == q['ans'] else "❌ Wrong"
        
        st.markdown(f"""
        <div class="{css}">
            <small><b>Ref: {q.get('ref')}</b></small><br>
            <b>Q{i+1}: {q['q']}</b><br>
            Your Ans: {user} | Correct: <b>{q['ans']}</b><br>
            <hr>
            <i>💡 Explanation: {q['exp']}</i>
        </div><br>
        """, unsafe_allow_html=True)
        
    if st.button("🏠 Back to Library"):
        st.session_state.page = "home"
        st.rerun()
