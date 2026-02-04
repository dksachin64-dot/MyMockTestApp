import streamlit as st
import google.generativeai as genai
import json
import time
import random

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Pariksha Pro Ultimate", layout="wide", page_icon="🇮🇳")

# API Key
GOOGLE_API_KEY = "AIzaSyALMoUhT8s7GYOHexDYrhnMNVT1xqQ4bgE"
genai.configure(api_key=GOOGLE_API_KEY)

# --- 2. CSS STYLING (Results Fixed) ---
st.markdown("""
<style>
    .stApp { background-color: #f4f6f9; }
    .hero-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 20px; border-radius: 15px; color: white; text-align: center;
        margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .q-card {
        background: white; padding: 20px; border-radius: 12px;
        border-left: 6px solid #2a5298; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .result-correct { background-color: #d4edda; padding: 10px; border-radius: 5px; color: #155724; }
    .result-wrong { background-color: #f8d7da; padding: 10px; border-radius: 5px; color: #721c24; }
</style>
""", unsafe_allow_html=True)

# --- 3. STATE ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'questions' not in st.session_state: st.session_state.questions = []
if 'responses' not in st.session_state: st.session_state.responses = {}

# --- 4. HUGE BACKUP DATABASE (Fresh Questions) ---
BACKUP_DB = [
    {"q": "Current Affairs: Who won the T20 World Cup 2024?", "opt": ["India", "Australia", "England", "SA"], "ans": "India", "exp": "India defeated South Africa in the final."},
    {"q": "History: Who was the first Governor-General of Bengal?", "opt": ["Warren Hastings", "Clive", "Canning", "Dalhousie"], "ans": "Warren Hastings", "exp": "He became Governor-General in 1773."},
    {"q": "Polity: Which Article deals with Untouchability?", "opt": ["Article 17", "Article 14", "Article 21", "Article 32"], "ans": "Article 17", "exp": "Abolition of Untouchability."},
    {"q": "Geography: Which river is known as Dakshin Ganga?", "opt": ["Godavari", "Krishna", "Kaveri", "Mahanadi"], "ans": "Godavari", "exp": "Godavari is the longest river in Peninsular India."},
    {"q": "Science: Powerhouse of the cell?", "opt": ["Mitochondria", "Nucleus", "Ribosome", "DNA"], "ans": "Mitochondria", "exp": "It generates ATP."},
    {"q": "Economy: Who calculates GDP in India?", "opt": ["NSO", "RBI", "Finance Ministry", "SEBI"], "ans": "NSO", "exp": "National Statistical Office calculates GDP."},
    {"q": "Current Affairs: Host of G20 Summit 2023?", "opt": ["India", "Brazil", "USA", "China"], "ans": "India", "exp": "Held in New Delhi."},
    {"q": "History: Battle of Plassey was fought in?", "opt": ["1757", "1764", "1857", "1947"], "ans": "1757", "exp": "Between British and Siraj-ud-Daulah."},
    {"q": "Polity: Fundamental Duties were added by?", "opt": ["42nd Amendment", "44th Amendment", "86th Amendment", "None"], "ans": "42nd Amendment", "exp": "Added in 1976 on Swaran Singh Committee recommendation."},
    {"q": "Geography: Largest freshwater lake in India?", "opt": ["Wular Lake", "Chilika", "Sambhar", "Dal"], "ans": "Wular Lake", "exp": "Located in J&K."},
    {"q": "Science: Chemical name of Vitamin C?", "opt": ["Ascorbic Acid", "Retinol", "Thiamine", "Citric Acid"], "ans": "Ascorbic Acid", "exp": "Deficiency causes Scurvy."},
    {"q": "Current Affairs: New CEO of YouTube?", "opt": ["Neal Mohan", "Sundar Pichai", "Satya Nadella", "Elon Musk"], "ans": "Neal Mohan", "exp": "He is an Indian-American executive."},
    {"q": "History: Who founded the Maurya Empire?", "opt": ["Chandragupta Maurya", "Ashoka", "Bindusara", "Porus"], "ans": "Chandragupta Maurya", "exp": "With the help of Chanakya."},
    {"q": "Polity: Minimum age for President of India?", "opt": ["35 years", "30 years", "25 years", "40 years"], "ans": "35 years", "exp": "Mentioned in Article 58."},
    {"q": "Geography: Highest peak in South India?", "opt": ["Anamudi", "Doda Betta", "Mahendragiri", "Kalsubai"], "ans": "Anamudi", "exp": "Located in Kerala."},
]

# --- 5. AI ENGINE (Hybrid Mode) ---
def get_exam_paper(exam_name):
    # Try getting fresh questions from AI
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Generate 20 Multiple Choice Questions for {exam_name} Exam.
        Topics: Current Affairs, History, Polity, Science, Reasoning.
        Format: JSON Array only.
        Keys: "q", "opt" (4 options), "ans" (exact option text), "exp" (explanation).
        """
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(text)
        return data
    except:
        # AGAR AI FAIL HUA -> To Backup DB se Random sawal uthao
        return random.sample(BACKUP_DB, min(len(BACKUP_DB), 10))

# --- 6. PAGE: HOME ---
if st.session_state.page == "home":
    st.markdown("""
    <div class="hero-card">
        <h1>🇮🇳 Pariksha AI Ultimate</h1>
        <p>Select Exam | 20 Questions | Instant Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    exams = ["UPSC CSE", "SSC CGL", "Railways NTPC", "Banking PO", "NEET UG", "JEE Mains"]
    cols = st.columns(2)
    
    for i, exam in enumerate(exams):
        with cols[i % 2]:
            if st.button(f"🚀 Start {exam}", use_container_width=True):
                with st.status("⚙️ Paper Set Ho Raha Hai...", expanded=True):
                    st.write("Fetching Real Questions...")
                    time.sleep(1)
                    st.write("Adding Current Affairs...")
                    st.session_state.questions = get_exam_paper(exam)
                    st.session_state.responses = {}
                    st.session_state.page = "exam"
                    st.rerun()

# --- 7. PAGE: EXAM (LIVE) ---
elif st.session_state.page == "exam":
    st.progress(len(st.session_state.responses) / len(st.session_state.questions))
    
    # Show Questions
    for i, q in enumerate(st.session_state.questions):
        st.markdown(f'<div class="q-card"><b>Q{i+1}.</b> {q["q"]}</div>', unsafe_allow_html=True)
        sel = st.radio(f"Select Answer for Q{i+1}", q["opt"], key=f"q{i}", index=None)
        if sel: st.session_state.responses[i] = sel
    
    st.markdown("---")
    if st.button("✅ Submit Paper (Result Dekhein)", type="primary", use_container_width=True):
        st.session_state.page = "result"
        st.rerun()

# --- 8. PAGE: RESULT (CLEAR ANALYSIS) ---
elif st.session_state.page == "result":
    st.balloons()
    
    score = 0
    total = len(st.session_state.questions)
    for i, q in enumerate(st.session_state.questions):
        if st.session_state.responses.get(i) == q["ans"]: score += 1
            
    st.markdown(f"""
    <div class="hero-card">
        <h1>Result: {score} / {total}</h1>
        <p>{'Pass 🎉' if score > total/2 else 'Fail ❌'}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed Analysis - OPEN BY DEFAULT
    st.subheader("📝 Question-wise Analysis")
    
    for i, q in enumerate(st.session_state.questions):
        user_ans = st.session_state.responses.get(i, "Not Attempted")
        correct = q['ans']
        
        # Color coding result
        if user_ans == correct:
            status = "✅ Sahi Jawab"
            color_class = "result-correct"
        else:
            status = "❌ Galat Jawab"
            color_class = "result-wrong"
            
        # Display Box
        st.markdown(f"""
        <div class="{color_class}" style="margin-bottom: 10px; border:1px solid #ddd;">
            <strong>Q{i+1}: {q['q']}</strong><br>
            Your Answer: <b>{user_ans}</b> | Correct Answer: <b>{correct}</b><br>
            <em>{status}</em>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander(f"💡 Explanation for Q{i+1}"):
            st.info(q['exp'])
            
    if st.button("🔄 Naya Test Dein (New Questions)"):
        st.session_state.page = "home"
        st.rerun()
        
