import streamlit as st
import json
import os
from app.chains import get_chain

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="Alex - Tech AI",
    page_icon="🤖",
    layout="centered"
)

# -------------------------
# Custom UI Styling
# -------------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.user-msg {
    background-color: #1f77b4;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
    text-align: right;
}
.bot-msg {
    background-color: #262730;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Title
# -------------------------
st.markdown("<h1 style='text-align:center;'>🤖 Alex - Tech Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>Ask only tech-related questions</p>", unsafe_allow_html=True)

# -------------------------
# Load LLM Chain
# -------------------------
@st.cache_resource
def load_chain():
    return get_chain()

chain = load_chain()

# -------------------------
# Chat History File
# -------------------------
CHAT_FILE = "chat_history.json"

# Load chat history
if os.path.exists(CHAT_FILE):
    with open(CHAT_FILE, "r") as f:
        st.session_state.messages = json.load(f)
else:
    if "messages" not in st.session_state:
        st.session_state.messages = []

# -------------------------
# Clear Chat Button
# -------------------------
if st.button("🗑 Clear Chat"):
    st.session_state.messages = []
    if os.path.exists(CHAT_FILE):
        os.remove(CHAT_FILE)
    st.rerun()

# -------------------------
# Recent Questions Section
# -------------------------
if st.session_state.messages:
    st.markdown("### 🕒 Recent Questions")

    recent_questions = [
        msg["content"]
        for msg in st.session_state.messages
        if msg["role"] == "user"
    ][-5:]

    for q in reversed(recent_questions):
        st.markdown(f"• {q}")

# -------------------------
# Display Chat Messages
# -------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'>{msg['content']}</div>", unsafe_allow_html=True)

# -------------------------
# User Input
# -------------------------
user_input = st.chat_input("💬 Ask your tech question...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Format history for LLM
    history_text = "\n".join(
        [f"{m['role']}: {m['content']}" for m in st.session_state.messages]
    )

    # Get response
    response = chain.invoke({
        "input": user_input,
        "history": history_text
    })

    # Add bot response
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Save to file
    with open(CHAT_FILE, "w") as f:
        json.dump(st.session_state.messages, f)

    st.rerun()