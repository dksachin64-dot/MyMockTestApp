import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS
import time

# --- CONFIGURATION ---
st.set_page_config(page_title="Agent X: The Researcher", page_icon="🕵️", layout="wide")

# API Key Setup
# Agar aapke paas nayi key hai to yahan dalein, purani limit over ho sakti hai
GOOGLE_API_KEY = "AIzaSyALMoUhT8s7GYOHexDYrhnMNVT1xqQ4bgE" 
genai.configure(api_key=GOOGLE_API_KEY)

# --- THE AGENT BRAIN (TOOLS) ---

def search_internet(query):
    """Real Internet Search using DuckDuckGo"""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=4))
            if results:
                return "\n".join([f"- {r['title']}: {r['body']} (Link: {r['href']})" for r in results])
            return "No results found."
    except Exception as e:
        return f"Search Error: {e}"

def run_agent(user_query):
    """
    Agent Logic:
    1. Sochta hai (Thinking)
    2. Tool use karta hai (Searching)
    3. Jawab banata hai (Answering)
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Step 1: Decision Making
    status_placeholder.markdown("🧠 **Agent X is Thinking...**")
    time.sleep(1)
    
    # Simple logic: Har query ke liye internet search karega (Best for Live Info)
    status_placeholder.markdown(f"🌍 **Searching Internet for:** *'{user_query}'*...")
    search_results = search_internet(user_query)
    
    # Step 2: Processing Info
    status_placeholder.markdown("📝 **Reading & Synthesizing Data...**")
    
    prompt = f"""
    You are an AI Agent named 'Agent X'.
    You have access to real-time internet search results.
    
    USER QUERY: {user_query}
    
    SEARCH RESULTS FROM INTERNET:
    {search_results}
    
    INSTRUCTIONS:
    1. Answer the user's query using the Search Results.
    2. Be professional, concise, and accurate.
    3. Cite the links if available.
    4. If the info is not in the search results, say "I couldn't find live info on this."
    """
    
    response = model.generate_content(prompt)
    status_placeholder.empty() # Clear status
    return response.text

# --- UI DESIGN (HACKER STYLE) ---
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #00ff41; font-family: 'Courier New', monospace; }
    
    /* Input Box */
    .stTextInput > div > div > input {
        background-color: #111; color: #00ff41; border: 1px solid #00ff41;
    }
    
    /* Result Box */
    .agent-response {
        border: 1px solid #00ff41;
        padding: 20px;
        background: #0a0a0a;
        border-radius: 5px;
        margin-top: 20px;
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.2);
    }
    
    /* Title */
    h1 { text-shadow: 0 0 10px #00ff41; }
</style>
""", unsafe_allow_html=True)

# --- APP LAYOUT ---
st.title("🕵️ AGENT X : LIVE ACCESS")
st.markdown("I am not just a chatbot. I have access to the **Real-Time Internet**.")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input
query = st.chat_input("Command me: (e.g., 'What is the price of Bitcoin right now?')")

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Agent Action
if query:
    # User Msg
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)
    
    # Agent Msg Container
    with st.chat_message("assistant"):
        status_placeholder = st.empty() # For live updates
        
        try:
            # RUN THE AGENT
            full_response = run_agent(query)
            
            st.markdown(f"""
            <div class="agent-response">
                {full_response}
            </div>
            """, unsafe_allow_html=True)
            
            # Save history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Agent Connection Failed: {e}")
            st.info("Tip: Check your Internet or API Key Quota.")

