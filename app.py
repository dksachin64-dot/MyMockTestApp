import streamlit as st
import google.generativeai as genai
import json, time, os

# ================= APP CONFIG =================
st.set_page_config(
    page_title="Pariksha AI Pro",
    layout="wide",
    page_icon="🎓"
)

# ================= API CONFIG (SAFE) =================
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ================= CSS =================
st.markdown("""
<style>
.stApp { background:#f6f7fb; }
.question-card{
    background:white;padding:25px;border-radius:15px;
    box-shadow:0 4px 12px rgba(0,0,0,.1);
    border-left:6px solid #4CAF50;
}
.timer-box{
    font-size:18px;font-weight:bold;color:#d9534f;
    background:white;padding:8px;border-radius:8px;
    text-align:center;border:1px solid #ddd;
}
.q-btn{
    width:45px;height:45px;border-radius:8px;
    font-weight:bold;border:none;margin:4px;
}
</style>
""", unsafe_allow_html=True)

# ================= SESSION =================
for k, v in {
    "questions": [],
    "idx": 0,
    "answers": {},
    "status": {},
    "start_time": None,
    "exam_on": False
}.items():
    st.session_state.setdefault(k, v)

# ================= EXAMS =================
EXAMS = {
    "Trending": ["SSC CGL", "SSC GD", "Railway ALP"],
    "Engineering": ["JEE Physics", "GATE CS"],
    "Medical": ["NEET Biology"],
    "Government": ["UPSC Prelims", "SSC CHSL"],
}

# ================= AI ENGINE =================
def generate_paper(exam):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
Create 10 MCQ mock questions for {exam}.
Difficulty mixed.
Return STRICT JSON only:
[
{{"q":"Question","opt":["A","B","C","D"],"ans":"A","exp":"Hinglish explanation"}}
]
"""
    res = model.generate_content(prompt)
    clean = res.text.replace("```json","").replace("```","").strip()
    return json.loads(clean)

# ================= SIDEBAR =================
with st.sidebar:
    st.title("📘 Pariksha AI Pro")
    cat = st.selectbox("Category", EXAMS.keys())
    exam = st.selectbox("Exam", EXAMS[cat])

    if st.button("🚀 START TEST", use_container_width=True):
        st.session_state.questions = generate_paper(exam)
        st.session_state.idx = 0
        st.session_state.answers = {}
        st.session_state.status = {i:"visited" for i in range(10)}
        st.session_state.start_time = time.time()
        st.session_state.exam_on = True
        st.rerun()

# ================= TIMER =================
def time_left():
    total = 15 * 60
    used = int(time.time() - st.session_state.start_time)
    return max(0, total - used)

# ================= EXAM SCREEN =================
if st.session_state.exam_on:
    qlist = st.session_state.questions
    i = st.session_state.idx
    q = qlist[i]

    if time_left() == 0:
        st.session_state.exam_on = False
        st.rerun()

    h1, h2, h3 = st.columns([2,1,1])
    h1.subheader(f"📝 {exam}")
    h2.progress((i+1)/len(qlist))
    h3.markdown(
        f"<div class='timer-box'>⏱️ {time_left()//60}:{time_left()%60:02d}</div>",
        unsafe_allow_html=True
    )

    c1, c2 = st.columns([3,1])

    with c1:
        st.markdown(
            f"<div class='question-card'><h4>Q{i+1}. {q['q']}</h4></div>",
            unsafe_allow_html=True
        )

        sel = st.radio(
            "Choose Answer",
            q["opt"],
            index=q["opt"].index(st.session_state.answers[i])
            if i in st.session_state.answers else None
        )

        b1,b2,b3 = st.columns(3)
        if b1.button("⬅ Prev") and i>0:
            st.session_state.idx -= 1
            st.rerun()

        if b2.button("💾 Save & Next"):
            if sel:
                st.session_state.answers[i]=sel
                st.session_state.status[i]="answered"
            if i<len(qlist)-1:
                st.session_state.idx+=1
            st.rerun()

        if b3.button("🟣 Review"):
            st.session_state.status[i]="review"
            st.session_state.idx=min(i+1,len(qlist)-1)
            st.rerun()

    with c2:
        st.write("### Question Palette")
        for x in range(len(qlist)):
            if st.button(f"{x+1}", key=f"p{x}", use_container_width=True):
                st.session_state.idx = x
                st.rerun()

        if st.button("✅ SUBMIT", use_container_width=True):
            st.session_state.exam_on = False
            st.rerun()

# ================= RESULT =================
elif st.session_state.questions:
    st.success("🎉 Exam Submitted")
    score = 0

    for i,q in enumerate(st.session_state.questions):
        ua = st.session_state.answers.get(i)
        if ua == q["ans"]:
            score+=1
            st.markdown(f"✅ Q{i+1} Correct")
        else:
            st.markdown(f"❌ Q{i+1} Wrong")
        st.info(q["exp"])

    st.metric("FINAL SCORE", f"{score}/10")

else:
    st.markdown("## 👋 Sidebar se exam select karke start karo")
