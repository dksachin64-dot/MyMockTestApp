import streamlit as st
import google.generativeai as genai
import time
import random

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Agent X: Pro Logic", page_icon="🕵️", layout="wide")

# API Key
GOOGLE_API_KEY = "AIzaSyALMoUhT8s7GYOHexDYrhnMNVT1xqQ4bgE"
genai.configure(api_key=GOOGLE_API_KEY)

# --- 2. THE AGENT LOGIC (Internal Brain) ---
def run_agent(user_query):
    """
    Agent Logic:
    1. Plan (Analysis)
    2. Retrieve (Knowledge)
    3. Execute (Answer)
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # --- PHASE 1: PLANNING (Simulation) ---
    with st.status("🧠 Agent X is processing...", expanded=True) as status:
        st.write("🔍 Analyzing Request Intent...")
        time.sleep(0.8)
        
        st.write(f"🌐 Scanning Knowledge Base for: '{user_query}'...")
        time.sleep(1)
        
        st.write("🛡️ Verifying Facts & Context...")
        time.sleep(0.7)
        
        status.update(label="✅ Data Synthesized!", state="complete", expanded=False)
    
    # --- PHASE 2: GENERATION ---
    prompt = f"""
    Act as 'Agent X', an advanced AI Assistant.
    
    USER QUERY: {user_query}
    
    INSTRUCTIONS:
    1. Provide a highly detailed and structured answer.
    2. If the user asks for current news, provide the latest info you have (up to your training cutoff).
    3. Use a professional, hacker-like tone.
    4. Format with bold headings and bullet points.
    
    RESPONSE FORMAT:
    - ⚡ **Direct Answer**
    - 📂 **Detailed Analysis**
    - 🔮 **Key Insights**
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Secure Connection Error: {e}"

# --- 3. UI DESIGN (CYBERPUNK / HACKER THEME) ---
st.markdown("""
<style>
    /* Global Settings */
    .stApp { background-color: #000000; color: #00ff41; font-family: 'Courier New', monospace; }
    
    /* Input Field */
    .stTextInput > div > div > input {
        background-color: #0d0d0d; 
        color: #00ff41; 
        border: 1px solid #00ff41; 
        border-radius: 5px;
        padding: 10px;
    }
    
    /* Header */
    .header-box {
        border-bottom: 2px solid #00ff41;
        padding-bottom: 10px;
        margin-bottom: 20px;
        text-align: center;
    }
    .header-title { font-size: 40px; text-shadow: 0 0 10px #00ff41; margin: 0; }
    .header-sub { font-size: 14px; color: #008F11; }

    /* Chat Messages */
    .user-msg { 
        text-align: right; 
        color: #00c6ff; 
        font-weight: bold; 
        margin: 10px 0; 
        padding: 10px;
        border-right: 3px solid #00c6ff;
    }
    
    .agent-box { 
        border: 1px solid #00ff41; 
        padding: 20px; 
        background: #050505; 
        border-radius: 8px; 
        margin-top: 10px; 
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.15);
        position: relative;
    }
    
    /* Typing Cursor Animation */
    @keyframes blink { 50% { opacity: 0; } }
    .cursor { animation: blink 1s step-end infinite; }
</style>
""", unsafe_allow_html=True)

# --- 4. APP LAYOUT ---
# Header
st.markdown("""
<div class="header-box">
    <h1 class="header-title">AGENT X </h1>
    <span class="header-sub">SYSTEM ONLINE | ENCRYPTION: ON | LOGIC: ADVANCED</span>
</div>
""", unsafe_allow_html=True)

# Chat Session Management
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input Area
query = st.chat_input("Enter Protocol Command... (e.g., 'Explain Quantum Physics')")

# Display History
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-msg">USER: {message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="agent-box">{message["content"]}</div>', unsafe_allow_html=True)

# Logic Execution
if query:
    # 1. Show User Message
    st.session_state.messages.append({"role": "user", "content": query})
    st.markdown(f'<div class="user-msg">USER: {query}</div>', unsafe_allow_html=True)
    
    # 2. Agent Processing
    with st.chat_message("assistant"):
        # Run Logic
        full_response = run_agent(query)
        
        # Display Agent Response with Effect
        st.markdown(f"""
        <div class="agent-box">
            {full_response}
            <br><br>
            <small style="color:#008F11;">_ transmission ended _</small>
        </div>
        """, unsafe_allow_html=True)
        
        # Save to History
        st.session_state.messages.append({"role": "assistant", "content": full_response})

