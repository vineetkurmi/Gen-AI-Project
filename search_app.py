import os
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

st.set_page_config(
    page_title="PulseNews",
    page_icon="📡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0d0d0d;
    color: #e8e0d0;
}
.stApp { background: #0d0d0d; }

/* scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0d0d0d; }
::-webkit-scrollbar-thumb { background: #c9a84c55; border-radius: 3px; }

/* ── Masthead ── */
.masthead {
    text-align: center;
    padding: 2.8rem 0 1.8rem;
    border-bottom: 1px solid #1e1e1e;
    margin-bottom: 2rem;
}
.masthead-sub {
    font-size: 0.7rem;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #4a4540;
    margin-bottom: 0.5rem;
}
.masthead-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(3rem, 7vw, 5rem);
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #f5edd8;
    line-height: 1;
    margin: 0;
}
.masthead-title .gold { color: #c9a84c; }
.masthead-date {
    font-size: 0.72rem;
    color: #3a3530;
    margin-top: 0.6rem;
    letter-spacing: 0.12em;
}

/* ── Section label ── */
.section-label {
    font-size: 0.65rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #4a4540;
    margin-bottom: 0.9rem;
    margin-top: 0.2rem;
}

/* ── Category grid ── */
.cat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin-bottom: 1.6rem;
}
.cat-btn {
    background: #111111;
    border: 1px solid #222222;
    border-radius: 8px;
    padding: 12px 8px;
    text-align: center;
    cursor: pointer;
    transition: all 0.16s ease;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 5px;
}
.cat-btn:hover { border-color: #c9a84c; background: #1a1608; }
.cat-btn.sel   { border-color: #c9a84c; background: #1a1608; box-shadow: 0 0 0 1px #c9a84c30; }
.cat-icon  { font-size: 1.3rem; }
.cat-label { font-size: 0.7rem; font-weight: 500; color: #8a8078; letter-spacing: 0.04em; }
.cat-btn.sel .cat-label { color: #c9a84c; }

/* ── Streamlit selectbox (category picker) ── */
div[data-testid="stSelectbox"] > label { display: none !important; }
div[data-testid="stSelectbox"] > div > div {
    background: #111111 !important;
    border: 1px solid #2a2a2a !important;
    color: #e8e0d0 !important;
    border-radius: 8px !important;
    font-size: 0.9rem !important;
}
div[data-testid="stSelectbox"] > div > div:hover,
div[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: #c9a84c !important;
}
div[data-testid="stSelectbox"] svg { fill: #c9a84c !important; }

/* dropdown popup */
div[data-baseweb="popover"] ul {
    background: #161616 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 8px !important;
}
div[data-baseweb="popover"] li {
    color: #c8bfb0 !important;
    font-size: 0.88rem !important;
}
div[data-baseweb="popover"] li:hover,
div[data-baseweb="popover"] li[aria-selected="true"] {
    background: #1a1608 !important;
    color: #c9a84c !important;
}

/* ── Text input ── */
div[data-testid="stTextInput"] > label { color: #6b6356 !important; font-size: 0.75rem !important; letter-spacing: 0.12em !important; text-transform: uppercase !important; }
div[data-testid="stTextInput"] input {
    background: #111111 !important;
    border: 1px solid #2a2a2a !important;
    color: #e8e0d0 !important;
    border-radius: 8px !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #c9a84c !important;
    box-shadow: 0 0 0 1px #c9a84c30 !important;
}
div[data-testid="stTextInput"] input::placeholder { color: #3a3530 !important; }

/* ── Fetch button ── */
div[data-testid="stButton"] > button {
    background: #c9a84c !important;
    color: #0d0d0d !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 0.65rem 2rem !important;
    width: 100% !important;
    margin-top: 0.3rem !important;
    transition: all 0.16s !important;
}
div[data-testid="stButton"] > button:hover {
    background: #e0bf6a !important;
    transform: translateY(-1px) !important;
}

/* ── Download button ── */
div[data-testid="stDownloadButton"] > button {
    background: transparent !important;
    color: #c9a84c !important;
    border: 1px solid #c9a84c40 !important;
    border-radius: 8px !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 0.5rem 1.2rem !important;
    width: auto !important;
    transition: all 0.16s !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    background: #c9a84c !important;
    color: #0d0d0d !important;
}

/* ── News card ── */
.news-card {
    background: #111111;
    border: 1px solid #1e1e1e;
    border-radius: 12px;
    padding: 2rem 2.2rem 2.2rem;
    margin-top: 1.2rem;
    position: relative;
    overflow: hidden;
}
.news-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #c9a84c 0%, #6b4f10 100%);
}

/* Topic badge */
.topic-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #1a1608;
    border: 1px solid #c9a84c40;
    color: #c9a84c;
    font-size: 0.68rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 0.4rem;
    margin-top: 1.2rem;
}

/* Empty state */
.empty-state {
    text-align: center;
    padding: 4rem 2rem 5rem;
}
.empty-icon { font-size: 3rem; margin-bottom: 1rem; opacity: 0.4; }
.empty-text {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: 1.1rem;
    color: #2e2a26;
}

/* Divider */
hr { border-color: #1a1a1a !important; margin: 1.5rem 0 !important; }

/* Spinner */
div[data-testid="stSpinner"] div { border-top-color: #c9a84c !important; }

/* Warning / info */
div[data-testid="stAlert"] { border-radius: 8px !important; background: #161208 !important; border-color: #c9a84c40 !important; color: #c8bfb0 !important; }

/* Hide branding & sidebar toggle */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
[data-testid="collapsedControl"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Imports ──────────────────────────────────────────────────────────────────
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import SystemMessage

# ── Constants ────────────────────────────────────────────────────────────────
CATEGORIES = [
    ("🌍", "World",         "Latest major world news and geopolitical developments today"),
    ("🤖", "AI & Tech",     "Latest AI and technological breakthroughs today"),
    ("💼", "Business",      "Latest business, markets and finance news today"),
    ("⚽", "Sports",        "Latest sports results and news today"),
    ("🎬", "Entertainment", "Latest entertainment and celebrity news today"),
    ("🇮🇳", "India",        "Latest news and developments from India today"),
    ("🔬", "Science",       "Latest scientific discoveries and research today"),
    ("✏️", "Custom",        None),
]

# ── Session state ─────────────────────────────────────────────────────────────
for key, default in [
    ("selected_idx", 0),
    ("history", []),
    ("current_summary", None),
    ("current_topic", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Agent (cached) ────────────────────────────────────────────────────────────
@st.cache_resource
def build_agent():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY"),
    )
    tool = TavilySearch(max_results=3, api_key=os.getenv("TAVILY_API_KEY"))
    sys_msg = SystemMessage(content="""
You are an intelligent News Research Assistant.
Always use the search tool for current information. Never invent facts.

Response format (use exactly this structure):

# <Topic Title>

## Key Highlights
• Point 1
• Point 2
• Point 3

## Detailed Summary
• Development 1
• Development 2
• Development 3

## Why It Matters
• Impact or significance

## Sources
• Source name – URL or publication
""")
    return create_react_agent(
        model=llm,
        tools=[tool],
        checkpointer=InMemorySaver(),
        prompt=sys_msg,
    )

def fetch_news(query: str) -> str:
    agent  = build_agent()
    config = {"configurable": {"thread_id": "pulsenews-1"}}
    resp   = agent.invoke(
        {"messages": [{"role": "user", "content": f"Give me today's latest news summary for: {query}"}]},
        config=config,
    )
    for msg in reversed(resp.get("messages", [])):
        if hasattr(msg, "content") and msg.content:
            return msg.content
    return "No response received."

# ── Masthead ──────────────────────────────────────────────────────────────────
today = datetime.now().strftime("%A, %B %d, %Y")
st.markdown(f"""
<div class="masthead">
  <p class="masthead-sub">Your intelligent news briefing</p>
  <h1 class="masthead-title">Pulse<span class="gold">News</span></h1>
  <p class="masthead-date">{today}</p>
</div>
""", unsafe_allow_html=True)

# ── Category selector ─────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Choose a category</div>', unsafe_allow_html=True)

cat_labels = [f"{icon}  {name}" for icon, name, _ in CATEGORIES]
selected_label = st.selectbox("Category", cat_labels, index=st.session_state.selected_idx, label_visibility="collapsed")
selected_idx   = cat_labels.index(selected_label)
st.session_state.selected_idx = selected_idx

icon, name, default_query = CATEGORIES[selected_idx]

# Custom topic input
custom_query = ""
if default_query is None:
    custom_query = st.text_input("Custom Topic", placeholder="e.g.  quantum computing, Formula 1, budget 2026…")

st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# ── Fetch button ──────────────────────────────────────────────────────────────
fetch = st.button("⚡  Fetch Latest News")

st.markdown("<hr>", unsafe_allow_html=True)

# ── Action ────────────────────────────────────────────────────────────────────
if fetch:
    if default_query is None:
        if not custom_query.strip():
            st.warning("Please enter a custom topic above.")
            st.stop()
        query         = f"Latest news about {custom_query.strip()}"
        display_label = custom_query.strip().title()
    else:
        query         = default_query
        display_label = name

    with st.spinner(f"Scanning sources for **{display_label}**…"):
        try:
            summary = fetch_news(query)
            st.session_state.current_summary = summary
            st.session_state.current_topic   = f"{icon}  {display_label}"
            # history
            if not st.session_state.history or st.session_state.history[-1][0] != display_label:
                st.session_state.history.append((display_label, summary))
        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()

# ── Result display ─────────────────────────────────────────────────────────────
if st.session_state.current_summary:
    st.markdown(f'<div class="topic-badge">{st.session_state.current_topic}</div>', unsafe_allow_html=True)
    st.markdown(st.session_state.current_summary)

    col1, col2 = st.columns([1, 3])
    with col1:
        st.download_button(
            label="⬇  Download",
            data=st.session_state.current_summary,
            file_name=f"pulsenews_{name.replace(' ','_').lower()}.md",
            mime="text/markdown",
        )

    # History
    if len(st.session_state.history) > 1:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="section-label">Recent searches</div>', unsafe_allow_html=True)
        for lbl, summ in reversed(st.session_state.history[-5:]):
            if st.button(f"↩  {lbl}", key=f"hist_{lbl}"):
                st.session_state.current_summary = summ
                st.session_state.current_topic   = lbl
                st.rerun()
else:
    st.markdown("""
    <div class="empty-state">
      <div class="empty-icon">📡</div>
      <div class="empty-text">Select a category and hit Fetch Latest News</div>
    </div>
    """, unsafe_allow_html=True)