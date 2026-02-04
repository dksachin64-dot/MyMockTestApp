import streamlit as st
import google.generativeai as genai
import json
import random
import time

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="World Exam Library AI", layout="wide", page_icon="🌍")

# API Key
GOOGLE_API_KEY = "AIzaSyALMoUhT8s7GYOHexDYrhnMNVT1xqQ4bgE"
genai.configure(api_key=GOOGLE_API_KEY)

# --- 2. CSS STYLING (World Class UI) ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    
    /* Search Bar Style */
    .stTextInput > div > div > input {
        border-radius: 25px;
        padding: 15px;
        border: 2px solid #4facfe;
        font-size: 18px;
    }
    
    .hero-card {
        background: linear-gradient(135deg, #00f260 0%, #0575E6 100%);
        padding: 30px; border-radius: 15px; text-align: center;
        margin-bottom: 30px; box-shadow: 0 0 20px rgba(0,242,96, 0.4);
    }
    
    .q-card {
        background: #1f2937; padding: 20px; border-radius: 12px;
        border-left: 5px solid #00f260; margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    .result-correct { border: 1px solid #00f260; background: rgba(0,242,96, 0.1); padding: 10px; border-radius: 8px; }
    .result-wrong { border: 1px solid #ff4b1f; background: rgba(255,75,31, 0.1); padding: 10px; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'questions' not in st.session_state: st.session_state.questions = []
if 'responses' not in st.session_state: st.session_state.responses = {}
if 'exam_title' not in st.session_state: st.session_state.exam_title = ""

# --- 4. UNIVERSAL AI ENGINE (Duniya ka koi bhi exam) ---
def get_universal_paper(exam_query):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # PROMPT: Ye AI ko kisi bhi exam ka expert bana deta hai
        prompt = f"""
        Act as a Global Examination Setter.
        The user wants a Mock Test for: "{exam_query}".
        
        1. Identify the country and standard of this exam.
        2. Create 10 High-Quality Multiple Choice Questions based on its REAL syllabus.
        3. If it's a language exam (IELTS/TOEFL), focus on Grammar/Vocab.
        4. If it's Math/Science (JEE/SAT), focus on numericals.
        
        Output strictly as JSON:
        [{{"q": "Question", "opt": ["A", "B", "C", "D"], "ans": "Correct Option Text", "exp": "Explanation"}}]
        """
        
        res = model.generate_content(prompt)
        text = res.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except:
        # Fallback (Agar naam galat ho ya AI fail ho)
        return [
            {"q": "AI Connection Issue: What is the capital of the World?", "opt": ["London", "New York", "No Capital", "Paris"], "ans": "No Capital", "exp": "The world has no single capital."},
            {"q": "General Logic: 2 + 2 * 2 = ?", "opt": ["6", "8", "4", "10"], "ans": "6", "exp": "BODMAS Rule: Multiply first."}
        ]

# --- 5. PAGE: HOME (SEARCH ENGINE) ---
if st.session_state.page == "home":
    st.markdown("""
    <div class="hero-card">
        <h1>🌍 World Exam Library AI</h1>
        <p>Type ANY Exam Name (e.g., SAT USA, UPSC India, Gaokao China)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # --- SEARCH BAR ---
    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input("🔍 Search Exam (Ex: 'Hardest JEE Math', 'IELTS English', 'USMLE Medical')", placeholder="Type exam name here...")
    with col2:
        st.write("") # Spacer
        st.write("") 
        if st.button("🚀 Generate Test", type="primary", use_container_width=True):
            if query:
                st.session_state.exam_title = query
                with st.status(f"🌎 Connecting to Global Library for '{query}'...", expanded=True):
                    st.write("🧠 Analyzing Exam Pattern...")
                    time.sleep(1)
                    st.write("✍️ Drafting Questions...")
                    st.session_state.questions = get_universal_paper(query)
                    st.session_state.responses = {}
                    st.session_state.page = "exam"
                    st.rerun()

    # --- POPULAR SUGGESTIONS ---
    st.markdown("### 🔥 Popular Across the World")
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("🇺🇸 SAT (Scholastic Aptitude)"):
        st.session_state.exam_title = "SAT USA Math & English"
        st.session_state.questions = get_universal_paper("SAT USA Math & English")
        st.session_state.responses = {}; st.session_state.page = "exam"; st.rerun()
        
    if c2.button("🇬🇧 GRE (Graduate Record)"):
        st.session_state.exam_title = "GRE Verbal & Quant"
        st.session_state.questions = get_universal_paper("GRE Verbal & Quant")
        st.session_state.responses = {}; st.session_state.page = "exam"; st.rerun()
        
    if c3.button("🇮🇳 UPSC CSE (India)"):
        st.session_state.exam_title = "UPSC CSE General Studies"
        st.session_state.questions = get_universal_paper("UPSC CSE General Studies")
        st.session_state.responses = {}; st.session_state.page = "exam"; st.rerun()
        
    if c4.button("🇨🇳 Gaokao (China Physics)"):
        st.session_state.exam_title = "Gaokao Physics Hard"
        st.session_state.questions = get_universal_paper("Gaokao Physics Hard")
        st.session_state.responses = {}; st.session_state.page = "exam"; st.rerun()

# --- 6. PAGE: EXAM ---
elif st.session_state.page == "exam":
    st.markdown(f"## 📝 Exam: {st.session_state.exam_title}")
    st.progress(len(st.session_state.responses)/len(st.session_state.questions))
    
    for i, q in enumerate(st.session_state.questions):
        st.markdown(f'<div class="q-card"><b>Q{i+1}.</b> {q["q"]}</div>', unsafe_allow_html=True)
        sel = st.radio(f"Select Answer {i+1}", q["opt"], key=f"q{i}", index=None)
        if sel: st.session_state.responses[i] = sel
        
    st.write("---")
    if st.button("✅ Submit & Check Global Rank", type="primary"):
        st.session_state.page = "result"
        st.rerun()

# --- 7. PAGE: RESULT ---
elif st.session_state.page == "result":
    score = sum([1 for i, q in enumerate(st.session_state.questions) if st.session_state.responses.get(i) == q['ans']])
    
    st.markdown(f"""
    <div class="hero-card">
        <h1>Score: {score} / {len(st.session_state.questions)}</h1>
        <p>Global Standard Assessment Completed</p>
    </div>
    """, unsafe_allow_html=True)
    
    for i, q in enumerate(st.session_state.questions):
        user = st.session_state.responses.get(i, "Skipped")
        css = "result-correct" if user == q['ans'] else "result-wrong"
        status = "✅ Correct" if user == q['ans'] else "❌ Wrong"
        
        st.markdown(f"""
        <div class="{css}">
            <b>Q{i+1}: {q['q']}</b><br>
            Your Ans: {user} | Correct: <b>{q['ans']}</b><br>
            <small>{status}</small><br>
            <i>💡 Analysis: {q['exp']}</i>
        </div><br>
        """, unsafe_allow_html=True)
        
    if st.button("🔍 Search Another Exam"):
        st.session_state.page = "home"
        st.rerun()
    
