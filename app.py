import streamlit as st
import google.generativeai as genai
import json
import time
import random

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="MockTest Pro AI", layout="wide", page_icon="🚀")

# API Key
GOOGLE_API_KEY = "AIzaSyALMoUhT8s7GYOHexDYrhnMNVT1xqQ4bgE"
genai.configure(api_key=GOOGLE_API_KEY)

# --- 2. CSS STYLING (Modern UI) ---
st.markdown("""
<style>
    .stApp { background-color: #f0f2f6; }
    
    .hero-card {
        background: linear-gradient(120deg, #89f7fe 0%, #66a6ff 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .hero-card h1 { color: white; margin: 0; font-size: 28px; }
    
    .exam-btn {
        width: 100%;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #ddd;
        background: white;
        text-align: center;
        cursor: pointer;
        transition: 0.3s;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    .q-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #66a6ff;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'questions' not in st.session_state: st.session_state.questions = []
if 'exam_name' not in st.session_state: st.session_state.exam_name = ""
if 'responses' not in st.session_state: st.session_state.responses = {}

# --- 4. EXAM LIST ---
EXAMS = {
    "UPSC CSE": "🇮🇳", "SSC CGL": "🏛️", "JEE Mains": "⚙️", "NEET": "🩺",
    "Bank PO": "🏦", "Railways": "🚂", "Defense": "⚔️", "CAT": "📊"
}

# --- 5. AI ENGINE (With Backup) ---
def get_ai_paper(exam):
    # Try AI Generation
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Create a hard Mock Test for {exam}.
        Return a JSON Array of 5 questions.
        Keys: "q" (Question), "opt" (4 Options list), "ans" (Correct Option), "exp" (Short Explanation).
        IMPORTANT: Return ONLY valid JSON.
        """
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        # BACKUP PLAN (Agar AI fail ho to ye dikhao)
        return [
            {
                "q": f"({exam} Server Busy) Who is known as the Iron Man of India?",
                "opt": ["Gandhi Ji", "Nehru Ji", "Sardar Patel", "Bose"],
                "ans": "Sardar Patel",
                "exp": "This is a backup question because AI traffic is high."
            },
            {
                "q": "Which gas is most abundant in the Earth's atmosphere?",
                "opt": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"],
                "ans": "Nitrogen",
                "exp": "Nitrogen makes up about 78% of the atmosphere."
            },
            {
                "q": "What is the value of Pi (approx)?",
                "opt": ["3.14", "2.14", "4.14", "1.14"],
                "ans": "3.14",
                "exp": "Pi is approximately 3.14159..."
            },
            {
                "q": "Capital of Australia is?",
                "opt": ["Sydney", "Melbourne", "Canberra", "Perth"],
                "ans": "Canberra",
                "exp": "Canberra is the capital city."
            },
            {
                "q": "Chemical symbol for Gold?",
                "opt": ["Au", "Ag", "Fe", "Cu"],
                "ans": "Au",
                "exp": "Au comes from Aurum."
            }
        ]

# --- 6. PAGE: HOME ---
if st.session_state.page == "home":
    st.markdown("""
    <div class="hero-card">
        <h1>🚀 Mock Test AI Pro</h1>
        <p>Select an exam to start instant AI generation</p>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(2)
    exam_list = list(EXAMS.keys())
    
    for i, exam in enumerate(exam_list):
        col = cols[i % 2]
        with col:
            if st.button(f"{EXAMS[exam]} {exam}", use_container_width=True):
                st.session_state.exam_name = exam
                
                # Loading Animation
                with st.status(f"🤖 AI {exam} ka Paper bana raha hai...", expanded=True):
                    st.write("Processing Syllabus...")
                    time.sleep(1)
                    st.write("Drafting Questions...")
                    
                    # Fetch Data
                    data = get_ai_paper(exam)
                    st.session_state.questions = data
                    st.session_state.responses = {}
                    st.session_state.page = "exam"
                    st.rerun()

# --- 7. PAGE: EXAM ---
elif st.session_state.page == "exam":
    st.markdown(f"### 📝 {st.session_state.exam_name} Test")
    
    progress = len(st.session_state.responses) / len(st.session_state.questions)
    st.progress(progress, text="Exam Progress")
    
    for i, q in enumerate(st.session_state.questions):
        st.markdown(f'<div class="q-card"><b>Q{i+1}.</b> {q["q"]}</div>', unsafe_allow_html=True)
        
        sel = st.radio(f"Select Answer {i+1}", q["opt"], key=f"q{i}", index=None)
        if sel:
            st.session_state.responses[i] = sel
            
    st.markdown("---")
    c1, c2 = st.columns(2)
    if c1.button("🏠 Home"):
        st.session_state.page = "home"
        st.rerun()
        
    if c2.button("✅ Submit Exam", type="primary"):
        st.session_state.page = "result"
        st.rerun()

# --- 8. PAGE: RESULT ---
elif st.session_state.page == "result":
    st.balloons()
    score = 0
    total = len(st.session_state.questions)
    
    for i, q in enumerate(st.session_state.questions):
        if st.session_state.responses.get(i) == q["ans"]:
            score += 1
            
    st.markdown(f"""
    <div class="hero-card">
        <h1>Result: {score}/{total}</h1>
        <p>{'Excellent! 🌟' if score > 3 else 'Keep Practicing! 💪'}</p>
    </div>
    """, unsafe_allow_html=True)
    
    for i, q in enumerate(st.session_state.questions):
        user_ans = st.session_state.responses.get(i, "Skipped")
        color = "green" if user_ans == q["ans"] else "red"
        
        with st.expander(f"Q{i+1}: Analysis"):
            st.markdown(f"**Question:** {q['q']}")
            st.markdown(f"**Your Answer:** :{color}[{user_ans}]")
            st.markdown(f"**Correct Answer:** :green[{q['ans']}]")
            st.info(f"💡 Explanation: {q['exp']}")
            
    if st.button("🔄 Start New Test"):
        st.session_state.page = "home"
        st.rerun()
        
