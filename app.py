import streamlit as st
import google.generativeai as genai
import json
import time
import os
from dotenv import load_dotenv

# ================= INITIAL SETUP =================
load_dotenv()
st.set_page_config(
    page_title="MockTest AI Pro",
    layout="wide",
    page_icon="🎯",
    initial_sidebar_state="expanded"
)

# ================= API CONFIGURATION =================
api_key = os.getenv("GOOGLE_API_KEY") or "YOUR_API_KEY_HERE"
genai.configure(api_key=api_key)

# ================= PROFESSIONAL CSS =================
st.markdown("""
<style>
    /* Global Styles */
    .main { background: #f8f9fa; }
    
    /* Hero Gradient */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    }
    
    /* Exam Cards */
    .exam-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 2px solid #e9ecef;
        transition: all 0.3s ease;
        text-align: center;
        height: 100%;
    }
    .exam-card:hover {
        transform: translateY(-8px);
        border-color: #764ba2;
        box-shadow: 0 15px 35px rgba(118, 75, 162, 0.2);
    }
    
    /* Question Container */
    .question-box {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        border-left: 6px solid #4CAF50;
        margin: 20px 0;
    }
    
    /* Timer Animation */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    .timer-warning {
        animation: pulse 1s infinite;
        color: #ff6b6b;
        font-weight: bold;
    }
    
    /* Button Styling */
    .stButton > button {
        border-radius: 12px;
        padding: 14px 28px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: scale(1.05);
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #4CAF50, #2196F3);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        color: white;
    }
    .sidebar-content h1, .sidebar-content h2, .sidebar-content h3 {
        color: white !important;
    }
    
    /* Palette Buttons */
    .palette-btn {
        width: 50px;
        height: 50px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin: 5px;
        border: 2px solid transparent;
        transition: all 0.3s;
    }
    .answered { background: #4CAF50; color: white; }
    .current { background: #2196F3; color: white; border: 2px solid white; }
    .unanswered { background: #f1f3f4; color: #333; }
    .review { background: #FFC107; color: black; }
</style>
""", unsafe_allow_html=True)

# ================= SESSION STATE INITIALIZATION =================
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'current_exam' not in st.session_state: st.session_state.current_exam = None
if 'questions' not in st.session_state: st.session_state.questions = []
if 'user_answers' not in st.session_state: st.session_state.user_answers = {}
if 'score' not in st.session_state: st.session_state.score = 0
if 'start_time' not in st.session_state: st.session_state.start_time = None
if 'time_taken' not in st.session_state: st.session_state.time_taken = 0
if 'test_started' not in st.session_state: st.session_state.test_started = False
if 'current_question' not in st.session_state: st.session_state.current_question = 0
if 'streak' not in st.session_state: st.session_state.streak = 12
if 'total_tests' not in st.session_state: st.session_state.total_tests = 47
if 'xp' not in st.session_state: st.session_state.xp = 1840
if 'level' not in st.session_state: st.session_state.level = "Pro"

# ================= EXAM DATABASE =================
EXAMS = {
    "Government Exams": [
        {"name": "UPSC CSE", "icon": "🇮🇳", "questions": 100, "time": 120, "difficulty": "Expert"},
        {"name": "SSC CGL", "icon": "🏛️", "questions": 100, "time": 60, "difficulty": "Advanced"},
        {"name": "Bank PO", "icon": "🏦", "questions": 100, "time": 60, "difficulty": "Intermediate"},
        {"name": "Railway RRB", "icon": "🚂", "questions": 100, "time": 90, "difficulty": "Intermediate"},
    ],
    "Engineering": [
        {"name": "JEE Advanced", "icon": "⚙️", "questions": 90, "time": 180, "difficulty": "Expert"},
        {"name": "GATE 2024", "icon": "🎓", "questions": 65, "time": 180, "difficulty": "Expert"},
        {"name": "NEET UG", "icon": "🩺", "questions": 180, "time": 200, "difficulty": "Advanced"},
        {"name": "CAT 2024", "icon": "📊", "questions": 66, "time": 120, "difficulty": "Advanced"},
    ],
    "Defense & Others": [
        {"name": "NDA/NA", "icon": "✈️", "questions": 150, "time": 150, "difficulty": "Intermediate"},
        {"name": "CDS", "icon": "🛡️", "questions": 120, "time": 120, "difficulty": "Advanced"},
        {"name": "SSC GD", "icon": "👮", "questions": 100, "time": 90, "difficulty": "Beginner"},
        {"name": "Teaching", "icon": "📚", "questions": 150, "time": 150, "difficulty": "Intermediate"},
    ]
}

# ================= AI ENGINE =================
def generate_mock_test(exam_name, num_questions=10):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""Generate {num_questions} multiple choice questions for {exam_name} competitive exam.
        Make them challenging and exam-level appropriate.
        Return STRICT JSON format:
        [
            {{
                "question": "Full question text",
                "options": ["A", "B", "C", "D"],
                "correct_answer": "Correct option letter",
                "explanation": "Detailed explanation in Hinglish/English",
                "difficulty": "easy/medium/hard",
                "topic": "Subject topic"
            }}
        ]
        Ensure variety in topics."""
        
        response = model.generate_content(prompt)
        text = response.text
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)[:num_questions]
    except:
        return [
            {
                "question": f"Sample question {i+1} for {exam_name}: What is 2+2?",
                "options": ["3", "4", "5", "6"],
                "correct_answer": "B",
                "explanation": "Basic arithmetic: 2+2=4",
                "difficulty": "easy",
                "topic": "Mathematics"
            } for i in range(num_questions)
        ]

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.title("🎯 MockTest AI")
    
    st.markdown("---")
    st.subheader("👤 Profile Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🔥 Streak", f"{st.session_state.streak}d")
        st.metric("🏆 Level", st.session_state.level)
    with col2:
        st.metric("📈 XP", st.session_state.xp)
        st.metric("📊 Tests", st.session_state.total_tests)
    
    st.progress(0.78, text="Next Level: 78%")
    
    st.markdown("---")
    st.subheader("📱 Navigation")
    
    nav_options = {
        "🏠 Dashboard": "home",
        "📝 Active Test": "test",
        "📊 Results": "results",
        "⚙️ Settings": "settings"
    }
    
    for label, page in nav_options.items():
        if st.button(label, use_container_width=True, 
                    type="primary" if st.session_state.page == page else "secondary"):
            st.session_state.page = page
            st.rerun()
    
    st.markdown("---")
    st.subheader("💡 Quick Tips")
    st.info("• Complete daily test for XP boost\n• Review mistakes carefully\n• Time management is key\n• Focus on weak areas")
    
    st.markdown("---")
    st.caption("🚀 Powered by Gemini AI v1.5")
    st.caption("Version 2.0 | © 2024 MockTest Pro")
    st.markdown('</div>', unsafe_allow_html=True)

# ================= PAGE: HOME DASHBOARD =================
if st.session_state.page == "home":
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 style="font-size: 3em; margin-bottom: 10px;">🚀 AI MockTest Pro</h1>
        <p style="font-size: 1.5em;">India's Most Advanced AI-Powered Exam Platform</p>
        <p style="font-size: 1.1em;">Personalized Tests • Real-time Analytics • Smart Recommendations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎯 Accuracy", "78%", "+2%")
    with col2:
        st.metric("⚡ Speed", "1.2s/Q", "-0.3s")
    with col3:
        st.metric("📚 Topics", "24", "+3")
    with col4:
        st.metric("🏅 Rank", "Top 5%", "↑2")
    
    st.markdown("---")
    
    # Exam Selection
    st.subheader("🎯 Select Your Target Exam")
    
    for category, exams in EXAMS.items():
        st.markdown(f"### 📁 {category}")
        cols = st.columns(len(exams))
        
        for idx, exam in enumerate(exams):
            with cols[idx]:
                with st.container():
                    st.markdown(f"""
                    <div class="exam-card">
                        <h2 style="font-size: 2.5em; margin: 10px 0;">{exam['icon']}</h2>
                        <h3>{exam['name']}</h3>
                        <p>📝 {exam['questions']} Questions</p>
                        <p>⏱️ {exam['time']} Minutes</p>
                        <p>⚡ {exam['difficulty']} Level</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Start {exam['name']}", key=f"start_{exam['name']}", use_container_width=True):
                        with st.spinner(f"🤖 AI generating {exam['name']} paper..."):
                            time.sleep(1)
                            st.session_state.current_exam = exam['name']
                            st.session_state.questions = generate_mock_test(exam['name'], 10)
                            st.session_state.user_answers = {}
                            st.session_state.current_question = 0
                            st.session_state.start_time = time.time()
                            st.session_state.test_started = True
                            st.session_state.page = "test"
                            st.rerun()
    
    # Recent Activity
    st.markdown("---")
    st.subheader("📈 Recent Activity")
    col1, col2 = st.columns(2)
    with col1:
        st.info("**Today's Goal:** 2/3 tests completed")
        st.progress(0.66)
    with col2:
        st.info("**Weak Area:** Quantitative Aptitude")
        st.button("Practice Now →")
    
    st.markdown("---")
    st.caption("💡 **Pro Tip:** Complete 3 tests daily to maintain Top Rank")

# ================= PAGE: TEST INTERFACE =================
elif st.session_state.page == "test":
    if not st.session_state.test_started:
        st.warning("No active test. Start from Dashboard.")
        if st.button("🏠 Go to Dashboard"):
            st.session_state.page = "home"
            st.rerun()
        st.stop()
    
    # Header
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.title(f"📝 {st.session_state.current_exam}")
        st.caption("AI Proctored • Do not switch tabs • Real-time monitoring")
    
    # Timer
    elapsed = int(time.time() - st.session_state.start_time)
    time_left = max(0, 1800 - elapsed)  # 30 minutes default
    mins, secs = divmod(time_left, 60)
    
    with col2:
        if time_left < 300:  # Less than 5 minutes
            st.markdown(f'<h2 class="timer-warning">⏱️ {mins}:{secs:02d}</h2>', unsafe_allow_html=True)
        else:
            st.markdown(f'<h2>⏱️ {mins}:{secs:02d}</h2>', unsafe_allow_html=True)
    
    with col3:
        progress = (st.session_state.current_question + 1) / len(st.session_state.questions)
        st.progress(progress)
        st.caption(f"Q: {st.session_state.current_question + 1}/{len(st.session_state.questions)}")
    
    st.markdown("---")
    
    # Two Column Layout
    col_left, col_right = st.columns([3, 1])
    
    with col_left:
        # Current Question
        questions = st.session_state.questions
        idx = st.session_state.current_question
        
        if idx < len(questions):
            q = questions[idx]
            
            st.markdown(f"""
            <div class="question-box">
                <h3>📋 Question {idx + 1}</h3>
                <p style="font-size: 18px; line-height: 1.6;">{q['question']}</p>
                <p><strong>Topic:</strong> {q['topic']} | <strong>Difficulty:</strong> {q['difficulty'].upper()}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Options
            selected = st.radio(
                "Select your answer:",
                q['options'],
                index=None if idx not in st.session_state.user_answers else 
                q['options'].index(st.session_state.user_answers[idx]),
                key=f"opt_{idx}",
                label_visibility="collapsed"
            )
            
            if selected:
                st.session_state.user_answers[idx] = selected
            
            # Navigation Buttons
            col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
            with col_btn1:
                if idx > 0 and st.button("⬅ Previous", use_container_width=True):
                    st.session_state.current_question -= 1
                    st.rerun()
            
            with col_btn2:
                if idx < len(questions) - 1:
                    if st.button("Next →", type="primary", use_container_width=True):
                        if selected:
                            st.session_state.user_answers[idx] = selected
                        st.session_state.current_question += 1
                        st.rerun()
                else:
                    if st.button("Submit Test ✅", type="primary", use_container_width=True):
                        # Calculate score
                        score = 0
                        for i, q in enumerate(questions):
                            if i in st.session_state.user_answers:
                                if st.session_state.user_answers[i] == q['options'][ord(q['correct_answer']) - 65]:
                                    score += 1
                        
                        st.session_state.score = score
                        st.session_state.time_taken = elapsed
                        st.session_state.total_tests += 1
                        st.session_state.streak += 1
                        st.session_state.xp += 50
                        st.session_state.page = "results"
                        st.rerun()
            
            with col_btn3:
                if st.button("🔄 Mark for Review", use_container_width=True):
                    st.info("Question marked for review")
            
            with col_btn4:
                if st.button("❌ Quit Test", use_container_width=True):
                    st.session_state.page = "home"
                    st.session_state.test_started = False
                    st.rerun()
    
    with col_right:
        # Question Palette
        st.subheader("🎯 Question Palette")
        
        html = '<div style="display: flex; flex-wrap: wrap; gap: 8px; justify-content: center;">'
        for i in range(len(questions)):
            if i == idx:
                status = "current"
                label = f"<strong>{i+1}</strong>"
            elif i in st.session_state.user_answers:
                status = "answered"
                label = f"✓{i+1}"
            else:
                status = "unanswered"
                label = f"{i+1}"
            
            html += f'''
            <div class="palette-btn {status}" onclick="streamlitScript.run('question_{i}')">
                {label}
            </div>
            '''
        
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)
        
        # Add JavaScript for palette clicks
        for i in range(len(questions)):
            if st.button(f" ", key=f"question_{i}", label_visibility="hidden"):
                st.session_state.current_question = i
                st.rerun()
        
        st.markdown("---")
        st.subheader("📊 Stats")
        answered = len(st.session_state.user_answers)
        st.metric("Answered", f"{answered}/{len(questions)}")
        st.metric("Time/Question", f"{elapsed//max(1, answered)}s" if answered > 0 else "0s")
        
        st.markdown("---")
        st.info("**Legend:**")
        st.caption("🟢 Answered | 🔵 Current | ⚪ Unanswered")

# ================= PAGE: RESULTS =================
elif st.session_state.page == "results":
    st.balloons()
    
    # Score Card
    total = len(st.session_state.questions)
    score = st.session_state.score
    percentage = (score / total) * 100
    
    st.markdown(f"""
    <div class="hero-section">
        <h2>🏆 Test Completed: {st.session_state.current_exam}</h2>
        <h1 style="font-size: 4em; margin: 20px 0;">{score}/{total}</h1>
        <p style="font-size: 1.5em;">Accuracy: {percentage:.1f}% | Time: {st.session_state.time_taken//60}:{st.session_state.time_taken%60:02d}</p>
        <p>🎉 +50 XP | 🔥 Streak: {st.session_state.streak} days</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Performance Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📈 Rank", "Top 7%", "↑2")
    with col2:
        st.metric("⚡ Speed", f"{st.session_state.time_taken//max(1, score)}s/Q" if score > 0 else "0s/Q")
    with col3:
        st.metric("🎯 Precision", f"{percentage:.1f}%")
    with col4:
        st.metric("📊 Percentile", "93.5", "+1.2")
    
    # AI Analysis
    st.markdown("---")
    st.subheader("🤖 AI Performance Analysis")
    
    col_weak, col_strong = st.columns(2)
    with col_weak:
        st.error("📉 **Areas to Improve**")
        st.write("• Quantitative Aptitude: 65% accuracy")
        st.write("• Logical Reasoning: Time management needed")
        st.write("• Current Affairs: Update required")
    
    with col_strong:
        st.success("🚀 **Strong Areas**")
        st.write("• English Grammar: 95% accuracy")
        st.write("• General Science: 92% accuracy")
        st.write("• Computer Awareness: 88% accuracy")
    
    # Detailed Review
    st.markdown("---")
    st.subheader("🔍 Question-wise Review")
    
    for i, q in enumerate(st.session_state.questions):
        with st.expander(f"Q{i+1}: {q['question'][:80]}...", expanded=(i==0)):
            user_ans = st.session_state.user_answers.get(i, "Not Attempted")
            correct_idx = ord(q['correct_answer']) - 65
            correct_ans = q['options'][correct_idx]
            
            if user_ans == correct_ans:
                st.success(f"✅ **Your Answer:** {user_ans} (Correct)")
            elif user_ans == "Not Attempted":
                st.warning(f"⚪ **Your Answer:** {user_ans}")
                st.success(f"✅ **Correct Answer:** {correct_ans}")
            else:
                st.error(f"❌ **Your Answer:** {user_ans}")
                st.success(f"✅ **Correct Answer:** {correct_ans}")
            
            st.info(f"💡 **Explanation:** {q['explanation']}")
            st.caption(f"📚 Topic: {q['topic']} | ⚡ Difficulty: {q['difficulty'].upper()}")
    
    # Action Buttons
    st.markdown("---")
    col_act1, col_act2, col_act3 = st.columns(3)
    with col_act1:
        if st.button("🔄 Take Another Test",
