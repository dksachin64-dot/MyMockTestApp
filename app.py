import streamlit as st
import google.generativeai as genai
import json
import random
import time

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Pariksha Pro Ultimate", layout="wide", page_icon="📚")

# API Key (Agar ye expire ho gayi hai to niche wala Database chalega)
GOOGLE_API_KEY = "AIzaSyALMoUhT8s7GYOHexDYrhnMNVT1xqQ4bgE"
genai.configure(api_key=GOOGLE_API_KEY)

# --- 2. CSS STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #f4f6f9; }
    .hero-card {
        background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%);
        padding: 20px; border-radius: 15px; color: white; text-align: center;
        margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .q-card {
        background: white; padding: 20px; border-radius: 12px;
        border-left: 6px solid #00b09b; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 15px; color: #333;
    }
    .result-correct { background-color: #d4edda; padding: 10px; border-radius: 5px; color: #155724; border: 1px solid #c3e6cb; }
    .result-wrong { background-color: #f8d7da; padding: 10px; border-radius: 5px; color: #721c24; border: 1px solid #f5c6cb; }
</style>
""", unsafe_allow_html=True)

# --- 3. EXAM-SPECIFIC DATABASE (High Level) ---
# Jab AI fail hoga, to ye "Asli Exam Level" ke sawal aayenge.

STATIC_DB = {
    "UPSC CSE": [
        {"q": "Consider the following statements regarding the Preamble:\n1. It is not justiciable.\n2. It can be amended.\nWhich is correct?", "opt": ["1 only", "2 only", "Both 1 and 2", "Neither 1 nor 2"], "ans": "Both 1 and 2", "exp": "The Preamble is part of the Constitution, can be amended (Kesavananda Bharati case), but is not enforceable in courts."},
        {"q": "Which Schedule of the Constitution deals with Anti-Defection Law?", "opt": ["9th Schedule", "10th Schedule", "11th Schedule", "12th Schedule"], "ans": "10th Schedule", "exp": "Added by the 52nd Amendment Act, 1985."},
        {"q": "With reference to inflation in India, which is used to measure headline inflation?", "opt": ["WPI", "CPI - Industrial Workers", "CPI - Combined", "GDP Deflator"], "ans": "CPI - Combined", "exp": "RBI uses CPI-Combined as the key measure of inflation."},
        {"q": "The term 'Golden Crescent' is associated with?", "opt": ["Gold Mining", "Opium Trade", "Wheat Production", "Solar Energy"], "ans": "Opium Trade", "exp": "Refers to illicit opium trade regions (Iran, Afghanistan, Pakistan)."},
        {"q": "Right to Privacy is protected under which Article?", "opt": ["Article 19", "Article 21", "Article 14", "Article 25"], "ans": "Article 21", "exp": "Declared a fundamental right in the Puttaswamy Judgment (2017)."},
        {"q": "Who acts as the Chairman of the Rajya Sabha?", "opt": ["President", "Vice-President", "Speaker", "PM"], "ans": "Vice-President", "exp": "The Vice-President is the ex-officio Chairman of Rajya Sabha."},
    ],
    "SSC CGL": [
        {"q": "If x + 1/x = 4, then x² + 1/x² = ?", "opt": ["14", "16", "12", "18"], "ans": "14", "exp": "Formula: (x + 1/x)² - 2 = 16 - 2 = 14."},
        {"q": "A can do a work in 10 days, B in 15 days. Together they finish in?", "opt": ["5 days", "6 days", "8 days", "7 days"], "ans": "6 days", "exp": "Formula: (A*B)/(A+B) = (10*15)/25 = 150/25 = 6."},
        {"q": "Synonym of 'CANDID'?", "opt": ["Frank", "Secretive", "Cruel", "Arrogant"], "ans": "Frank", "exp": "Candid means truthful and straightforward."},
        {"q": "Who was the first female ruler of Delhi Sultanate?", "opt": ["Razia Sultan", "Nur Jahan", "Chand Bibi", "Mumtaz"], "ans": "Razia Sultan", "exp": "She reigned from 1236 to 1240."},
        {"q": "Which instrument measures atmospheric pressure?", "opt": ["Thermometer", "Barometer", "Hygrometer", "Anemometer"], "ans": "Barometer", "exp": "Barometer is used for atmospheric pressure."},
        {"q": "The profit earned after selling an article for Rs. 1754 is same as loss incurred after selling for Rs. 1492. Cost Price?", "opt": ["1623", "1500", "1600", "1580"], "ans": "1623", "exp": "CP = (SP1 + SP2) / 2 = (1754 + 1492) / 2 = 1623."},
    ],
    "NEET UG": [
        {"q": "Which of the following is not a function of the Liver?", "opt": ["Production of Bile", "Detoxification", "Production of Insulin", "Storage of Glycogen"], "ans": "Production of Insulin", "exp": "Insulin is produced by the Pancreas, not the Liver."},
        {"q": "The basic unit of classification is?", "opt": ["Species", "Genus", "Family", "Order"], "ans": "Species", "exp": "Species is the fundamental unit of taxonomy."},
        {"q": "Powerhouse of the cell is?", "opt": ["Nucleus", "Mitochondria", "Ribosome", "Golgi"], "ans": "Mitochondria", "exp": "Site of ATP production."},
        {"q": "Which blood group is the Universal Donor?", "opt": ["A+", "B+", "AB+", "O-"], "ans": "O-", "exp": "O Negative blood can be given to anyone."},
        {"q": "The genetic material of a virus can be?", "opt": ["DNA only", "RNA only", "Both DNA and RNA", "Either DNA or RNA"], "ans": "Either DNA or RNA", "exp": "Viruses contain either DNA or RNA, never both."},
    ],
    "JEE Mains": [
        {"q": "Dimensional formula of Force is?", "opt": ["MLT-2", "ML2T-2", "MLT-1", "M0L0T0"], "ans": "MLT-2", "exp": "Force = Mass × Acceleration = M × LT-2."},
        {"q": "The derivative of sin(x) is?", "opt": ["cos(x)", "-cos(x)", "tan(x)", "sec(x)"], "ans": "cos(x)", "exp": "d/dx(sin x) = cos x."},
        {"q": "Which acts as a Lewis Acid?", "opt": ["NH3", "BF3", "OH-", "H2O"], "ans": "BF3", "exp": "BF3 is electron deficient, so it accepts electrons."},
        {"q": "Value of i^4 (where i is imaginary unit)?", "opt": ["1", "-1", "i", "-i"], "ans": "1", "exp": "i^2 = -1, so i^4 = (-1)*(-1) = 1."},
    ]
}

# --- 4. SESSION MANAGEMENT ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'questions' not in st.session_state: st.session_state.questions = []
if 'responses' not in st.session_state: st.session_state.responses = {}
if 'exam_mode' not in st.session_state: st.session_state.exam_mode = ""

# --- 5. AI GENERATOR (With Intelligent Fallback) ---
def get_questions(exam_name):
    # 1. Try AI Generation
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Generate 10 Hard-Level MCQ questions for {exam_name}.
        Return ONLY valid JSON array. Keys: "q", "opt" (list), "ans", "exp".
        """
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except:
        # 2. AI Failed? Use Exam-Specific Static DB
        # Agar exact match nahi mila to 'General' questions denge
        fallback_qs = STATIC_DB.get(exam_name, STATIC_DB["SSC CGL"]) 
        return random.sample(fallback_qs, min(len(fallback_qs), 10))

# --- 6. PAGE: HOME ---
if st.session_state.page == "home":
    st.markdown("""
    <div class="hero-card">
        <h1>🎓 Pariksha AI Ultimate</h1>
        <p>Real Exam Level Questions | AI + Backup System</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🏛️ UPSC CSE (GS)", use_container_width=True):
            st.session_state.exam_mode = "UPSC CSE"
            st.session_state.questions = get_questions("UPSC CSE")
            st.session_state.responses = {}
            st.session_state.page = "exam"
            st.rerun()
            
        if st.button("🩺 NEET UG (Bio)", use_container_width=True):
            st.session_state.exam_mode = "NEET UG"
            st.session_state.questions = get_questions("NEET UG")
            st.session_state.responses = {}
            st.session_state.page = "exam"
            st.rerun()

    with col2:
        if st.button("📊 SSC CGL (Tier 1)", use_container_width=True):
            st.session_state.exam_mode = "SSC CGL"
            st.session_state.questions = get_questions("SSC CGL")
            st.session_state.responses = {}
            st.session_state.page = "exam"
            st.rerun()

        if st.button("⚙️ JEE Mains (PCM)", use_container_width=True):
            st.session_state.exam_mode = "JEE Mains"
            st.session_state.questions = get_questions("JEE Mains")
            st.session_state.responses = {}
            st.session_state.page = "exam"
            st.rerun()

# --- 7. PAGE: EXAM ---
elif st.session_state.page == "exam":
    st.subheader(f"📝 {st.session_state.exam_mode} Test")
    st.caption("Attempt all questions carefully.")
    
    for i, q in enumerate(st.session_state.questions):
        st.markdown(f'<div class="q-card"><b>Q{i+1}.</b> {q["q"]}</div>', unsafe_allow_html=True)
        sel = st.radio(f"Select Answer:", q["opt"], key=f"q{i}", index=None)
        if sel: st.session_state.responses[i] = sel
    
    st.write("---")
    if st.button("✅ Submit Test", type="primary", use_container_width=True):
        st.session_state.page = "result"
        st.rerun()

# --- 8. PAGE: RESULT ---
elif st.session_state.page == "result":
    score = 0
    total = len(st.session_state.questions)
    for i, q in enumerate(st.session_state.questions):
        if st.session_state.responses.get(i) == q["ans"]: score += 1
            
    st.markdown(f"""
    <div class="hero-card">
        <h2>Result: {score} / {total}</h2>
        <p>{'Excellent! 🌟' if score > total/2 else 'Needs Improvement 📉'}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🔍 Detailed Analysis")
    
    for i, q in enumerate(st.session_state.questions):
        user_ans = st.session_state.responses.get(i, "Not Attempted")
        correct = q['ans']
        
        # Color Logic
        if user_ans == correct:
            css_class = "result-correct"
            status = "✅ Correct"
        else:
            css_class = "result-wrong"
            status = "❌ Incorrect"
            
        st.markdown(f"""
        <div class="{css_class}" style="margin-bottom: 15px;">
            <strong>Q{i+1}: {q['q']}</strong><br>
            <span style="color: #555;">Your Ans: <b>{user_ans}</b> | Correct: <b>{correct}</b></span><br>
            <br>
            <em>💡 Reason: {q['exp']}</em>
        </div>
        """, unsafe_allow_html=True)
        
    if st.button("🏠 Home"):
        st.session_state.page = "home"
        st.rerun()
        
