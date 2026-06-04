import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from dotenv import load_dotenv
import time

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="JARVIS",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #020b18 !important;
    color: #c8e8ff;
    font-family: 'Rajdhani', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 60% at 50% -10%, rgba(0,180,255,0.12) 0%, transparent 70%),
        radial-gradient(ellipse 40% 30% at 90% 80%, rgba(0,255,200,0.06) 0%, transparent 60%),
        #020b18 !important;
}

/* hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(0,180,255,0.3); border-radius: 2px; }

/* ── Layout wrapper ── */
.block-container {
    max-width: 860px !important;
    padding: 0 1.5rem 2rem !important;
    margin: 0 auto !important;
}

/* ── Header ── */
.jarvis-header {
    text-align: center;
    padding: 2.2rem 0 1.6rem;
    position: relative;
}
.jarvis-logo {
    font-family: 'Orbitron', monospace;
    font-size: clamp(2.4rem, 6vw, 3.6rem);
    font-weight: 900;
    letter-spacing: 0.3em;
    background: linear-gradient(135deg, #00d4ff 0%, #00ffcc 50%, #0080ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: none;
    animation: pulse-glow 3s ease-in-out infinite;
}
@keyframes pulse-glow {
    0%, 100% { filter: drop-shadow(0 0 12px rgba(0,212,255,0.5)); }
    50%       { filter: drop-shadow(0 0 28px rgba(0,255,200,0.8)); }
}
.jarvis-sub {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.78rem;
    letter-spacing: 0.4em;
    color: rgba(0,212,255,0.55);
    margin-top: 0.3rem;
    text-transform: uppercase;
}
.header-line {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,212,255,0.4), rgba(0,255,200,0.4), transparent);
    margin: 1.2rem 0 0;
}

/* ── HUD strip ── */
.hud-strip {
    display: flex;
    justify-content: center;
    gap: 2rem;
    padding: 0.6rem 0 1rem;
}
.hud-item {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.72rem;
    letter-spacing: 0.15em;
    color: rgba(0,212,255,0.5);
    text-transform: uppercase;
}
.hud-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #00ffcc;
    box-shadow: 0 0 6px #00ffcc;
    animation: blink 2s ease-in-out infinite;
}
@keyframes blink {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.2; }
}

/* ── Chat container ── */
.chat-area {
    background: rgba(0,20,40,0.55);
    border: 1px solid rgba(0,180,255,0.12);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(8px);
    min-height: 300px;
    max-height: 58vh;
    overflow-y: auto;
}

/* ── Message bubbles ── */
.msg-row {
    display: flex;
    margin-bottom: 1rem;
    gap: 0.6rem;
    animation: slide-in 0.3s ease-out;
}
@keyframes slide-in {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
.msg-row.user  { flex-direction: row-reverse; }
.msg-row.user .bubble {
    background: rgba(0,100,200,0.25);
    border: 1px solid rgba(0,160,255,0.3);
    border-radius: 16px 4px 16px 16px;
    color: #d0eeff;
}
.msg-row.bot .bubble {
    background: rgba(0,40,70,0.7);
    border: 1px solid rgba(0,255,200,0.15);
    border-radius: 4px 16px 16px 16px;
    color: #c0ffe8;
}
.bubble {
    padding: 0.65rem 1rem;
    font-size: 0.97rem;
    line-height: 1.55;
    max-width: 78%;
    word-break: break-word;
}
.avatar {
    width: 32px; height: 32px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.8rem;
    font-family: 'Orbitron', monospace;
    font-weight: 700;
    flex-shrink: 0;
    margin-top: 2px;
}
.avatar.user-av {
    background: rgba(0,100,200,0.4);
    border: 1px solid rgba(0,160,255,0.4);
    color: #7dd3fc;
}
.avatar.bot-av {
    background: rgba(0,200,160,0.15);
    border: 1px solid rgba(0,255,200,0.35);
    color: #00ffcc;
    box-shadow: 0 0 10px rgba(0,255,200,0.2);
}
.msg-time {
    font-size: 0.65rem;
    color: rgba(0,180,255,0.35);
    align-self: flex-end;
    margin: 0 0.2rem;
    flex-shrink: 0;
}

/* ── Thinking animation ── */
.thinking {
    display: flex; align-items: center; gap: 6px;
    padding: 0.5rem 0.8rem;
    color: rgba(0,255,200,0.6);
    font-size: 0.8rem;
    letter-spacing: 0.1em;
}
.dot-flashing span {
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #00ffcc;
    animation: dotflash 1.2s infinite;
}
.dot-flashing span:nth-child(2) { animation-delay: 0.2s; }
.dot-flashing span:nth-child(3) { animation-delay: 0.4s; }
@keyframes dotflash {
    0%, 80%, 100% { opacity: 0.2; transform: scale(0.8); }
    40%           { opacity: 1;   transform: scale(1.2); }
}

/* ── Input row ── */
.stTextInput > div > div > input {
    background: rgba(0,20,45,0.8) !important;
    border: 1px solid rgba(0,180,255,0.25) !important;
    border-radius: 10px !important;
    color: #c8e8ff !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s;
    caret-color: #00ffcc;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(0,255,200,0.5) !important;
    box-shadow: 0 0 0 3px rgba(0,255,200,0.08), 0 0 16px rgba(0,200,160,0.15) !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder { color: rgba(0,180,255,0.3) !important; }
.stTextInput label { display: none !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, rgba(0,100,180,0.4), rgba(0,60,120,0.6)) !important;
    border: 1px solid rgba(0,180,255,0.35) !important;
    border-radius: 10px !important;
    color: #7dd3fc !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    padding: 0.6rem 1.4rem !important;
    transition: all 0.2s !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, rgba(0,180,255,0.3), rgba(0,120,200,0.5)) !important;
    border-color: rgba(0,255,200,0.5) !important;
    color: #00ffcc !important;
    box-shadow: 0 0 14px rgba(0,200,160,0.2) !important;
    transform: translateY(-1px) !important;
}

/* ── Footer line ── */
.footer-line {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,180,255,0.2), transparent);
    margin: 1rem 0 0.5rem;
}
.footer-text {
    text-align: center;
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    color: rgba(0,180,255,0.25);
    text-transform: uppercase;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(0,10,25,0.95) !important;
    border-right: 1px solid rgba(0,180,255,0.1) !important;
}
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = [
        SystemMessage(content="You are JARVIS, an advanced AI assistant. Be concise, precise, and insightful. Address the user with subtle sophistication.")
    ]
if "display" not in st.session_state:
    st.session_state.display = []   # list of (role, text, timestamp)
if "llm" not in st.session_state:
    st.session_state.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="jarvis-header">
    <div class="jarvis-logo">JARVIS</div>
    <div class="jarvis-sub">Just A Rather Very Intelligent System</div>
    <div class="header-line"></div>
</div>
<div class="hud-strip">
    <div class="hud-item"><div class="hud-dot"></div> Online</div>
    <div class="hud-item"><div class="hud-dot" style="animation-delay:.6s"></div> Groq · LLaMA 3.3 70B</div>
    <div class="hud-item"><div class="hud-dot" style="animation-delay:1.2s"></div> Secure</div>
</div>
""", unsafe_allow_html=True)


# ── Chat display ──────────────────────────────────────────────────────────────
chat_html = '<div class="chat-area" id="chat-area">'

if not st.session_state.display:
    chat_html += """
    <div style="text-align:center; padding: 3rem 1rem; color: rgba(0,180,255,0.3);">
        <div style="font-family:'Orbitron',monospace; font-size:1.8rem; margin-bottom:.6rem; opacity:.4;">⬡</div>
        <div style="font-size:.85rem; letter-spacing:.15em; text-transform:uppercase;">Systems Online. Awaiting Input.</div>
    </div>"""
else:
    for role, text, ts in st.session_state.display:
        if role == "user":
            chat_html += f"""
            <div class="msg-row user">
                <div class="avatar user-av">YOU</div>
                <div class="msg-time">{ts}</div>
                <div class="bubble">{text}</div>
            </div>"""
        else:
            # preserve newlines
            safe_text = text.replace("\n", "<br>")
            chat_html += f"""
            <div class="msg-row bot">
                <div class="avatar bot-av">J</div>
                <div class="msg-time">{ts}</div>
                <div class="bubble">{safe_text}</div>
            </div>"""

chat_html += '</div>'
st.markdown(chat_html, unsafe_allow_html=True)

# Auto-scroll
st.markdown("""
<script>
const ca = document.getElementById('chat-area');
if(ca) ca.scrollTop = ca.scrollHeight;
</script>
""", unsafe_allow_html=True)


# ── Input row (form prevents re-run loop) ────────────────────────────────────
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2, col3 = st.columns([6, 1, 1])
    with col1:
        user_input = st.text_input("msg", placeholder="Send a command to JARVIS…",
                                   label_visibility="collapsed")
    with col2:
        send = st.form_submit_button("Send", use_container_width=True)
    with col3:
        clear = st.form_submit_button("Clear", use_container_width=True)

# ── Handle clear ─────────────────────────────────────────────────────────────
if clear:
    st.session_state.display = []
    st.session_state.history = [
        SystemMessage(content="You are JARVIS, an advanced AI assistant. Be concise, precise, and insightful.")
    ]
    st.rerun()

# ── Handle send ──────────────────────────────────────────────────────────────
if send and user_input.strip():
    query = user_input.strip()
    ts = time.strftime("%H:%M")

    st.session_state.display.append(("user", query, ts))
    st.session_state.history.append(HumanMessage(content=query))

    with st.spinner("JARVIS is thinking…"):
        response = st.session_state.llm.invoke(st.session_state.history)

    reply = response.content
    st.session_state.history.append(AIMessage(content=reply))
    st.session_state.display.append(("bot", reply, time.strftime("%H:%M")))

    st.rerun()


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-line"></div>
<div class="footer-text">JARVIS · Powered by Groq &amp; LangChain · v1.0</div>
""", unsafe_allow_html=True)