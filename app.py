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
    messages = [
        {"role": "system", "content": "You are a helpful assistant that answers based only on the PDF context."},
        {"role": "user", "content": f"CONTEXT:\n{ctx}\n\nQUESTION:\n{question}"},
    ]
    res = client.chat.completions.create(model=CHAT_MODEL, messages=messages, temperature=0.2)
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

# ===== RENDER INTO IFRAME (guaranteed JS run + auto-scroll) =====
def render_messages_iframe(iframe_height=800):
    """
    Renders messages into an HTML string and displays via components.html.
    The embedded script will auto-scroll the chat box to the bottom.
    """
    # Build messages HTML
    msgs_html = ""
    for m in st.session_state.msgs:
        if m["role"] == "bot":
            msgs_html += (
                "<div class='msg-row'>"
                "<div class='avatar bot'>🤖</div>"
                f"<div class='bubble bot'>{m['text']}</div>"
                "</div>\n"
            )
        else:
            msgs_html += (
                "<div class='msg-row user'>"
                f"<div class='bubble user'>{m['text']}</div>"
                "<div class='avatar user'>YOU</div>"
                "</div>\n"
            )

    # Full HTML: CSS + messages + JS to auto-scroll to bottom
    html = f"""
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8"/>
        <style>
          body {{ margin:0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial; background: white; }}
          .wrap {{ padding: 18px 24px; box-sizing: border-box; }}
          .chat-box {{ height: 100%; overflow-y: auto; box-sizing: border-box; padding-bottom: 20px; }}
          .msg-row {{ display:flex; align-items:flex-start; margin:10px 0; max-width:100%; }}
          .msg-row.user {{ justify-content:flex-end; }}
          .avatar {{ width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:600; margin:0 10px; flex-shrink:0; }}
          .avatar.bot {{ background: #dbeafe; color:#0b3a78; }}
          .avatar.user {{ background: #0b93f6; color:#fff; }}
          .bubble {{ padding:10px 14px; border-radius:12px; max-width:70%; line-height:1.4; font-size:15px; word-break:break-word; box-shadow: 0 4px 10px rgba(0,0,0,0.03); }}
          .bubble.bot {{ background:#edf2ff; color:#0b2a4a; border-bottom-left-radius:4px; }}
          .bubble.user {{ background:#0b93f6; color:#fff; border-bottom-right-radius:4px; }}
        </style>
      </head>
      <body>
        <div class="wrap">
          <div class="chat-box" id="chatBox">
            {msgs_html}
          </div>
        </div>

        <script>
          // Auto-scroll to bottom after rendering
          (function() {{
            const box = document.getElementById('chatBox');
            if (box) {{
              // small timeout to ensure layout done
              setTimeout(function(){{ box.scrollTop = box.scrollHeight; }}, 50);
            }}
          }})();
        </script>
      </body>
    </html>
    """

    # Render inside iframe; height adjustable
    components.html(html, height=iframe_height, scrolling=True)

# ===== MAIN =====
def main():
    st.set_page_config(page_title="Chat with PDFs", layout="wide")
    _ensure_state()

    # Sidebar: upload, process, and stable input
    with st.sidebar:
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
        st.markdown("💡 Ask questions below.")
        st.text_input("Ask something about your PDFs...", key="sidebar_q", placeholder="Type your question...")

        def sidebar_send_cb():
            q = st.session_state.get("sidebar_q", "").strip()
            if not q:
                return
            add_msg("user", q)
            if not st.session_state.get("index"):
                add_msg("bot", "⚠️ Please process PDFs first.")
                st.session_state.sidebar_q = ""
                return
            try:
                with st.spinner("Thinking..."):
                    res = retrieve(q, st.session_state.index, st.session_state.chunks)
                    if res:
                        ans = answer_question(q, res)
                        add_msg("bot", ans)
                    else:
                        add_msg("bot", "No relevant information found.")
            except Exception as e:
                add_msg("bot", f"⚠️ Error: {str(e)}")
            finally:
                st.session_state.sidebar_q = ""

        st.button("Send", on_click=sidebar_send_cb)

    # Render chat inside iframe (guaranteed auto-scroll)
    # You can increase iframe_height if the chat area looks small on your screen
    render_messages_iframe(iframe_height=800)

if __name__ == "__main__":
    main()
