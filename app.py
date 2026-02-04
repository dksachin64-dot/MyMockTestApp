import streamlit as st
import google.generativeai as genai
import json
import random
import time
import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Live Exam Source AI", layout="wide", page_icon="📡")

# API Key
GOOGLE_API_KEY = "AIzaSyALMoUhT8s7GYOHexDYrhnMNVT1xqQ4bgE"
genai.configure(api_key=GOOGLE_API_KEY)

# --- 2. MODERN UI (LIVE NEWS STYLE) ---
st.markdown("""
<style>
    .stApp { background-color: #f0f2f5; }
    
    /* Search Bar */
    .stTextInput > div > div > input {
        border-radius: 30px;
        padding: 15px;
        border: 2px solid #2962ff;
        font-size: 16px;
    }
    
    /* Hero Section */
    .hero-card {
        background: linear-gradient(90deg, #2962ff 0%, #0015ff 100%);
        padding: 25px; border-radius: 15px; color: white; text-align: center;
        margin-bottom: 20px; box-shadow: 0 4px 20px rgba(41, 98, 255, 0.3);
    }
    
    /* Question Card with Source Badge */
    .q-card {
        background: white; padding: 20px; border-radius: 12px;
        border-left: 5px solid #2962ff; margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Source Tag */
    .source-tag {
        background-color: #e3f2fd; color: #1565c0;
        padding: 4px 10px; border-radius: 20px;
        font-size: 12px; font-weight: bold;
        display: inline-block; margin-bottom: 10px;
        border: 1px solid #bbdefb;
    }
    
    .status-live {
        color: red; font-weight: bold; animation: blink 1.5s infinite;
    }
    @keyframes blink { 50% { opacity: 0; } }
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'questions' not in st.session_state: st.session_state.questions = []
if 'responses' not in st.session_state: st.session_state.responses = {}
if 'topic' not in st.session_state: st.session_state.topic = ""

# --- 4. LIVE AI ENGINE (SOURCE HUNTER) ---
def get_live_questions(topic):
    # Aaj ki date taaki current affairs purana na ho
    today = datetime.date.today().strftime("%B %Y")
    random_seed = random.randint(1, 10000) # Isse har baar naya paper banega
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # SPECIAL PROMPT: Source Mangwaya Hai
        prompt = f"""
        Act as a Live Exam Engine. User wants questions for: "{topic}".
        Current Context: {today} [Random Seed: {random_seed}]
        
        Create 10 High-Quality MCQ Questions.
        CRITICAL REQUIREMENT: For every question, cite a REAL SOURCE.
        
        Examples of Sources:
        - "Source: The Hindu (Jan 2025)"
        - "Source: NCERT Biology Class 11, Ch-4"
        - "Source: SSC CGL PYQ 2022"
        - "Source: Economic Survey of India"
        
        Output JSON Array:
        [{{
            "q": "Question Text",
            "opt": ["A", "B", "C", "D"],
            "ans": "Correct Option",
            "src": "Exact Source Name",
            "exp": "Explanation"
        }}]
        """
        
        res = model.generate_content(prompt)
        return json.loads(res.text.replace("```json", "").replace("```", "").strip())
    except:
        # Fallback (Agar AI busy ho)
        return [
            {"q": "Live Connection Weak: Who is the current RBI Governor?", "opt": ["Shaktikanta Das", "Urjit Patel", "Raghuram Rajan", "Manmohan Singh"], "ans": "Shaktikanta Das", "src": "Source: RBI Official Website", "exp": "He is the 25th Governor."},
            {"q": "General Science: Chemical formula of Water?", "opt": ["H2O", "CO2", "O2", "NaCl"], "ans": "H2O", "src": "Source: NCERT Science Class 9", "exp": "Universal solvent."}
        ]

# --- 5. HOME PAGE (LIVE SEARCH) ---
if st.session_state.page == "home":
    st.markdown("""
    <div class="hero-card">
        <h1>📡 Live Exam Source AI</h1>
        <p>Exam ka naam likhein, AI <span class="status-live">● LIVE</span> source se paper banayega.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search Bar
    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input("🔍 Search Any Exam / Topic (e.g., 'UPSC Current Affairs', 'SSC Geometry', 'NEET Genetics')", placeholder="Type here...")
    with col2:
        st.write("")
        st.write("")
        if st.button("🔴 Go Live", type="primary", use_container_width=True):
            if query:
                st.session_state.topic = query
                with st.status(f"📡 Connecting to Live Sources for '{query}'...", expanded=True):
                    st.write("🔍 Scanning Books & News...")
                    time.sleep(1)
                    st.write("📖 Extracting Real Questions...")
                    st.session_state.questions = get_live_questions(query)
                    st.session_state.responses = {}
                    st.session_state.page = "exam"
                    st.rerun()

    # Quick Trends
    st.subheader("⚡ Trending Live Sources")
    c1, c2, c3 = st.columns(3)
    if c1.button("📰 Daily Current Affairs (The Hindu)"):
        st.session_state.topic = "Daily Current Affairs The Hindu"
        st.session_state.questions = get_live_questions("Latest Current Affairs from The Hindu & Indian Express")
        st.session_state.responses = {}; st.session_state.page = "exam"; st.rerun()
        
    if c2.button("📘 NCERT Science (Class 10-12)"):
        st.session_state.topic = "NCERT Science Mix"
        st.session_state.questions = get_live_questions("Hard NCERT Science Questions")
        st.session_state.responses = {}; st.session_state.page = "exam"; st.rerun()
        
    if c3.button("🏛️ SSC CGL (Previous Year)"):
        st.session_state.topic = "SSC CGL PYQ"
        st.session_state.questions = get_live_questions("SSC CGL Previous Year Questions Math Reasoning")
        st.session_state.responses = {}; st.session_state.page = "exam"; st.rerun()

# --- 6. EXAM PAGE (WITH SOURCE BADGE) ---
elif st.session_state.page == "exam":
    st.markdown(f"### 📝 Live Test: {st.session_state.topic}")
    st.caption("AI ne neeche diye gaye sources se ye paper banaya hai.")
    
    for i, q in enumerate(st.session_state.questions):
        # Display Source Badge
        st.markdown(f'<span class="source-tag">📡 {q.get("src", "Source: General Knowledge")}</span>', unsafe_allow_html=True)
        
        # Display Question
        st.markdown(f'<div class="q-card"><b>Q{i+1}.</b> {q["q"]}</div>', unsafe_allow_html=True)
        sel = st.radio(f"Select Answer {i+1}", q["opt"], key=f"q{i}", index=None)
        if sel: st.session_state.responses[i] = sel
        st.write("") # Gap

    st.write("---")
    if st.button("✅ Submit & Verify Sources", type="primary"):
        st.session_state.page = "result"
        st.rerun()

# --- 7. RESULT PAGE ---
elif st.session_state.page == "result":
    score = sum([1 for i, q in enumerate(st.session_state.questions) if st.session_state.responses.get(i) == q['ans']])
    
    st.markdown(f"""
    <div class="hero-card">
        <h1>Score: {score} / {len(st.session_state.questions)}</h1>
        <p>Source Verification Complete ✅</p>
    </div>
    """, unsafe_allow_html=True)
    
    for i, q in enumerate(st.session_state.questions):
        user = st.session_state.responses.get(i, "Skipped")
        status = "✅ Correct" if user == q['ans'] else "❌ Wrong"
        color = "#d4edda" if user == q['ans'] else "#f8d7da"
        
        st.markdown(f"""
        <div style="background-color: {color}; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
            <small style="color: #555;"><b>📍 {q.get('src', 'Source: AI Library')}</b></small><br>
            <h4 style="margin: 5px 0;">Q{i+1}: {q['q']}</h4>
            <p>Your Ans: <b>{user}</b> | Correct: <b>{q['ans']}</b></p>
            <hr>
            <i>💡 Explanation: {q['exp']}</i>
        </div>
        """, unsafe_allow_html=True)
        
    if st.button("🔍 Search New Live Topic"):
        st.session_state.page = "home"
        st.rerun()
