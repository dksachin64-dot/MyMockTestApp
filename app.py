import streamlit as st
import google.generativeai as genai
import json
import time
import random

# --- 1. CONFIGURATION & SETUP ---
st.set_page_config(page_title="MockTest Pro AI", layout="wide", page_icon="🎯")

# API Key
GOOGLE_API_KEY = "AIzaSyALMoUhT8s7GYOHexDYrhnMNVT1xqQ4bgE"
genai.configure(api_key=GOOGLE_API_KEY)

# --- 2. PRO DESIGN (CSS) ---
st.markdown("""
<style>
    .stApp { background-color: #f4f6f9; }
    
    /* Hero Card */
    .hero-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    /* Exam Icon Cards */
    .exam-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #eee;
    }
    
    /* Question Card */
    .q-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        border-left: 6px solid #764ba2;
        margin-bottom: 20px;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'xp' not in st.session_state: st.session_state.xp = 1200
if 'questions' not in st.session_state: st.session_state.questions = []
if 'current_exam' not in st.session_state: st.session_state.current_exam = ""
if 'responses' not in st.session_state: st.session_state.responses = {}

# --- 4. EXAM ICONS ---
EXAM_ICONS = {
    "SSC CGL": "🏛️", "UPSC CSE": "🇮🇳", "JEE Mains": "⚙️", 
    "NEET": "🩺", "Bank PO": "🏦", "Railways": "🚂",
    "CAT": "📊", "Defense": "✈️"
}

# --- 5. AI GENERATOR ---
def generate_paper_ai(exam_name):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Create a professional Mock Test for: {exam_name}.
    Format: JSON Array. Size: 5 Questions.
    Include: 'q' (question), 'opt' (list of 4 options), 'ans' (correct option), 'exp' (explanation).
    """
    try:
        res = model.generate_content(prompt)
        text = res.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except:
        return []

# --- HELPER: LOADER ---
def start_loader(exam_name):
    st.session_state.current_exam = exam_name
    with st.status(f"🤖 AI {exam_name} ka Paper bana raha hai...", expanded=True) as status:
        st.write("🔍 Syllabus Scan ho raha hai...")
        time.sleep(1)
        st.write("✍️ Drafting Questions...")
        
        data = generate_paper_ai(exam_name)
        
        if data:
            st.session_state.questions = data
            st.session_state.responses = {}
            st.session_state.page = "exam"
            status.update(label="✅ Paper Ready!", state="complete", expanded=False)
            st.rerun()
        else:
            status.update(label="❌ Error. Try Again.", state="error")

# --- 6. PAGE: HOME ---
if st.session_state.page == "home":
    with st.sidebar:
        st.header("👤 Profile")
        st.write(f"**XP:** {st.session_state.xp} 🔥")
        st.progress(0.7)

    st.markdown(f"""
    <div class="hero-card">
        <h1>🚀 Mock Test AI Pro</h1>
        <p>India's Smartest Exam Portal</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("📝 Select Your Exam")
    
    cols = st.columns(4)
    exams = list(EXAM_ICONS.keys())
    for i, col in enumerate(cols):
        with col:
            if i < 4:
                exam = exams[i]
                if st.button(f"{EXAM_ICONS[exam]} {exam}", key=exam, use_container_width=True):
                    start_loader(exam)
                    
    cols2 = st.columns(4)
    for i, col in enumerate(cols2):
        with col:
            if i+4 < len(exams):
                exam = exams[i+4]
                if st.button(f"{EXAM_ICONS[exam]} {exam}", key=exam, use_container_width=True):
                    start_loader(exam)

# --- 7. PAGE: EXAM ---
elif st.session_state.page == "exam":
    st.markdown(f"## 📝 {st.session_state.current_exam} - Live Test")
    
    if st.button("🔴 QUIT TEST"):
        st.session_state.page = "home"
        st.rerun()
        
    st.progress(len(st.session_state.responses) / len(st.session_state.questions))
    
    for i, q in enumerate(st.session_state.questions):
        st.markdown(f"""
        <div class="q-card">
            <b>Q{i+1}.</b> {q['q']}
        </div>
        """, unsafe_allow_html=True)
        
        val = st.session_state.responses.get(i, None)
        sel = st.radio(f"Select Option:", q['opt'], index=None if not val else q['opt'].index(val), key=f"rad_{i}")
        if sel:
            st.session_state.responses[i] = sel
            
    if st.button("✅ SUBMIT EXAM", type="primary", use_container_width=True):
        st.session_state.page = "result"
        st.session_state.xp += 50
        st.rerun()

# --- 8. PAGE: RESULT ---
elif st.session_state.page == "result":
    st.balloons()
    score = 0
    for i, q in enumerate(st.session_state.questions):
        if st.session_state.responses.get(i) == q['ans']:
            score += 1
            
    st.markdown(f"""
    <div class="hero-card">
        <h2>🏆 Test Result</h2>
        <h1>{score} / {len(st.session_state.questions)}</h1>
        <p>XP Earned: +50</p>
    </div>
    """, unsafe_allow_html=True)
    
    for i, q in enumerate(st.session_state.questions):
        user_ans = st.session_state.responses.get(i, "Skipped")
        with st.expander(f"Q{i+1}: Analysis"):
            st.write(f"**Correct:** {q['ans']}")
            st.info(f"💡 {q['exp']}")
            
    if st.button("🔄 Take Another Test"):
        st.session_state.page = "home"
        st.rerun()
        
