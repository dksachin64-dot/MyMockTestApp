import streamlit as st
import google.generativeai as genai
import json
import time

# --- 1. CONFIGURATION & SETUP ---
st.set_page_config(page_title="India Exam Portal Pro", layout="wide", page_icon="🎓")

# Aapki API Key (Security Warning: Future mein ise chupana behtar hai)
GOOGLE_API_KEY = "AIzaSyALMoUhT8s7GYOHexDYrhnMNVT1xqQ4bgE"
genai.configure(api_key=GOOGLE_API_KEY)

# --- 2. ADVANCED CSS (HIGH-TECH LOOK) ---
st.markdown("""
<style>
    /* Main Background Clean Look */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Question Card Styling (Shadow & Radius) */
    .question-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #4CAF50;
        margin-bottom: 20px;
    }
    
    /* Timer Style */
    .timer-box {
        font-size: 20px;
        font-weight: bold;
        color: #d9534f;
        background: #fff;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #ddd;
        text-align: center;
    }
    
    /* Palette Buttons */
    .palette-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
    }
    .p-btn {
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        cursor: pointer;
        transition: 0.3s;
    }
    .status-visited { background: white; border: 1px solid #333; color: black; }
    .status-answered { background: #28a745; color: white; border: none; box-shadow: 0 2px 5px rgba(40,167,69,0.3); }
    .status-review { background: #6f42c1; color: white; border: none; }
    
    /* Custom Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #eee;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE MANAGEMENT ---
if 'questions' not in st.session_state: st.session_state.questions = []
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'responses' not in st.session_state: st.session_state.responses = {}
if 'status_map' not in st.session_state: st.session_state.status_map = {}
if 'exam_active' not in st.session_state: st.session_state.exam_active = False

# --- 4. EXTENSIVE EXAM LIST (INDIA) ---
ALL_EXAMS = {
    "🏆 Trending Now": ["SSC CGL - Tier 1", "SSC GD Constable", "UP Police Constable", "RRB ALP (Railway)"],
    "engineering": ["JEE Mains - Physics", "JEE Mains - Chemistry", "JEE Mains - Maths", "GATE - CS", "BITSAT"],
    "medical": ["NEET - Biology", "NEET - Physics", "NEET - Chemistry", "AIIMS Nursing"],
    "government": ["UPSC CSE - Prelims (GS)", "SSC CHSL", "SSC MTS", "IB Intelligence Bureau"],
    "defence": ["NDA - Mathematics", "NDA - GAT", "CDS - General Knowledge", "AFCAT"],
    "banking": ["SBI PO - Quant", "IBPS Clerk - Reasoning", "RBI Grade B"],
    "teaching": ["CTET - Paper 1", "UGC NET - Teaching Aptitude"],
    "law_mgmt": ["CLAT - Legal Reasoning", "CAT - Verbal Ability", "IPMAT"]
}

# --- 5. AI ENGINE (BRAIN) ---
def generate_paper(exam_name):
    model = genai.GenerativeModel('gemini-1.5-flash')
    with st.spinner(f"🚀 AI is designing a unique paper for {exam_name}..."):
        prompt = f"""
        Act as an expert examiner for Indian Competitive Exams.
        Create a mock test of 10 high-quality questions for: {exam_name}.
        Difficulty: Mixed (Easy to Hard).
        
        STRICT JSON OUTPUT FORMAT:
        [
            {{
                "id": 1,
                "q": "Question text here?",
                "opt": ["Option A", "Option B", "Option C", "Option D"],
                "ans": "Option A",
                "exp": "Explanation in Hinglish (Mix of Hindi-English) for easy understanding."
            }}
        ]
        """
        try:
            res = model.generate_content(prompt)
            clean_text = res.text.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_text)
            return data
        except:
            st.error("⚠️ AI Server Busy. Please click 'Start' again.")
            return []

# --- 6. MAIN APP UI ---

# Sidebar Navigation
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2997/2997235.png", width=60)
    st.title("Pariksha AI Pro")
    st.markdown("---")
    
    # Category Filter
    category = st.selectbox("📚 Select Category", list(ALL_EXAMS.keys()), format_func=lambda x: x.upper())
    
    # Specific Exam Selection
    selected_exam = st.selectbox("📝 Select Exam", ALL_EXAMS[category])
    
    st.markdown("---")
    if st.button("🚀 START NEW TEST", type="primary", use_container_width=True):
        st.session_state.questions = generate_paper(selected_exam)
        st.session_state.current_idx = 0
        st.session_state.responses = {}
        st.session_state.status_map = {i: "visited" for i in range(10)}
        st.session_state.exam_active = True
        st.rerun()

    st.info("💡 Pro Tip: Phone ko Landscape mode mein pakdein best view ke liye.")

# Main Screen Logic
if st.session_state.exam_active and st.session_state.questions:
    q_list = st.session_state.questions
    curr = st.session_state.current_idx
    q_data = q_list[curr]
    
    # --- TOP HEADER (Timer & Info) ---
    c1, c2, c3 = st.columns([2, 1, 1])
    c1.subheader(f"Exam: {selected_exam}")
    c2.progress((curr + 1) / len(q_list), text=f"Progress: {curr+1}/{len(q_list)}")
    c3.markdown('<div class="timer-box">⏱️ 15:00 LEFT</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # --- SPLIT SCREEN UI ---
    col_q, col_p = st.columns([3, 1])
    
    # LEFT: Question Area
    with col_q:
        st.markdown(f"""
        <div class="question-card">
            <h4>Q{curr+1}: {q_data['q']}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Options logic
        user_sel = st.session_state.responses.get(curr, None)
        choice = st.radio("Select your answer:", q_data['opt'], index=q_data['opt'].index(user_sel) if user_sel else None, key=f"q_{curr}")
        
        st.write("")
        # Navigation Buttons
        b1, b2, b3 = st.columns(3)
        if b1.button("⬅️ Previous") and curr > 0:
            st.session_state.current_idx -= 1
            st.rerun()
            
        if b2.button("💾 Save & Next", type="primary"):
            if choice:
                st.session_state.responses[curr] = choice
                st.session_state.status_map[curr] = "answered"
            else:
                st.session_state.status_map[curr] = "visited"
            
            if curr < len(q_list) - 1:
                st.session_state.current_idx += 1
                st.rerun()
                
        if b3.button("🟣 Mark Review"):
            st.session_state.status_map[curr] = "review"
            if curr < len(q_list) - 1:
                st.session_state.current_idx += 1
                st.rerun()

    # RIGHT: Question Palette
    with col_p:
        st.markdown("**Question Palette**")
        
        # Grid Display using HTML
        html_grid = '<div class="palette-grid">'
        for i in range(len(q_list)):
            status = st.session_state.status_map.get(i, "visited")
            border = "border: 2px solid blue;" if i == curr else ""
            html_grid += f'<div class="p-btn status-{status}" style="{border}">{i+1}</div>'
        html_grid += '</div>'
        st.markdown(html_grid, unsafe_allow_html=True)
        
        st.write("---")
        
        # Submit Logic
        if st.button("✅ SUBMIT EXAM", type="primary", use_container_width=True):
            st.session_state.exam_active = False
            st.rerun()

# --- 7. RESULT SCREEN (After Submit) ---
elif not st.session_state.exam_active and st.session_state.questions:
    st.balloons()
    st.success("🎉 Exam Submitted Successfully!")
    
    score = 0
    with st.expander("📊 Click to View Detailed Analysis", expanded=True):
        for i, q in enumerate(st.session_state.questions):
            user_ans = st.session_state.responses.get(i, "Not Answered")
            correct_ans = q['ans']
            
            if user_ans == correct_ans:
                score += 1
                st.markdown(f"✅ **Q{i+1}: Correct**")
            else:
                st.markdown(f"❌ **Q{i+1}: Incorrect**")
                st.caption(f"Your Ans: {user_ans} | Correct: {correct_ans}")
            
            st.info(f"💡 Explanation: {q['exp']}")
            st.write("---")
            
    st.metric("FINAL SCORE", f"{score} / {len(st.session_state.questions)}")
    
    if st.button("Start New Test"):
        st.session_state.questions = []
        st.rerun()

else:
    # Welcome Screen
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h1>👋 Welcome to Pariksha AI Pro</h1>
        <p>Select a category from the sidebar to start your personalized mock test.</p>
    </div>
    """, unsafe_allow_html=True)
        
