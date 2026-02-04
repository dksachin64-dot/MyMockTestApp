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

# --- 2. COMPLETE SYLLABUS DATABASE (NO 11th/12th TAGS) ---
SYLLABUS = {
    "Physics": [
        "Kinematics & Laws of Motion", "Rotational Motion", "Gravitation", 
        "Thermodynamics & KTG", "Oscillations & Waves", "Electrostatics", 
        "Current Electricity", "Magnetic Effects of Current", "EMI & AC", 
        "Ray & Wave Optics", "Modern Physics (Dual Nature, Atoms, Nuclei)", "Semiconductors"
    ],
    "Chemistry": [
        "Atomic Structure", "Chemical Bonding", "Thermodynamics", "Equilibrium", 
        "Redox & Electrochemistry", "Chemical Kinetics", "Surface Chemistry", 
        "p-Block Elements", "d and f Block Elements", "Coordination Compounds", 
        "GOC (General Organic Chemistry)", "Hydrocarbons", "Aldehydes, Ketones & Acids", 
        "Biomolecules & Polymers"
    ],
    "Biology": [ # NEET Only
        "Diversity in Living World", "Structural Organisation in Plants/Animals", 
        "Cell: Structure & Functions", "Plant Physiology", "Human Physiology", 
        "Reproduction", "Genetics & Evolution", "Biology in Human Welfare", 
        "Biotechnology", "Ecology & Environment"
    ],
    "Maths": [ # JEE Only
        "Sets, Relations & Functions", "Complex Numbers", "Quadratic Equations", 
        "Matrices & Determinants", "Permutations & Combinations", "Binomial Theorem", 
        "Sequence & Series", "Limits, Continuity & Differentiability", 
        "Integral Calculus", "Differential Equations", "Coordinate Geometry", 
        "Vector Algebra & 3D Geometry", "Probability"
    ]
}

# --- 3. DYNAMIC THEMING (BACKGROUNDS & VISUALS) ---
def get_theme_css(subject):
    if subject == "Chemistry":
        # Blue/Purple Chemical Lab Theme
        return """
        <style>
            .stApp { background: linear-gradient(to bottom, #0f0c29, #302b63, #24243e); color: white; }
            .subject-header { 
                background: linear-gradient(90deg, #8E2DE2, #4A00E0); 
                padding: 40px; border-radius: 20px; text-align: center;
                box-shadow: 0 0 30px rgba(74, 0, 224, 0.5); border: 2px solid #a855f7;
            }
            .q-card { background: rgba(255, 255, 255, 0.1); border-left: 5px solid #d8b4fe; backdrop-filter: blur(10px); }
            .btn-primary { background-color: #7c3aed !important; }
        </style>
        """
    elif subject == "Biology":
        # Green DNA/Nature Theme
        return """
        <style>
            .stApp { background: linear-gradient(to bottom, #000000, #0f3d0f, #000000); color: #dcfce7; }
            .subject-header { 
                background: linear-gradient(90deg, #11998e, #38ef7d); 
                padding: 40px; border-radius: 20px; text-align: center;
                box-shadow: 0 0 30px rgba(56, 239, 125, 0.4); border: 2px solid #4ade80;
            }
            .q-card { background: rgba(20, 83, 45, 0.4); border-left: 5px solid #22c55e; backdrop-filter: blur(10px); }
        </style>
        """
    elif subject == "Physics":
        # Dark Space/Nebula Theme
        return """
        <style>
            .stApp { background: linear-gradient(to bottom, #000000, #434343); color: #e0f2fe; }
            .subject-header { 
                background: linear-gradient(90deg, #cb2d3e, #ef473a); 
                padding: 40px; border-radius: 20px; text-align: center;
                box-shadow: 0 0 30px rgba(239, 71, 58, 0.5); border: 2px solid #f87171;
            }
            .q-card { background: rgba(255, 255, 255, 0.05); border-left: 5px solid #fca5a5; backdrop-filter: blur(10px); }
        </style>
        """
    elif subject == "Maths":
        # Tech Grid/Matrix Theme
        return """
        <style>
            .stApp { background-color: #0d1117; color: #e6edf3; }
            .subject-header { 
                background: linear-gradient(90deg, #00F260, #0575E6); 
                padding: 40px; border-radius: 20px; text-align: center;
                box-shadow: 0 0 30px rgba(5, 117, 230, 0.5); border: 2px solid #60a5fa;
            }
            .q-card { background: rgba(30, 41, 59, 0.8); border-left: 5px solid #3b82f6; }
        </style>
        """
    else:
        # Default Landing Page (Golden/Premium)
        return """
        <style>
            .stApp { background-color: #121212; color: #ffffff; }
            .hero-card {
                background: linear-gradient(135deg, #FFD700 0%, #FDB931 100%);
                color: black; padding: 40px; border-radius: 15px; text-align: center;
                box-shadow: 0 0 50px rgba(255, 215, 0, 0.3);
            }
        </style>
        """

# --- 4. SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'questions' not in st.session_state: st.session_state.questions = []
if 'responses' not in st.session_state: st.session_state.responses = {}
if 'exam_config' not in st.session_state: st.session_state.exam_config = {}

# --- 5. AI ENGINE (ADVANCED PROMPT) ---
def get_advanced_paper(exam, subject, topic):
    # Determine difficulty based on Exam Type
    level = "Extremely Hard (JEE Advanced Level)" if "Advanced" in exam else "Hard (NEET/Mains Level)"
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Act as the Chief Paper Setter for NTA (India).
        Create a High-Stakes Mock Test.
        
        exam: {exam}
        subject: {subject}
        topic: {topic}
        difficulty: {level}
        
        INSTRUCTIONS:
        1. Generate 5 questions strictly from '{topic}'.
        2. Questions must test deep concepts, numerical ability, and application.
        3. For JEE, include Integer Type or Multi-correct logic if applicable (but MCQ format).
        4. For NEET, include Assertion-Reason or Match-Matrix types.
        
        OUTPUT JSON:
        [{{ "q": "Question Text", "opt": ["A","B","C","D"], "ans": "Correct Option", "exp": "Deep Concept Explanation" }}]
        """
        res = model.generate_content(prompt)
        return json.loads(res.text.replace("```json", "").replace("```", "").strip())
    except:
        # Offline Backup (Subject Specific)
        return [
            {"q": f"Offline Mode: Concept of {topic} is best described by?", "opt": ["Theory A", "Theory B", "Theory C", "Theory D"], "ans": "Theory A", "exp": "Server busy. This is a backup question."},
            {"q": "Calculate the value for standard conditions.", "opt": ["Zero", "One", "Infinite", "Variable"], "ans": "Zero", "exp": "Standard result backup."}
        ]

# --- 6. PAGE: LANDING (EXAM SELECTION) ---
if st.session_state.page == "home":
    st.markdown(get_theme_css("Default"), unsafe_allow_html=True)
    
    st.markdown("""
    <div class="hero-card">
        <h1 style="font-size: 60px; font-weight: 900;">NTA PRO 2.0</h1>
        <p style="font-size: 20px;">The Most Advanced AI Exam Engine in India</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.info("🩺 MEDICAL STREAM")
        if st.button("START NEET UG", use_container_width=True):
            st.session_state.exam_config = {"exam": "NEET UG", "subjects": ["Physics", "Chemistry", "Biology"]}
            st.session_state.page = "subject_select"
            st.rerun()
            
    with c2:
        st.info("⚙️ ENGINEERING MAINS")
        if st.button("START JEE MAINS", use_container_width=True):
            st.session_state.exam_config = {"exam": "JEE MAINS", "subjects": ["Physics", "Chemistry", "Maths"]}
            st.session_state.page = "subject_select"
            st.rerun()

    with c3:
        st.error("🚀 ENGINEERING ADVANCED")
        if st.button("START JEE ADVANCED", use_container_width=True):
            st.session_state.exam_config = {"exam": "JEE ADVANCED", "subjects": ["Physics", "Chemistry", "Maths"]}
            st.session_state.page = "subject_select"
            st.rerun()

# --- 7. PAGE: SUBJECT DASHBOARD ---
elif st.session_state.page == "subject_select":
    # Default dark theme for selection
    st.markdown(get_theme_css("Default"), unsafe_allow_html=True)
    
    exam = st.session_state.exam_config['exam']
    subjects = st.session_state.exam_config['subjects']
    
    if st.button("⬅️ Change Exam"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown(f"## 🎯 Target: {exam} | Select Subject")
    
    cols = st.columns(len(subjects))
    for i, sub in enumerate(subjects):
        with cols[i]:
            if st.button(f"{sub.upper()}", use_container_width=True):
                st.session_state.exam_config['selected_subject'] = sub
                st.session_state.page = "topic_select"
                st.rerun()

# --- 8. PAGE: TOPIC/SYLLABUS SELECTION ---
elif st.session_state.page == "topic_select":
    sub = st.session_state.exam_config['selected_subject']
    exam = st.session_state.exam_config['exam']
    
    # APPLY DYNAMIC THEME BASED ON SUBJECT
    st.markdown(get_theme_css(sub), unsafe_allow_html=True)
    
    # Subject Header
    st.markdown(f"""
    <div class="subject-header">
        <h1>WELCOME TO {sub.upper()} LAB</h1>
        <p>{exam} Edition | Advanced Syllabus Loaded</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # Syllabus Dropdown
    topic_list = SYLLABUS.get(sub, [])
    selected_topic = st.selectbox("📂 Select Chapter / Unit:", topic_list)
    
    st.write("")
    
    if st.button("🚀 INITIALIZE TEST ENVIRONMENT", type="primary", use_container_width=True):
        st.session_state.exam_config['topic'] = selected_topic
        
        with st.status(f"⚙️ Generating {exam} Level Questions from '{selected_topic}'...", expanded=True):
            st.write("🔍 Analyzing Previous Year Trends...")
            time.sleep(1)
            st.write("🧠 Constructing High-Difficulty Problems...")
            st.session_state.questions = get_advanced_paper(exam, sub, selected_topic)
            st.session_state.responses = {}
            st.session_state.page = "exam"
            st.rerun()
            
    if st.button("⬅️ Back"):
        st.session_state.page = "subject_select"
        st.rerun()

# --- 9. PAGE: EXAM ARENA ---
elif st.session_state.page == "exam":
    sub = st.session_state.exam_config['selected_subject']
    topic = st.session_state.exam_config['topic']
    
    # KEEP THEME
    st.markdown(get_theme_css(sub), unsafe_allow_html=True)
    
    st.markdown(f"### 📝 Test: {topic}")
    
    if not st.session_state.questions:
        st.error("Protocol Failed. Please Retry.")
        if st.button("Back"): st.session_state.page = "home"; st.rerun()
    
    # Progress
    total = len(st.session_state.questions)
    st.progress(len(st.session_state.responses)/total)
    
    for i, q in enumerate(st.session_state.questions):
        st.markdown(f"""
        <div class="q-card">
            <h4 style="margin:0;">Q{i+1}: {q['q']}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        sel = st.radio(f"Choose Option {i+1}", q['opt'], key=f"q{i}", index=None)
        if sel: st.session_state.responses[i] = sel
        st.write("")
        
    c1, c2 = st.columns([1, 4])
    if c1.button("🛑 Abort"):
        st.session_state.page = "home"
        st.rerun()
        
    if c2.button("✅ FINAL SUBMIT", type="primary", use_container_width=True):
        st.session_state.page = "result"
        st.rerun()

# --- 10. PAGE: RESULT ANALYTICS ---
elif st.session_state.page == "result":
    sub = st.session_state.exam_config['selected_subject']
    # KEEP THEME
    st.markdown(get_theme_css(sub), unsafe_allow_html=True)
    
    score = sum([1 for i, q in enumerate(st.session_state.questions) if st.session_state.responses.get(i) == q['ans']])
    total = len(st.session_state.questions)
    
    st.markdown(f"""
    <div class="subject-header">
        <h1>SCORE: {score}/{total}</h1>
        <p>Advanced Analysis Report</p>
    </div>
    """, unsafe_allow_html=True)
    
    for i, q in enumerate(st.session_state.questions):
        user = st.session_state.responses.get(i, "Skipped")
        is_correct = (user == q['ans'])
        css_class = "correct" if is_correct else "wrong"
        status = "✅ CORRECT" if is_correct else "❌ INCORRECT"
        
        st.markdown(f"""
        <style>
            .correct {{ background: rgba(16, 185, 129, 0.2); border: 1px solid #10b981; padding: 15px; border-radius: 10px; }}
            .wrong {{ background: rgba(239, 68, 68, 0.2); border: 1px solid #ef4444; padding: 15px; border-radius: 10px; }}
        </style>
        <div class="{css_class}">
            <h4>Q{i+1}: {q['q']}</h4>
            <p><b>Your Ans:</b> {user} | <b>Correct:</b> {q['ans']}</p>
            <p><b>Status:</b> {status}</p>
            <hr style="border-color: rgba(255,255,255,0.1);">
            <p><i>💡 Concept: {q['exp']}</i></p>
        </div>
        <br>
        """, unsafe_allow_html=True)
        
    if st.button("🔄 Start New Test"):
        st.session_state.page = "home"
        st.rerun()
    
