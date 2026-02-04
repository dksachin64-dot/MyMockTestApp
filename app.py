import streamlit as st
import time
import sys
import subprocess

# --- 1. MAGIC AUTO-INSTALLER (Ye Error Fix Karega) ---
# Ye check karega ki tool hai ya nahi. Agar nahi hai, to turant install karega.
try:
    from duckduckgo_search import DDGS
except ImportError:
    st.warning("⚙️ Installing Internet Search Tools... (Please wait)")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "duckduckgo-search"])
    from duckduckgo_search import DDGS
    st.success("✅ Installation Complete!")
    time.sleep(1)
    st.rerun()

import google.generativeai as genai

# --- 2. CONFIGURATION ---
st.set_page_config(page_title="Agent X: The Researcher", page_icon="🕵️", layout="wide")

# API Key
GOOGLE_API_KEY = "AIzaSyALMoUhT8s7GYOHexDYrhnMNVT1xqQ4bgE"
genai.configure(api_key=GOOGLE_API_KEY)

# --- 3. THE AGENT BRAIN (TOOLS) ---

def search_internet(query):
    """Real Internet Search using DuckDuckGo"""
    try:
        with DDGS() as ddgs:
            # 5 results layenge taaki agent ke paas zyada info ho
            results = list(ddgs.text(query, max_results=5))
            if results:
                return "\n".join([f"- {r['title']}: {r['body']} (Link: {r['href']})" for r in results])
            return "No results found."
    except Exception as e:
        return f"Search Error: {e}"

def run_agent(user_query):
    """
    Agent Logic: Thinking -> Searching -> Answering
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # UI Updates (Thinking Process)
    status_placeholder.info("🧠 Agent X is Thinking...")
    time.sleep(0.5)
    
    status_placeholder.warning(f"🌍 Searching Live Web for: '{user_query}'...")
    search_results = search_internet(user_query)
    
    status_placeholder.success("📝 Analyze & Writing Answer...")
    
    # AI ko Internet ka Data khilana
    prompt = f"""
    You are Agent X, an advanced AI with real-time internet access.
    
    USER QUESTION: {user_query}
    
    LIVE INTERNET DATA:
    {search_results}
    
    INSTRUCTIONS:
    1. Answer the user's question using the Internet Data.
    2. If data is about stock price, news, or sports, give the LATEST value.
    3. Keep it professional and direct.
    4. Provide links/sources at the end.
    """
    
    response = model.generate_content(prompt)
    status_placeholder.empty() # Remove status bar
    return response.text

# --- 4. UI DESIGN (MATRIX STYLE) ---
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #00ff41; font-family: 'Courier New', monospace; }
    
    /* Search Bar */
    .stTextInput > div > div > input {
        background-color: #111; color: #00ff41; 
        border: 1px solid #00ff41; border-radius: 5px;
    }
    
    /* Chat Bubbles */
    .user-msg { text-align: right; color: #00c6ff; margin: 10px; font-weight: bold; }
    .agent-msg { 
        border: 1px solid #00ff41; 
        padding: 15px; 
        background: #050505; 
        border-radius: 8px; 
        margin-top: 10px; 
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.1);
    }
    
    h1 { text-shadow: 0 0 10px #00ff41; border-bottom: 2px solid #00ff41; padding-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# --- 5. APP LAYOUT ---
st.title("🕵️ AGENT X : LIVE NET ACCESS")
st.markdown("ask me anything. I can search the **Real Internet**.")

# Chat History Session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input Box
query = st.chat_input("Enter Command (e.g., 'Who won the match yesterday?')")

# Show Old Chats
for message in st.session_state.messages:
    role_class = "user-msg" if message["role"] == "user" else "agent-msg"
    with st.chat_message(message["role"]):
        st.markdown(f'<div class="{role_class}">{message["content"]}</div>', unsafe_allow_html=True)

# Process New Query
if query:
    # Show User Query
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(f'<div class="user-msg">{query}</div>', unsafe_allow_html=True)
    
    # Agent Action
    with st.chat_message("assistant"):
        status_placeholder = st.empty() # Placeholder for status updates
        
        try:
            full_response = run_agent(query)
            
            # Show Answer
            st.markdown(f'<div class="agent-msg">{full_response}</div>', unsafe_allow_html=True)
            
            # Save History
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"System Error: {e}")
