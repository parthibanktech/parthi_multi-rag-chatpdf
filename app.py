# app.py — Sidebar + chat rendered inside iframe (components.html) so auto-scroll always works
from dotenv import load_dotenv
import streamlit as st
from pypdf import PdfReader
from openai import OpenAI
import numpy as np
import faiss
import os
import textwrap
import streamlit.components.v1 as components

# ===== CONFIG =====
EMBED_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"
CHUNK_SIZE = 1000
TOP_K = 5

# ===== INIT OPENAI =====
def init_openai():
    load_dotenv()
    key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", "")
    if not key:
        st.error("❌ Missing OPENAI_API_KEY in .env or Streamlit secrets.toml")
        st.stop()
    return OpenAI(api_key=key)

client = init_openai()

# ===== PDF HELPERS =====
def get_pdf_text(docs):
    text = ""
    for pdf in docs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
    return text

def chunk_text(text):
    chunks, current = [], ""
    for para in [p.strip() for p in text.split("\n") if p.strip()]:
        if len(current) + len(para) < CHUNK_SIZE:
            current += " " + para
        else:
            chunks.append(current.strip())
            current = para
    if current:
        chunks.append(current.strip())
    return chunks

def embed_texts(texts):
    all_emb = []
    for i in range(0, len(texts), 16):
        batch = texts[i:i + 16]
        res = client.embeddings.create(model=EMBED_MODEL, input=batch)
        all_emb.extend([np.array(x.embedding, dtype="float32") for x in res.data])
    return np.vstack(all_emb) if all_emb else np.zeros((0, 1536), dtype="float32")

def build_index(embeds):
    index = faiss.IndexFlatL2(embeds.shape[1])
    index.add(embeds)
    return index

def retrieve(query, index, chunks, k=TOP_K):
    q_emb = np.array(
        client.embeddings.create(model=EMBED_MODEL, input=[query]).data[0].embedding,
        dtype="float32",
    )
    D, I = index.search(np.array([q_emb]), k)
    return [chunks[i] for i in I[0] if 0 <= i < len(chunks)]

def answer_question(question, retrieved):
    ctx = "\n\n".join(
        [f"[Source {i + 1}]\n{textwrap.shorten(c, 800)}" for i, c in enumerate(retrieved)]
    )

    system_prompt = """
You are an expert AI assistant. ALWAYS reply in clean, well-structured **Markdown**, using:

- Clear section headings (##)
- Bullet points
- Numbered lists when explaining steps
- Bold for key concepts
- Code blocks (```java / ```python) when showing examples
- Tables when helpful
- Short paragraphs (2–3 sentences max)

NEVER produce long unformatted paragraphs.  
NEVER mix everything into one block.

Your answers **must follow this structure**:

## 🟦 Direct Answer  
(A short, clear answer in 2–3 sentences.)

## 🟩 Detailed Explanation  
(Concepts broken into subsections with bullets.)

## 🟧 Examples  
(Add relevant examples or code.)

## 🟪 Source References  
(List the context sources used: [Source 1], [Source 2], ...)

If context does not contain enough info, clearly say:
"Not enough information in the provided PDF context."
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": f"""
CONTEXT:
{ctx}

QUESTION:
{question}

Generate a clean, structured answer using the required markdown format.
""",
        },
    ]

    res = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages,
        temperature=0.2
    )
    return res.choices[0].message.content.strip()

# ===== STATE ENSURE =====
def _ensure_state():
    if "msgs" not in st.session_state:
        st.session_state.msgs = [{"role":"bot", "text":"👋 Hi! Upload a PDF to begin chatting."}]
    if "index" not in st.session_state:
        st.session_state.index = None
        st.session_state.chunks = None
    if "sidebar_q" not in st.session_state:
        st.session_state.sidebar_q = ""

def add_msg(role, text):
    st.session_state.msgs.append({"role": role, "text": text})

# ===== RENDER CHAT (Native Streamlit) =====
def render_chat():
    """
    Renders messages using Streamlit's native chat components.
    This guarantees correct Markdown rendering for headers, lists, and code.
    """
    for msg in st.session_state.msgs:
        # Map our internal roles to Streamlit's expected roles
        role = "assistant" if msg["role"] == "bot" else "user"
        
        with st.chat_message(role):
            st.markdown(msg["text"])

# ===== MAIN =====
def main():
    st.set_page_config(page_title="Parthi Multi RAG", layout="wide")
    _ensure_state()

    # Sidebar: upload, process
    with st.sidebar:
        st.title("🚀 Parthi Multi RAG")
        st.header("📂 Upload your PDFs")
        st.caption("⚠️ Max 50MB per file for best performance")
        docs = st.file_uploader("Drag and drop files here", accept_multiple_files=True, type=["pdf"])

        if st.button("Process"):
            if not docs:
                st.warning("Please upload at least one PDF file.")
            else:
                # Validate file sizes
                MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB in bytes
                oversized_files = [doc.name for doc in docs if doc.size > MAX_FILE_SIZE]
                
                if oversized_files:
                    st.error(f"❌ Files too large (max 50MB): {', '.join(oversized_files)}")
                    st.info("💡 Try splitting large PDFs or use smaller files.")
                else:
                    try:
                        with st.spinner("Processing PDFs..."):
                            text = get_pdf_text(docs)
                            if not text.strip():
                                add_msg("bot", "⚠️ No readable text found in PDFs. Please check if PDFs are text-based (not scanned images).")
                            else:
                                chunks = chunk_text(text)
                                if not chunks:
                                    add_msg("bot", "⚠️ Could not create text chunks. PDF might be empty.")
                                else:
                                    embeds = embed_texts(chunks)
                                    index = build_index(embeds)
                                    st.session_state.index = index
                                    st.session_state.chunks = chunks
                                    add_msg("bot", f"✅ Processed {len(docs)} file(s) into {len(chunks)} chunks.")
                                    st.success(f"✅ Ready! Processed {len(chunks)} chunks from {len(docs)} file(s).")
                    except Exception as e:
                        st.error(f"❌ Error processing PDFs: {str(e)}")
                        add_msg("bot", f"⚠️ Error: {str(e)}")

        st.markdown("---")
        if st.button("Clear Chat"):
            st.session_state.msgs = [{"role":"bot", "text":"👋 Hi! Upload a PDF to begin chatting."}]
            st.rerun()

    # Main Chat Interface
    render_chat()

    # Chat Input (Bottom of main area)
    if prompt := st.chat_input("Ask something about your PDFs..."):
        add_msg("user", prompt)
        
        if not st.session_state.get("index"):
            add_msg("bot", "⚠️ Please process PDFs first.")
        else:
            try:
                with st.spinner("Thinking..."):
                    res = retrieve(prompt, st.session_state.index, st.session_state.chunks)
                    if res:
                        ans = answer_question(prompt, res)
                        add_msg("bot", ans)
                    else:
                        add_msg("bot", "No relevant information found.")
            except Exception as e:
                add_msg("bot", f"⚠️ Error: {str(e)}")
        
        st.rerun()

if __name__ == "__main__":
    main()
