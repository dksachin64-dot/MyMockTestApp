import streamlit as st
import google.generativeai as genai
import json
import time
import random

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="NTA PRO: Exam Portal", layout="wide", page_icon="🧬")

# API Key
GOOGLE_API_KEY = "AIzaSyALMoUhT8s7GYOHexDYrhnMNVT1xqQ4bgE"
genai.configure(api_key=GOOGLE_API_KEY)

# --- 2. COMPLETE SYLLABUS DATABASE ---
SYLLABUS = {
    "Physics": [
        "Kinematics & Laws of Motion", "Rotational Motion", "Gravitation", 
        "Thermodynamics & KTG", "Oscillations & Waves", "Electrostatics", 
        "Current Electricity", "Magnetic Effects of Current", "EMI & AC", 
        "Ray & Wave Optics", "Modern Physics", "Semiconductors"
    ],
    "Chemistry": [
        "Atomic Structure", "Chemical Bonding", "Thermodynamics", "Equilibrium", 
        "Redox & Electrochemistry", "Chemical Kinetics", "Surface Chemistry", 
        "p-Block Elements", "d and f Block Elements", "Coordination Compounds", 
        "GOC (General Organic Chemistry)", "Hydrocarbons", "Aldehydes, Ketones & Acids", 
        "Biomolecules & Polymers"
    ],
    "Biology": [
        "Diversity in Living World", "Structural Organisation", 
        "Cell: Structure & Functions", "Plant Physiology", "Human Physiology", 
        "Reproduction", "Genetics & Evolution", "Biology in Human Welfare", 
        "Biotechnology", "Ecology & Environment"
    ],
    "Maths": [
        "Sets, Relations & Functions", "Complex Numbers", "Quadratic Equations", 
        "Matrices & Determinants", "Permutations & Combinations", "Binomial Theorem", 
        "Sequence & Series", "Calculus (Limits, Diff, Integral)", 
        "Coordinate Geometry", "Vector Algebra & 3D", "Probability"
    ]
}

# --- 3. FORCE VISIBLE CSS (Button Fix) ---
def get_theme_css(subject):
    # Common Button Style (Text will ALWAYS be visible now)
    button_style = """
        <style>
            /* Force Button Text Color */
            .stButton > button {
                color: #000000 !important; /* Black Text */
                background-color: #ffffff !important; /* White Background */
                border: 2px solid #cccccc !important;
                font-weight: bold !important;
                font-size: 16px !important;
            }
            .stButton > button:hover {
                border-color: #00c6ff !important;
                color: #0072ff !important;
            }
            .stApp { color: white; }
        </style>
    """
    
    if subject == "Chemistry":
        return button_style + """
        <style>
            .stApp { background: linear-gradient(to bottom, #0f0c29, #302b63, #24243e); }
            .subject-header { 
                background: linear-gradient(90deg, #8E2DE2, #4A00E0); 
                padding: 30px; border-radius: 15px; text-align: center; border: 2px solid #a855f7;
            }
            .q-card { background: rgba(255, 255, 255, 0.1); border-left: 5px solid #d8b4fe; padding: 20px; border-radius: 10px; }
        </style>
        """
    elif subject == "Biology":
        return button_style + """
        <style>
            .stApp { background: linear-gradient(to bottom, #000000, #0f3d0f); }
            .subject-header { 
                background: linear-gradient(90deg, #11998e, #38ef7d); 
                padding: 30px; border-radius: 15px; text-align: center; border: 2px solid #4ade80;
            }
            .q-card { background: rgba(20, 83, 45, 0.4); border-left: 5px solid #22c55e; padding: 20px; border-radius: 10px; }
        </style>
        """
    elif subject == "Physics":
        return button_style + """
        <style>
            .stApp { background: linear-gradient(to bottom, #000000, #434343); }
            .subject-header { 
                background: linear-gradient(90deg, #cb2d3e, #ef473a); 
                padding: 30px; border-radius: 15px; text-align: center; border: 2px solid #f87171;
            }
            .q-card { background: rgba(255, 255, 255, 0.05); border-left: 5px solid #fca5a5; padding: 20px; border-radius: 10px; }
        </style>
        """
    elif subject == "Maths":
        return button_style + """
        <style>
            .stApp { background-color: #0d1117; }
            .subject-header { 
                background: linear-gradient(90deg, #00F260, #0575E6); 
                padding: 30px; border-radius: 15px; text-align: center; border: 2px solid #60a5fa;
            }
            .q-card { background: rgba(30, 41, 59, 0.8); border-left: 5px solid #3b82f6; padding: 20px; border-radius: 10px; }
        </style>
        """
    else:
        # Home Page Theme
        return button_style + """
        <style>
            .stApp { background-color: #121212; }
            .hero-card {
                background: linear-gradient(135deg, #FFD700 0%, #FDB931 100%);
                color: black; padding: 30px; border-radius: 15px; text-align: center;
                box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
            }
        </style>
        """

# --- 4. SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'questions' not in st.session_state: st.session_state.questions = []
if 'responses' not in st.session_state: st.session_state.responses = {}
if 'exam_config' not in st.session_state: st.session_state.exam_config = {}

# --- 5. AI ENGINE ---
def get_advanced_paper(exam, subject, topic):
    level = "Extremely Hard" if "Advanced" in exam else "Hard"
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Act as NTA Paper Setter. Create 5 High-Level MCQs for {exam}.
        Subject: {subject}, Topic: {topic}, Difficulty: {level}.
        Output JSON: [{{ "q": "Question", "opt": ["A","B","C","D"], "ans": "Correct Option", "exp": "Explanation" }}]
        """
        res = model.generate_content(prompt)
        return json.loads(res.text.replace("```json", "").replace("```", "").strip())
    except:
        return [
            {"q": f"Offline Backup: What describes {topic} best?", "opt": ["Concept A", "Concept B", "Concept C", "Concept D"], "ans": "Concept A", "exp": "Server busy."},
            {"q": "Calculate standard value.", "opt": ["0", "1", "10", "100"], "ans": "0", "exp": "Backup numerical."}
        ]

# --- 6. PAGE: HOME ---
if st.session_state.page == "home":
    st.markdown(get_theme_css("Default"), unsafe_allow_html=True)
    
    st.markdown("""
    <div class="hero-card">
        <h1>🚀 NTA PRO 2.0</h1>
        <p>Advanced AI Exam Portal</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("NEET UG (Medical)"):
            st.session_state.exam_config = {"exam": "NEET UG", "subjects": ["Physics", "Chemistry", "Biology"]}
            st.session_state.page = "subject_select"
            st.rerun()
    with c2:
        if st.button("JEE MAINS"):
            st.session_state.exam_config = {"exam": "JEE MAINS", "subjects": ["Physics", "Chemistry", "Maths"]}
            st.session_state.page = "subject_select"
            st.rerun()
    with c3:
        if st.button("JEE ADVANCED"):
            st.session_state.exam_config = {"exam": "JEE ADVANCED", "subjects": ["Physics", "Chemistry", "Maths"]}
            st.session_state.page = "subject_select"
            st.rerun()

# --- 7. PAGE: SUBJECT SELECT ---
elif st.session_state.page == "subject_select":
    st.markdown(get_theme_css("Default"), unsafe_allow_html=True)
    
    exam = st.session_state.exam_config['exam']
    subjects = st.session_state.exam_config['subjects']
    
    if st.button("⬅️ Back"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown(f"### 🎯 Target: {exam}")
    cols = st.columns(len(subjects))
    for i, sub in enumerate(subjects):
        with cols[i]:
            if st.button(sub):
                st.session_state.exam_config['selected_subject'] = sub
                st.session_state.page = "topic_select"
                st.rerun()

# --- 8. PAGE: TOPIC SELECT ---
elif st.session_state.page == "topic_select":
    sub = st.session_state.exam_config['selected_subject']
    st.markdown(get_theme_css(sub), unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="subject-header">
        <h1>{sub.upper()} LAB</h1>
    </div>
    """, unsafe_allow_html=True)
    
    topic_list = SYLLABUS.get(sub, ["General"])
    selected_topic = st.selectbox("📂 Select Chapter:", topic_list)
    
    if st.button("🚀 START TEST"):
        st.session_state.exam_config['topic'] = selected_topic
        with st.status("⚙️ Generating Paper..."):
            st.session_state.questions = get_advanced_paper(st.session_state.exam_config['exam'], sub, selected_topic)
            st.session_state.responses = {}
            st.session_state.page = "exam"
            st.rerun()

# --- 9. PAGE: EXAM ---
elif st.session_state.page == "exam":
    sub = st.session_state.exam_config['selected_subject']
    st.markdown(get_theme_css(sub), unsafe_allow_html=True)
    
    st.markdown(f"### 📝 {st.session_state.exam_config['topic']}")
    
    for i, q in enumerate(st.session_state.questions):
        st.markdown(f'<div class="q-card"><b>Q{i+1}.</b> {q["q"]}</div>', unsafe_allow_html=True)
        sel = st.radio(f"Select Answer {i+1}", q['opt'], key=f"q{i}", index=None)
        if sel: st.session_state.responses[i] = sel
        
    if st.button("✅ SUBMIT"):
        st.session_state.page = "result"
        st.rerun()

# --- 10. PAGE: RESULT ---
elif st.session_state.page == "result":
    sub = st.session_state.exam_config['selected_subject']
    st.markdown(get_theme_css(sub), unsafe_allow_html=True)
    
    score = sum([1 for i, q in enumerate(st.session_state.questions) if st.session_state.responses.get(i) == q['ans']])
    st.markdown(f"## Score: {score}/{len(st.session_state.questions)}")
    
    for i, q in enumerate(st.session_state.questions):
        user = st.session_state.responses.get(i, "Skipped")
        status = "✅ Correct" if user == q['ans'] else "❌ Wrong"
        st.markdown(f"""
        <div class="q-card">
            <b>Q{i+1}: {q['q']}</b><br>
            Your Ans: {user} | Correct: {q['ans']}<br>
            <i>{status} - {q['exp']}</i>
        </div>
        """, unsafe_allow_html=True)
        
    if st.button("🏠 Home"):
        st.session_state.page = "home"
        st.rerun()
        
