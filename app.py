import os
import tempfile
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DocuMind · RAG Assistant",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
    color: #e8e4dc !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: #0f0f18 !important;
    border-right: 1px solid #1e1e2e !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding: 2rem 1.5rem !important;
}

#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stDecoration"] { display: none !important; }

[data-testid="stMain"] .block-container {
    padding: 2.5rem 3rem !important;
    max-width: 1100px !important;
}

/* ── Logo / Title ── */
.app-logo {
    font-family: 'DM Serif Display', serif;
    font-size: 2.6rem;
    letter-spacing: -0.02em;
    line-height: 1;
    color: #f0ebe0;
    margin-bottom: 0.15rem;
}
.app-logo span { color: #c8a96e; }
.app-subtitle {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #555566;
    margin-bottom: 2.5rem;
}

/* ── Section labels ── */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #c8a96e;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #c8a96e33, transparent);
}

/* ── Stat cards ── */
.stat-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
    margin-bottom: 1.8rem;
}
.stat-card {
    background: #12121c;
    border: 1px solid #1e1e2e;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    position: relative;
    overflow: hidden;
}
.stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #c8a96e, transparent);
}
.stat-number {
    font-family: 'DM Serif Display', serif;
    font-size: 1.8rem;
    color: #c8a96e;
    line-height: 1;
    margin-bottom: 0.2rem;
}
.stat-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #44445a;
}

/* ── Upload zone ── */
[data-testid="stFileUploader"] {
    background: #12121c !important;
    border: 1.5px dashed #2a2a3e !important;
    border-radius: 12px !important;
    padding: 1.2rem !important;
    transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"]:hover { border-color: #c8a96e !important; }
[data-testid="stFileUploaderDropzone"] { background: transparent !important; }

/* ── Inline upload panel ── */
.upload-panel {
    background: #0d0d18;
    border: 1.5px solid #1e1e2e;
    border-radius: 16px;
    padding: 2.5rem 2rem;
    margin: 1.5rem 0;
    position: relative;
    overflow: hidden;
}
.upload-panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #c8a96e, #6e8ac8, transparent);
}
.upload-panel-icon {
    font-size: 2.8rem;
    display: block;
    margin-bottom: 0.8rem;
    opacity: 0.6;
}
.upload-panel-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.5rem;
    color: #c8a96e;
    margin-bottom: 0.4rem;
}
.upload-panel-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    color: #44445a;
    margin-bottom: 1.5rem;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #c8a96e, #a8844e) !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.04em !important;
    padding: 0.6rem 1.6rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px #c8a96e22 !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 28px #c8a96e44 !important;
}
.stButton > button:active { transform: translateY(0) !important; }
.stButton > button:disabled {
    background: #1e1e2e !important;
    color: #44445a !important;
    box-shadow: none !important;
}

/* ── Chat messages ── */
.chat-wrapper { display: flex; flex-direction: column; gap: 1.2rem; margin-bottom: 1.5rem; }
.msg-user { display: flex; justify-content: flex-end; gap: 0.8rem; align-items: flex-start; }
.msg-bot  { display: flex; justify-content: flex-start; gap: 0.8rem; align-items: flex-start; }

.bubble-user {
    background: linear-gradient(135deg, #1e1e3a, #16162a);
    border: 1px solid #2a2a4a;
    border-radius: 16px 4px 16px 16px;
    padding: 1rem 1.3rem;
    max-width: 72%;
    font-size: 0.92rem;
    line-height: 1.6;
    color: #dcd8f0;
}
.bubble-bot {
    background: #12121c;
    border: 1px solid #1e1e2e;
    border-radius: 4px 16px 16px 16px;
    padding: 1rem 1.3rem;
    max-width: 82%;
    font-size: 0.92rem;
    line-height: 1.7;
    color: #e8e4dc;
    position: relative;
}
.bubble-bot::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, #c8a96e, #6e8ac8);
    border-radius: 4px 0 0 4px;
}

.avatar {
    width: 34px; height: 34px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.9rem;
    flex-shrink: 0;
    font-family: 'DM Mono', monospace;
}
.avatar-user { background: linear-gradient(135deg, #2a2a4a, #1a1a2e); border: 1px solid #3a3a5a; color: #8888cc; }
.avatar-bot  { background: linear-gradient(135deg, #1e1a12, #2a2218); border: 1px solid #3a3020; color: #c8a96e; }

/* ── Context chunks panel ── */
.chunk-item {
    background: #12121e;
    border-left: 3px solid #c8a96e55;
    border-radius: 0 6px 6px 0;
    padding: 0.7rem 1rem;
    margin-bottom: 0.6rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    line-height: 1.6;
    color: #88886a;
}
.chunk-header {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #c8a96e66;
    margin-bottom: 0.4rem;
}

/* ── Input area ── */
.stTextInput > div > div > input {
    background: #12121c !important;
    border: 1.5px solid #1e1e2e !important;
    border-radius: 10px !important;
    color: #e8e4dc !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: #c8a96e !important;
    box-shadow: 0 0 0 3px #c8a96e11 !important;
}
.stTextInput > div > div > input::placeholder { color: #44445a !important; }

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: #12121c !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 8px !important;
    color: #e8e4dc !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #2a2a3e; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #3a3a5a; }

hr { border-color: #1e1e2e !important; margin: 1.5rem 0 !important; }

.sidebar-section {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #c8a96e;
    margin: 1.4rem 0 0.6rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #1e1e2e;
}

.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.08em;
    padding: 0.25rem 0.7rem;
    border-radius: 20px;
}
.badge-ready { background: #0d200d; border: 1px solid #1a4a1a; color: #4aaa4a; }
.badge-idle  { background: #1a1a10; border: 1px solid #3a3a20; color: #aaaa4a; }
.badge-dot   { width: 6px; height: 6px; border-radius: 50%; background: currentColor; animation: pulse 2s infinite; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
</style>
""", unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────────────────────
for key, default in {
    "messages": [],
    "vectorstore": None,
    "retriever": None,
    "chain": None,
    "doc_name": None,
    "chunk_count": 0,
    "show_context": True,
    "input_key": 0,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ── Shared processing function ────────────────────────────────────────────────
def build_index(file_obj, chunk_size, chunk_overlap, search_type, k_chunks):
    from langchain_community.document_loaders import PyPDFLoader, TextLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain_groq import ChatGroq
    from langchain_core.prompts import ChatPromptTemplate

    suffix = ".pdf" if file_obj.name.endswith(".pdf") else ".txt"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(file_obj.read())
        tmp_path = tmp.name

    loader = PyPDFLoader(tmp_path) if suffix == ".pdf" else TextLoader(tmp_path, encoding="utf-8")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vs = FAISS.from_documents(chunks, embeddings)
    retriever = vs.as_retriever(search_type=search_type, search_kwargs={"k": k_chunks})

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are DocuMind, a precise and helpful document assistant. "
         "Answer ONLY using the provided context. If the answer isn't in the context, say so clearly. "
         "Be concise, accurate, and well-structured."),
        ("human", "Context:\n{context}\n\nQuestion: {question}"),
    ])

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY"),
    )

    st.session_state.vectorstore = vs
    st.session_state.retriever = retriever
    st.session_state.chain = prompt | llm
    st.session_state.doc_name = file_obj.name
    st.session_state.chunk_count = len(chunks)
    st.session_state.messages = []
    os.unlink(tmp_path)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="app-logo">Docu<span>Mind</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">◈ RAG Intelligence System</div>', unsafe_allow_html=True)

    if st.session_state.vectorstore:
        st.markdown('<span class="badge badge-ready"><span class="badge-dot"></span>Index Ready</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge badge-idle"><span class="badge-dot"></span>Awaiting Document</span>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Document</div>', unsafe_allow_html=True)
    sidebar_file = st.file_uploader("Drop a file", type=["pdf", "txt"], label_visibility="collapsed")

    st.markdown('<div class="sidebar-section">Retrieval Settings</div>', unsafe_allow_html=True)
    k_chunks      = st.slider("Chunks to retrieve", 1, 8, 3)
    chunk_size    = st.slider("Chunk size (tokens)", 200, 1000, 500, step=50)
    chunk_overlap = st.slider("Overlap", 0, 200, 50, step=10)
    search_type   = st.selectbox("Search strategy", ["similarity", "mmr"])

    st.markdown('<div class="sidebar-section">Display</div>', unsafe_allow_html=True)
    st.session_state.show_context = st.toggle("Show retrieved context", value=st.session_state.show_context)

    sidebar_build = st.button("⟳  Build Index", use_container_width=True, disabled=sidebar_file is None)

    if st.session_state.vectorstore:
        st.markdown("---")
        if st.button("⇄  Change Document", use_container_width=True):
            st.session_state.vectorstore = None
            st.session_state.retriever   = None
            st.session_state.chain       = None
            st.session_state.doc_name    = None
            st.session_state.chunk_count = 0
            st.rerun()
        if st.button("⌫  Clear session", use_container_width=True):
            for k in ["messages", "vectorstore", "retriever", "chain", "doc_name", "chunk_count"]:
                st.session_state[k] = [] if k == "messages" else None if k != "chunk_count" else 0
            st.rerun()

# ── Sidebar build trigger ─────────────────────────────────────────────────────
if sidebar_build and sidebar_file:
    with st.spinner("Indexing document…"):
        build_index(sidebar_file, chunk_size, chunk_overlap, search_type, k_chunks)
    st.rerun()

# ── Main area ─────────────────────────────────────────────────────────────────
st.markdown('<div class="app-logo" style="font-size:2rem;">Docu<span style="color:#c8a96e">Mind</span></div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Retrieval-Augmented Generation · Powered by LLaMA 3.3 & FAISS</div>', unsafe_allow_html=True)

# ── INLINE UPLOAD — shown whenever no document is loaded ─────────────────────
if not st.session_state.vectorstore:
    st.markdown("""
    <div class="upload-panel">
        <span class="upload-panel-icon">⬡</span>
        <div class="upload-panel-title">Load a Document</div>
        <div class="upload-panel-sub">PDF or TXT · Supports drag & drop</div>
    </div>
    """, unsafe_allow_html=True)

    inline_file = st.file_uploader(
        "Upload document",
        type=["pdf", "txt"],
        label_visibility="collapsed",
        key="inline_uploader",
    )

    if inline_file:
        col_info, col_btn = st.columns([4, 1])
        with col_info:
            st.markdown(
                f'<div style="font-family:\'DM Mono\',monospace;font-size:0.8rem;color:#8888aa;padding-top:0.5rem;">📄 {inline_file.name}</div>',
                unsafe_allow_html=True,
            )
        with col_btn:
            if st.button("⟳  Build Index", key="inline_build"):
                with st.spinner("Indexing document…"):
                    build_index(inline_file, chunk_size, chunk_overlap, search_type, k_chunks)
                st.rerun()

# ── Stats row (post-load) ─────────────────────────────────────────────────────
if st.session_state.vectorstore:
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card">
            <div class="stat-number">{st.session_state.chunk_count}</div>
            <div class="stat-label">Index Chunks</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{len(st.session_state.messages) // 2}</div>
            <div class="stat-label">Turns in Session</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{k_chunks}</div>
            <div class="stat-label">Passages / Query</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f'<div class="section-label">Active Document</div>'
        f'<div style="font-family:\'DM Mono\',monospace;font-size:0.8rem;color:#8888aa;margin-bottom:1.5rem;">📄 {st.session_state.doc_name}</div>',
        unsafe_allow_html=True,
    )

st.markdown("---")
st.markdown('<div class="section-label">Conversation</div>', unsafe_allow_html=True)

# ── Chat history ──────────────────────────────────────────────────────────────
if not st.session_state.messages:
    if st.session_state.vectorstore:
        st.markdown("""
        <div style="text-align:center;padding:3rem 2rem;opacity:0.5;">
            <span style="font-size:2.5rem;display:block;margin-bottom:0.8rem;">◈</span>
            <div style="font-family:'DM Serif Display',serif;font-size:1.2rem;color:#666677;margin-bottom:0.4rem;">Index is ready</div>
            <div style="font-family:'DM Mono',monospace;font-size:0.72rem;color:#333344;letter-spacing:0.1em;">Ask anything about your document below</div>
        </div>
        """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg-user">
                <div class="bubble-user">{msg["content"]}</div>
                <div class="avatar avatar-user">U</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-bot">
                <div class="avatar avatar-bot">◈</div>
                <div class="bubble-bot">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.session_state.show_context and "context_chunks" in msg:
                with st.expander(f"↳ Retrieved {len(msg['context_chunks'])} context passages", expanded=False):
                    for i, chunk in enumerate(msg["context_chunks"], 1):
                        st.markdown(f"""
                        <div class="chunk-item">
                            <div class="chunk-header">Passage {i}</div>
                            {chunk[:420]}{"…" if len(chunk) > 420 else ""}
                        </div>
                        """, unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-label">Ask a Question</div>', unsafe_allow_html=True)

input_col, btn_col = st.columns([6, 1])
with input_col:
    question = st.text_input(
        "question",
        placeholder="What does the document say about…",
        label_visibility="collapsed",
        key=f"question_input_{st.session_state.input_key}",
        disabled=st.session_state.vectorstore is None,
    )
with btn_col:
    send = st.button("Send →", disabled=st.session_state.vectorstore is None, use_container_width=True)

# ── Answer ────────────────────────────────────────────────────────────────────
if send and question.strip() and st.session_state.chain:
    user_question = question.strip()
    st.session_state.input_key += 1
    st.session_state.messages.append({"role": "user", "content": user_question})

    with st.spinner("Retrieving & reasoning…"):
        retrieved = st.session_state.retriever.invoke(user_question)
        context   = "\n\n".join([doc.page_content for doc in retrieved])
        response  = st.session_state.chain.invoke({"context": context, "question": user_question})

    st.session_state.messages.append({
        "role": "assistant",
        "content": response.content,
        "context_chunks": [doc.page_content for doc in retrieved],
    })
    st.rerun()