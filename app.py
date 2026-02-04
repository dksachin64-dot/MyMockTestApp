import streamlit as st
import google.generativeai as genai
import json

# --- SETUP ---
st.set_page_config(layout="wide", page_title="India Exam Portal")

# AAPKI API KEY (Maine aapke screenshot se yahan daal di hai)
GOOGLE_API_KEY = "AIzaSyB5...4bgE"  # Yahan apni poori key check kar lena

try:
    genai.configure(api_key=GOOGLE_API_KEY)
except:
    st.error("API Key missing! Code mein key dalein.")

# --- CSS FOR REALISTIC CBT LOOK ---
st.markdown("""
<style>
    .block-container {padding-top: 1rem; padding-bottom: 0rem;}
    .question-area {
        background-color: #ffffff; padding: 20px; border: 1px solid #ddd;
        height: 70vh; overflow-y: scroll; border-radius: 5px;
    }
    .palette-area {
        background-color: #e6f7ff; padding: 10px; border: 1px solid #b3e0ff;
        height: 70vh; overflow-y: scroll;
    }
    .q-btn {
        display: inline-block; width: 40px; height: 35px; margin: 4px;
        text-align: center; border: 1px solid #333; border-radius: 4px;
        padding-top: 5px; font-weight: bold; cursor: pointer;
    }
    .status-not-visited { background-color: #ffffff; color: black; }
    .status-answered { background-color: #28a745; color: white; border-color: #28a745; }
    .status-not-answered { background-color: #dc3545; color: white; border-color: #dc3545; }
    .status-review { background-color: #6f42c1; color: white; border-color: #6f42c1; }
    .current-q { border: 2px solid blue !important; box-shadow: 0 0 5px blue; }
</style>
""", unsafe_allow_html=True)

# --- STATE ---
if 'q_list' not in st.session_state: st.session_state.q_list = []
if 'idx' not in st.session_state: st.session_state.idx = 0
if 'answers' not in st.session_state: st.session_state.answers = {}
if 'status' not in st.session_state: st.session_state.status = {}

# --- AI FUNCTION ---
def get_exam(subject):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Create 10 hard multiple choice questions for {subject} (Indian Exam Level).
    Strictly JSON format: [{{"q": "Question text", "opt": ["A) ..", "B) ..", "C) ..", "D) .."], "ans": "A) .."}}]
    """
    try:
        res = model.generate_content(prompt)
        text = res.text.replace("```json", "").replace("```", "").strip()
        st.session_state.q_list = json.loads(text)
        # Init status
        for i in range(len(st.session_state.q_list)):
            st.session_state.status[i] = "not-visited"
    except:
        st.error("AI Error. Try again.")

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/8/81/Ashoka_Chakra.svg", width=50)
    st.title("Exam Portal")
    sub = st.selectbox("Subject", ["SSC CGL - English", "NEET - Biology", "JEE - Physics"])
    if st.button("Start New Exam", type="primary"):
        st.session_state.q_list = []
        st.session_state.answers = {}
        st.session_state.idx = 0
        get_exam(sub)

# --- MAIN UI ---
if st.session_state.q_list:
    # Top Bar
    c1, c2 = st.columns([3, 1])
    c1.subheader(f"Subject: {sub}")
    c2.info("⏳ Time Left: 15:00")
    
    col_q, col_p = st.columns([3, 1])
    
    # Left: Question
    with col_q:
        st.markdown('<div class="question-area">', unsafe_allow_html=True)
        curr = st.session_state.idx
        q = st.session_state.q_list[curr]
        
        st.markdown(f"**Q.{curr+1}: {q['q']}**")
        
        # Options
        sel = st.session_state.answers.get(curr, None)
        choice = st.radio("Choose Option:", q['opt'], index=q['opt'].index(sel) if sel else None, key=f"r_{curr}")
        
        st.write("---")
        b1, b2, b3 = st.columns(3)
        if b1.button("Save & Next ➡️"):
            if choice:
                st.session_state.answers[curr] = choice
                st.session_state.status[curr] = "answered"
            else:
                st.session_state.status[curr] = "not-answered"
            if curr < len(st.session_state.q_list)-1: st.session_state.idx += 1
            st.rerun()
            
        if b2.button("Mark Review 🟣"):
            st.session_state.status[curr] = "review"
            if curr < len(st.session_state.q_list)-1: st.session_state.idx += 1
            st.rerun()
            
        if b3.button("⬅️ Back") and curr > 0:
            st.session_state.idx -= 1
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)

    # Right: Palette
    with col_p:
        st.markdown('<div class="palette-area">', unsafe_allow_html=True)
        st.write("**Question Palette**")
        html = "<div>"
        for i in range(len(st.session_state.q_list)):
            stat = st.session_state.status.get(i, "not-visited")
            border = "current-q" if i == st.session_state.idx else ""
            html += f"<div class='q-btn status-{stat} {border}'>{i+1}</div>"
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)
        
        st.write("")
        if st.button("SUBMIT PAPER 🔴", type="primary"):
            st.success("Exam Submitted!")
            st.balloons()
            # Score calc logic can go here
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("👈 Click 'Start New Exam' from sidebar")
          
